"""One lightweight supervisor per managed app, with Linux orphan adoption."""

import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import threading
import time

from .linux_process import (ProcessIdentity, enable_child_subreaper, identify_listener_processes,
                            process_identity_alive, read_linux_process, read_process_descendants,
                            signal_verified_process)
from .portless_state import read_portless_routes, require_ready_portless_proxy
from .private_state import WorkflowError
from .server_registry import (MAX_SERVERS, ServerRegistry, retain_live_server_owners, server_record_key)
from .workspace_context import WorkspaceBinding


def reap_owned_children() -> None:
    """Reap children only inside the dedicated supervisor, not in the calling harness."""
    while True:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                return
        except ChildProcessError:
            return


def supervise_owned_tree(root: ProcessIdentity, known: dict[int, ProcessIdentity]) -> dict:
    """Retain exact identities before children detach or their launch parent exits."""
    snapshots = read_process_descendants(root)
    for pid, snapshot in snapshots.items():
        if pid != root.pid:
            known[pid] = snapshot.identity
    return snapshots


def stop_owned_tree(root: ProcessIdentity, known: dict[int, ProcessIdentity], launcher: ProcessIdentity | None,
                    *, grace: float = 3) -> bool:
    """Let Portless remove its own route, then stop verified child survivors without group/PID reuse races."""
    supervise_owned_tree(root, known)
    if launcher:
        signal_verified_process(launcher, signal.SIGTERM)
    deadline = time.monotonic() + grace
    wake = threading.Event()
    while time.monotonic() < deadline:
        supervise_owned_tree(root, known)
        reap_owned_children()
        if not any(process_identity_alive(value) for value in known.values()):
            return True
        wake.wait(0.05)
    for child in known.values():
        signal_verified_process(child, signal.SIGTERM)
    deadline = time.monotonic() + 1
    while time.monotonic() < deadline:
        supervise_owned_tree(root, known)
        reap_owned_children()
        if not any(process_identity_alive(value) for value in known.values()):
            return True
        wake.wait(0.05)
    for child in known.values():
        signal_verified_process(child, signal.SIGKILL)
    deadline = time.monotonic() + 1
    while time.monotonic() < deadline:
        supervise_owned_tree(root, known)
        reap_owned_children()
        if not any(process_identity_alive(value) for value in known.values()):
            return True
        wake.wait(0.05)
    return False


