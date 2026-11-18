"""Locked server ownership records. Untracked servers never become cleanup-owned."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import signal
import time
import uuid

from .linux_process import (ProcessIdentity, current_ancestor_identity, identify_listener_processes,
                            process_identity_alive, process_working_directory, read_linux_process,
                            read_process_descendants, signal_verified_process)
from .portless_state import named_portless_url, read_portless_routes
from .private_state import (WorkflowError, ensure_private_directory, private_state_lock,
                            read_private_json, write_private_json)
from .workspace_context import WorkspaceBinding, validate_context_text

SCHEMA = 'dotfiles.servers.v1'
MAX_SERVERS = 128
MAX_OWNERS = 64


def server_record_key(hostname: str, portless_directory: Path) -> str:
    """One lock namespace covers every worktree that could compete for this route."""
    return hashlib.sha256((str(portless_directory) + '\0' + hostname).encode()).hexdigest()


def server_command_digest(command: list[str]) -> str:
    """Store command identity only, never argv that might contain credentials."""
    return hashlib.sha256(json.dumps(command, separators=(',', ':')).encode()).hexdigest()


def validate_server_command(command: list[str]) -> None:
    """Keep Portless in charge of port assignment and reject obvious secret arguments."""
    if not command or len(command) > 128:
        raise WorkflowError('SERVER_COMMAND', 'Provide one app command after -- with at most 128 arguments.')
    for argument in command:
        validate_context_text(argument, 'Command argument', 4096)
        if (argument in ('--force', '--port', '-p', '--app-port', '--tailscale', '--funnel', '--ngrok')
                or argument.startswith(('--port=', '--app-port=', 'PORT=', 'PORTLESS_APP_PORT='))):
            raise WorkflowError('SERVER_COMMAND', 'Managed startup cannot force routes, set ports, or expose the app externally.')
    if Path(command[0]).name in ('portless', 'env'):
        raise WorkflowError('SERVER_COMMAND', 'Provide the app command itself, not another Portless or env wrapper.')


def server_owner_record(binding: WorkspaceBinding, owner_pid: int) -> dict:
    """Use a stable harness/ancestor identity, not a transient shell or a timestamp lease."""
    return {'session': binding.session, 'worktree': binding.worktree,
            'process': current_ancestor_identity(owner_pid).to_json(),
            'acquired_at': datetime.now(timezone.utc).isoformat()}


def same_server_owner(left: dict, right: dict) -> bool:
    return all(left[key] == right[key] for key in ('session', 'worktree', 'process'))


def retain_live_server_owners(record: dict) -> list[dict]:
    """Remove owners only after exact process-identity death, never ordinary assistant idle."""
    record['owners'] = [owner for owner in record['owners']
                        if process_identity_alive(ProcessIdentity.from_json(owner['process']))]
    return record['owners']


class ServerRegistry:
    """Persist ownership and child start identities under one owner-only global lock."""

    def __init__(self, root: Path):
        self.root = root
        self.directory = root / 'servers'
        self.path = self.directory / 'registry.json'
        self.lock = self.directory / 'registry.lock'

    def load_registry(self) -> dict:
        if not ensure_private_directory(self.root, create=False):
            return {'schema': SCHEMA, 'records': {}}
        if not ensure_private_directory(self.directory, create=False):
            return {'schema': SCHEMA, 'records': {}}
        document = read_private_json(self.path)
        if document is None:
            return {'schema': SCHEMA, 'records': {}}
        if (not isinstance(document, dict) or set(document) != {'schema', 'records'}
                or document['schema'] != SCHEMA or not isinstance(document['records'], dict)
                or len(document['records']) > MAX_SERVERS):
            raise WorkflowError('SERVER_STATE_INVALID', 'Server registry is invalid. No process was changed.')
        for key, record in document['records'].items():
            self.validate_server_record(key, record)
        return document

    def validate_server_record(self, key: str, record: object) -> None:
        """Malformed ownership state protects processes instead of granting cleanup permission."""
        required = {'generation', 'hostname', 'portless_directory', 'repository', 'worktree', 'app_directory',
                    'command_digest', 'managed', 'status', 'owners', 'keep', 'supervisor', 'launcher',
                    'portless_process', 'children', 'process_groups', 'url', 'created_at', 'port'}
        if not isinstance(record, dict) or set(record) != required:
            raise WorkflowError('SERVER_STATE_INVALID', 'Server record fields are invalid.')
        for field in ('generation', 'hostname', 'repository', 'worktree', 'app_directory', 'portless_directory', 'url', 'created_at'):
            validate_context_text(record[field], 'Server metadata', 4096)
        if key != server_record_key(record['hostname'], Path(record['portless_directory'])):
            raise WorkflowError('SERVER_STATE_INVALID', 'Server route lock identity is invalid.')
        if (record['status'] not in ('starting', 'running', 'stop-requested', 'stopped', 'released', 'orphaned', 'cleanup-incomplete')
                or type(record['managed']) is not bool or type(record['keep']) is not bool
                or not isinstance(record['owners'], list) or len(record['owners']) > MAX_OWNERS
                or not isinstance(record['children'], list) or len(record['children']) > 512
                or not isinstance(record['process_groups'], list)
                or type(record['port']) is not int or not 0 <= record['port'] < 65536):
            raise WorkflowError('SERVER_STATE_INVALID', 'Server ownership or lifecycle metadata is invalid.')
        for owner in record['owners']:
            if not isinstance(owner, dict) or set(owner) != {'session', 'worktree', 'process', 'acquired_at'}:
                raise WorkflowError('SERVER_STATE_INVALID', 'Server owner metadata is invalid.')
            ProcessIdentity.from_json(owner['process'])
            if owner['worktree'] != record['worktree']:
                raise WorkflowError('SERVER_STATE_INVALID', 'Server owner belongs to a different worktree.')
        for field in ('supervisor', 'launcher', 'portless_process'):
            if record[field] is not None:
                ProcessIdentity.from_json(record[field])
        for child in record['children']:
            ProcessIdentity.from_json(child)
        if record['managed'] and record['supervisor'] is None:
            raise WorkflowError('SERVER_STATE_INVALID', 'Cleanup-owned servers require a recorded supervisor identity.')

    def save_registry(self, document: dict) -> None:
        ensure_private_directory(self.root)
        write_private_json(self.path, document)

    def lock_registry(self, *, timeout: float = 5):
        ensure_private_directory(self.root)
        return private_state_lock(self.lock, timeout=timeout)

    def assert_same_app(self, record: dict, binding: WorkspaceBinding, app: dict) -> None:
        if any(record[field] != value for field, value in (
                ('repository', binding.repository), ('worktree', binding.worktree), ('app_directory', app['app_directory']))):
            raise WorkflowError('SERVER_SCOPE_CONFLICT', 'The named route belongs to a different exact app/worktree. It remains untouched.')

    def add_server_owner(self, record: dict, owner: dict) -> None:
        if not any(same_server_owner(value, owner) for value in record['owners']):
            if len(record['owners']) >= MAX_OWNERS:
                raise WorkflowError('SERVER_OWNERS_FULL', 'This app reached 64 active owners.')
            record['owners'].append(owner)

    def reusable_record(self, record: dict, binding: WorkspaceBinding, app: dict, command: list[str], owner: dict) -> dict:
        self.assert_same_app(record, binding, app)
        if record['command_digest'] != server_command_digest(command):
            raise WorkflowError('SERVER_COMMAND_CONFLICT', 'The tracked app uses a different launch command. Verify it rather than starting a duplicate.')
        retain_live_server_owners(record)
        if record['status'] != 'running':
            raise WorkflowError('SERVER_NOT_READY', 'The tracked app is not running. Inspect status or recover dead owners before starting again.')
        if record['managed'] and not process_identity_alive(ProcessIdentity.from_json(record['supervisor'])):
            raise WorkflowError('SERVER_SUPERVISOR_DEAD', 'The supervisor is dead. Inspect and recover only recorded resources before reuse.')
        identity = record['portless_process']
        if identity is None or not process_identity_alive(ProcessIdentity.from_json(identity)):
            raise WorkflowError('SERVER_NOT_READY', 'The recorded app process is no longer live.')
        routes = read_portless_routes(Path(record['portless_directory']))
        route = next((value for value in routes if value['hostname'] == record['hostname']), None)
        if not route or route['port'] != record['port']:
            raise WorkflowError('SERVER_NOT_READY', 'The named route changed. Recheck the actual app before reuse.')
        tree = read_process_descendants(ProcessIdentity.from_json(identity))
        listeners, _ = identify_listener_processes(route['port'], tree)
        if not listeners:
            raise WorkflowError('SERVER_NOT_READY', 'The named route has no verified listener in the recorded app tree.')
        self.add_server_owner(record, owner)
        return self.public_server_record(record, 'reused')

    def reuse_untracked_route(self, route: dict, binding: WorkspaceBinding, app: dict, command: list[str],
                             owner: dict, directory: Path, proxy: dict) -> dict:
        """Verify exact cwd and listener for reuse; never authorize killing an old unknown server."""
        if route['pid'] <= 1:
            raise WorkflowError('SERVER_UNTRACKED_ALIAS', 'An existing alias occupies this name. Inspect it; this helper neither replaces nor cleans it.')
        process = read_linux_process(route['pid'])
        if process is None or process_working_directory(process.identity) != Path(app['app_directory']):
            raise WorkflowError('SERVER_UNTRACKED_CONFLICT', 'The existing route cannot be verified as this exact app. It remains untouched.')
        tree = read_process_descendants(process.identity)
        listeners, _ = identify_listener_processes(route['port'], tree)
        if not listeners:
            raise WorkflowError('SERVER_UNTRACKED_CONFLICT', 'The existing route has no verified current app listener. It remains untouched.')
        return self.new_server_record(binding, app, command, owner, directory, managed=False,
                                      supervisor=None, process=process.identity, proxy=proxy, port=route['port'])

    def new_server_record(self, binding: WorkspaceBinding, app: dict, command: list[str], owner: dict,
                          directory: Path, *, managed: bool, supervisor: ProcessIdentity | None,
                          process: ProcessIdentity | None, proxy: dict, port: int = 0) -> dict:
        return {'generation': uuid.uuid4().hex, 'hostname': app['hostname'], 'portless_directory': str(directory),
                'repository': binding.repository, 'worktree': binding.worktree, 'app_directory': app['app_directory'],
                'command_digest': server_command_digest(command), 'managed': managed,
                'status': 'starting' if managed else 'running', 'owners': [owner], 'keep': False,
                'supervisor': supervisor.to_json() if supervisor else None, 'launcher': None,
                'portless_process': process.to_json() if process else None, 'children': [], 'process_groups': [],
                'url': named_portless_url(app['hostname'], proxy), 'created_at': datetime.now(timezone.utc).isoformat(),
                'port': port}

    def public_server_record(self, record: dict, action: str) -> dict:
        read_only_transport = record['status'] == 'running' and record['portless_process'] is not None and process_identity_alive(ProcessIdentity.from_json(record['portless_process']))
        return {'action': action, 'url': record['url'], 'status': record['status'], 'managed': record['managed'],
                'worktree': record['worktree'], 'app_directory': record['app_directory'],
                'owners': [owner['session'] for owner in record['owners']], 'keep': record['keep'],
                'supervisor': record['supervisor'], 'portless_process': record['portless_process'],
                'process_groups': record['process_groups'], 'transport_verified': read_only_transport,
                'application_verified': False}

    def scoped_server_status(self, binding: WorkspaceBinding) -> dict:
        records = [self.public_server_record(record, 'status') for record in self.load_registry()['records'].values()
                   if record['repository'] == binding.repository and record['worktree'] == binding.worktree]
        return {'mode': 'read-only', 'worktree': binding.worktree, 'records': records,
                'warning': 'Saved status needs a current listener check. Ordinary assistant idle never releases owners.'}

    def select_server_record(self, document: dict, binding: WorkspaceBinding, app: dict, directory: Path) -> tuple[str, dict]:
        key = server_record_key(app['hostname'], directory)
        record = document['records'].get(key)
        if record is None:
            raise WorkflowError('SERVER_MISSING', 'No tracked record exists for this exact app/worktree.')
        self.assert_same_app(record, binding, app)
        return key, record

    def release_server_owner(self, binding: WorkspaceBinding, app: dict, directory: Path,
                             owner: dict, *, keep: bool = False, wait: bool = True) -> dict:
        supervisor = None
        with self.lock_registry():
            document = self.load_registry()
            key, record = self.select_server_record(document, binding, app, directory)
            if not any(same_server_owner(value, owner) for value in record['owners']):
                raise WorkflowError('SERVER_OWNER', 'Only the current recorded session/process owner can release this app.')
            if keep:
                record['keep'] = True
            record['owners'] = [value for value in record['owners'] if not same_server_owner(value, owner)]
            retain_live_server_owners(record)
            if not record['owners'] and not record['keep']:
                if record['managed'] and record['status'] not in ('stopped', 'released'):
                    record['status'] = 'stop-requested'
                    supervisor = ProcessIdentity.from_json(record['supervisor'])
                elif not record['managed']:
                    record['status'] = 'released'
            self.save_registry(document)
            output = self.public_server_record(record, 'released-owner')
        if supervisor:
            signal_verified_process(supervisor, signal.SIGTERM)
            if wait:
                output = self.wait_server_shutdown(key, supervisor)
        return output

    def set_server_keep(self, binding: WorkspaceBinding, app: dict, directory: Path,
                        owner: dict, *, keep: bool) -> dict:
        with self.lock_registry():
            document = self.load_registry()
            _, record = self.select_server_record(document, binding, app, directory)
            if not any(same_server_owner(value, owner) for value in record['owners']):
                raise WorkflowError('SERVER_OWNER', 'Only a current owner can change explicit keep behavior.')
            record['keep'] = keep
            self.save_registry(document)
            return self.public_server_record(record, 'kept' if keep else 'keep-cleared')

    def wait_server_shutdown(self, key: str, supervisor: ProcessIdentity, *, timeout: float = 10) -> dict:
        deadline = time.monotonic() + timeout
        while process_identity_alive(supervisor) and time.monotonic() < deadline:
            time.sleep(0.05)
        record = self.load_registry()['records'][key]
        output = self.public_server_record(record, 'stopped' if record['status'] == 'stopped' else 'cleanup-pending')
        if record['status'] != 'stopped':
            output['warning'] = 'Cleanup is incomplete. Run scoped recover; unrelated processes remain protected.'
        return output

    def recover_dead_server_owners(self, binding: WorkspaceBinding, *, grace: float = 3) -> dict:
        """Explicitly recover recorded resources after owner death, never untracked route history."""
        requests = []
        outcomes = []
        with self.lock_registry():
            document = self.load_registry()
            for key, record in document['records'].items():
                if record['repository'] != binding.repository or record['worktree'] != binding.worktree:
                    continue
                before = len(record['owners'])
                retain_live_server_owners(record)
                outcome = {'hostname': record['hostname'], 'dead_owners_removed': before - len(record['owners'])}
                if record['owners'] or record['keep']:
                    outcome['action'] = 'preserved-active-or-kept'
                elif not record['managed']:
                    record['status'] = 'released'
                    outcome['action'] = 'untracked-process-preserved'
                elif record['status'] == 'stopped':
                    outcome['action'] = 'already-stopped'
                else:
                    record['status'] = 'stop-requested'
                    supervisor = ProcessIdentity.from_json(record['supervisor'])
                    if process_identity_alive(supervisor):
                        requests.append((key, supervisor, []))
                    else:
                        # A reused supervisor PID is never signaled. Only matching recorded children are eligible.
                        identities = [ProcessIdentity.from_json(value) for value in record['children']]
                        if record['portless_process']:
                            identities.append(ProcessIdentity.from_json(record['portless_process']))
                        requests.append((key, None, identities))
                    outcome['action'] = 'cleanup-requested'
                outcomes.append(outcome)
            self.save_registry(document)
        for key, supervisor, children in requests:
            if supervisor:
                signal_verified_process(supervisor, signal.SIGTERM)
                self.wait_server_shutdown(key, supervisor)
                continue
            cleanup_verified_children(children, grace=grace)
            with self.lock_registry():
                document = self.load_registry()
                record = document['records'][key]
                remaining = [identity.to_json() for identity in children if process_identity_alive(identity)]
                record['children'] = remaining
                record['status'] = 'cleanup-incomplete' if remaining else 'stopped'
                self.save_registry(document)
        return {'worktree': binding.worktree, 'records': outcomes,
                'warning': 'Recovery used exact recorded process starts only. Untracked servers and routes were not changed.'}


def cleanup_verified_children(children: list[ProcessIdentity], *, grace: float = 3) -> None:
    """Gracefully stop identity-pinned owned children, then signal only verified survivors."""
    for child in children:
        signal_verified_process(child, signal.SIGTERM)
    deadline = time.monotonic() + grace
    while any(process_identity_alive(value) for value in children) and time.monotonic() < deadline:
        time.sleep(0.05)
    for child in children:
        if process_identity_alive(child):
            signal_verified_process(child, signal.SIGKILL)