def run_server_supervisor(root_directory: Path, binding: WorkspaceBinding, app: dict, owner: dict,
                          command: list[str], portless_directory: Path, response: socket.socket,
                          *, ready_timeout: float = 20, grace: float = 3) -> int:
    """Acquire/reuse is locked until transport readiness; every launched child has a cleanup path."""
    enable_child_subreaper()
    registry = ServerRegistry(root_directory)
    current = read_linux_process(os.getpid())
    if current is None:
        raise WorkflowError('SERVER_UNSUPPORTED', 'The supervisor process identity is unavailable.')
    supervisor = current.identity
    key = server_record_key(app['hostname'], portless_directory)
    known: dict[int, ProcessIdentity] = {}
    launcher = None
    generation = None
    owns_resource = False
    shutdown = threading.Event()
    command_process = None
    previous_handlers = {}
    control = socket.socket(fileno=os.dup(response.fileno()))
    control.setblocking(False)
    response_sent = False

    def send_response(output: dict) -> None:
        nonlocal response_sent
        import json
        response.sendall((json.dumps(output) + '\n').encode())
        response_sent = True

    for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        previous_handlers[signum] = signal.signal(signum, lambda _signal, _frame: shutdown.set())
    try:
        with registry.lock_registry(timeout=ready_timeout + 5):
            document = registry.load_registry()
            proxy = require_ready_portless_proxy(portless_directory)
            routes = read_portless_routes(portless_directory)
            existing = document['records'].get(key)
            if existing and existing['status'] not in ('stopped', 'released'):
                output = registry.reusable_record(existing, binding, app, command, owner)
                registry.save_registry(document)
                send_response(output)
                return 0
            route = next((value for value in routes if value['hostname'] == app['hostname']), None)
            if route:
                record = registry.reuse_untracked_route(route, binding, app, command, owner, portless_directory, proxy)
                document['records'][key] = record
                registry.save_registry(document)
                send_response(registry.public_server_record(record, 'reused-untracked'))
                return 0
            if len(document['records']) >= MAX_SERVERS and key not in document['records']:
                raise WorkflowError('SERVER_REGISTRY_FULL', 'Server registry reached 128 records. Review stopped records manually.')
            record = registry.new_server_record(binding, app, command, owner, portless_directory,
                                                managed=True, supervisor=supervisor, process=None, proxy=proxy)
            generation = record['generation']
            document['records'][key] = record
            registry.save_registry(document)
            owns_resource = True
            executable = shutil.which('portless')
            if executable is None:
                raise WorkflowError('PORTLESS_UNAVAILABLE', 'Portless is missing. No app was launched.')
            launch_arguments = [executable, 'run', '--name', app['base_name'], '--', *command]
            environment = dict(os.environ, PORTLESS_STATE_DIR=str(portless_directory))
            for key_name in ('PORT', 'PORTLESS_APP_PORT', 'PORTLESS_TAILSCALE', 'PORTLESS_FUNNEL', 'PORTLESS_NGROK'):
                if environment.get(key_name):
                    raise WorkflowError('SERVER_ENVIRONMENT', 'Unset app-port or sharing overrides before managed startup.')
            if environment.get('PORTLESS') == '0':
                raise WorkflowError('SERVER_ENVIRONMENT', 'Managed startup requires Portless rather than bypass mode.')
            # Application output is discarded. Existing app-specific evidence/logs should be linked separately.
            command_process = subprocess.Popen(launch_arguments, cwd=app['app_directory'], env=environment,
                                               stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                               stderr=subprocess.DEVNULL, start_new_session=True, close_fds=True)
            process = read_linux_process(command_process.pid)
            if process is None:
                raise WorkflowError('SERVER_LAUNCH_FAILED', 'The Portless launcher exited before its identity could be recorded.')
            launcher = process.identity
            known[launcher.pid] = launcher
            record['launcher'] = launcher.to_json()
            registry.save_registry(document)
            deadline = time.monotonic() + ready_timeout
            while not shutdown.is_set() and time.monotonic() < deadline:
                snapshots = supervise_owned_tree(supervisor, known)
                record['children'] = [value.to_json() for value in known.values()]
                record['process_groups'] = sorted({value.group_pid for value in snapshots.values() if value.identity != supervisor})
                registry.save_registry(document)
                if command_process.poll() is not None:
                    raise WorkflowError('SERVER_LAUNCH_FAILED', 'The app command exited before a named listener became ready.')
                # EOF means the requesting agent command disappeared during acquisition.
                try:
                    if control.recv(1, socket.MSG_PEEK) == b'':
                        raise WorkflowError('SERVER_LAUNCH_INTERRUPTED', 'The start request ended before acquisition completed.')
                except BlockingIOError:
                    pass
                routes = read_portless_routes(portless_directory)
                route = next((value for value in routes if value['hostname'] == app['hostname']), None)
                if route:
                    route_owner = snapshots.get(route['pid'])
                    listeners, _ = identify_listener_processes(route['port'], snapshots)
                    if route_owner and route_owner.identity.uid == os.getuid() and listeners:
                        record['status'], record['port'] = 'running', route['port']
                        record['portless_process'] = route_owner.identity.to_json()
                        registry.save_registry(document)
                        send_response(registry.public_server_record(record, 'started'))
                        break
                shutdown.wait(0.05)
            else:
                raise WorkflowError('SERVER_READY_TIMEOUT', 'No verified named app listener became ready before the bounded deadline.')
        # Owner liveness and child links are checked here, not in per-tool hooks or global scans.
        response.close()
        control.close()
        next_record = 0.0
        while not shutdown.is_set():
            snapshots = supervise_owned_tree(supervisor, known)
            if command_process.poll() is not None:
                shutdown.set()
                break
            if time.monotonic() >= next_record:
                with registry.lock_registry():
                    document = registry.load_registry()
                    record = document['records'].get(key)
                    if record is None or record['generation'] != generation:
                        raise WorkflowError('SERVER_STATE_CHANGED', 'Managed ownership changed unexpectedly. Cleanup requires inspection.')
                    retain_live_server_owners(record)
                    record['children'] = [value.to_json() for value in known.values()
                                          if process_identity_alive(value)]
                    record['process_groups'] = sorted({value.group_pid for value in snapshots.values() if value.identity != supervisor})
                    if record['status'] == 'stop-requested' or (not record['owners'] and not record['keep']):
                        shutdown.set()
                    registry.save_registry(document)
                next_record = time.monotonic() + 1
            reap_owned_children()
            shutdown.wait(0.2)
        return 0
    except WorkflowError as exc:
        if not response_sent:
            try:
                send_response({'error': exc.code, 'message': str(exc)})
            except OSError:
                pass
        return 1
    except (OSError, ValueError):
        if not response_sent:
            try:
                send_response({'error': 'SERVER_SUPERVISOR_ERROR', 'message': 'Managed acquisition failed. Only owned subprocesses are eligible for cleanup.'})
            except OSError:
                pass
        return 1
    finally:
        if owns_resource:
            clean = stop_owned_tree(supervisor, known, launcher, grace=grace)
            with registry.lock_registry():
                document = registry.load_registry()
                record = document['records'].get(key)
                if record and record['generation'] == generation:
                    record['status'] = 'stopped' if clean else 'cleanup-incomplete'
                    record['children'] = [value.to_json() for value in known.values() if process_identity_alive(value)]
                    registry.save_registry(document)
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)
        response.close()
        control.close()
