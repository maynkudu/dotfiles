import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.workflow.linux_process import ProcessIdentity, process_identity_alive, read_linux_process, signal_verified_process
from tools.workflow.private_state import WorkflowError
from tools.workflow.server_registry import ServerRegistry
from tools.workflow.workspace_context import bind_git_workspace

SERVER = ROOT / 'bin/agent-server'
FIXTURES = ROOT / 'tests/fixtures/workflow_server'


@unittest.skipUnless(sys.platform == 'linux' and hasattr(os, 'pidfd_open'), 'Linux pidfd supervision required')
class ServerLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / 'app'
        self.repo.mkdir()
        subprocess.run(['git', 'init', '--initial-branch=main', str(self.repo)], capture_output=True, check=True)
        (self.repo / 'portless.json').write_text('{"name":"fixture-app"}\n')
        self.state = self.root / 'state'
        self.portless = self.root / 'portless'
        self.portless.mkdir()
        self.binaries = self.root / 'bin'
        self.binaries.mkdir()
        shutil.copyfile(FIXTURES / 'fake_portless.py', self.binaries / 'portless')
        (self.binaries / 'portless').chmod(0o755)
        self.proxy = socket.socket()
        self.proxy.bind(('127.0.0.1', 0))  # Disposable test fixture only, never a production port selection.
        self.proxy.listen()
        self.addCleanup(self.proxy.close)
        self.port = self.reserve_fixture_port()
        (self.portless / 'proxy.pid').write_text(str(os.getpid()))
        (self.portless / 'proxy.port').write_text(str(self.proxy.getsockname()[1]))
        (self.portless / 'proxy.tls').write_text('1')
        (self.portless / 'routes.json').write_text('[]')
        self.environment = dict(os.environ, PATH=str(self.binaries) + os.pathsep + os.environ['PATH'],
                                FIXTURE_APP_PORT=str(self.port), FIXTURE_TREE_FILE=str(self.root / 'tree.json'))
        for key in ('PORT', 'PORTLESS_APP_PORT', 'PORTLESS', 'PORTLESS_TAILSCALE', 'PORTLESS_FUNNEL', 'PORTLESS_NGROK'):
            self.environment.pop(key, None)
        self.command = [sys.executable, str(FIXTURES / 'child_tree.py')]
        self.addCleanup(self.cleanup_fixture_processes)

    def reserve_fixture_port(self):
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            return listener.getsockname()[1]

    def arguments(self, session='fixture-a', owner=None):
        return [sys.executable, str(SERVER), '--worktree', str(self.repo), '--session', session,
                '--owner-pid', str(owner or os.getpid()), '--state-dir', str(self.state),
                '--portless-state-dir', str(self.portless)]

    def invoke(self, action, session='fixture-a', *extra, check=True, environment=None):
        result = subprocess.run([*self.arguments(session), action, *extra], capture_output=True, text=True,
                                env=environment or self.environment, timeout=15)
        if check:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        return result

    def start(self, session='fixture-a', environment=None):
        return self.invoke('start', session, '--app-dir', str(self.repo), '--ready-timeout', '3', '--grace', '0.2',
                           '--', *self.command, environment=environment)

    def records(self):
        return ServerRegistry(self.state).load_registry()['records']

    def wait_condition(self, predicate, *, timeout=8):
        deadline = time.monotonic() + timeout
        wake = threading.Event()
        while time.monotonic() < deadline:
            if predicate():
                return
            wake.wait(0.025)
        self.fail('Fixture condition did not become true before its bounded deadline')

    def cleanup_fixture_processes(self):
        # Every test subprocess we own is cleaned even when an assertion fails.
        try:
            records = list(self.records().values())
        except WorkflowError:
            records = []
        for record in records:
            if record.get('supervisor'):
                identity = ProcessIdentity.from_json(record['supervisor'])
                signal_verified_process(identity, signal.SIGTERM)
        wake = threading.Event()
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline and any(record.get('supervisor') and process_identity_alive(
                ProcessIdentity.from_json(record['supervisor'])) for record in records):
            wake.wait(0.05)
        for record in records:
            for value in record.get('children', []):
                signal_verified_process(ProcessIdentity.from_json(value), signal.SIGKILL)
            if record.get('supervisor'):
                signal_verified_process(ProcessIdentity.from_json(record['supervisor']), signal.SIGKILL)
        tree = self.root / 'tree.json'
        if tree.exists():
            for pid in json.loads(tree.read_text()).values():
                current = read_linux_process(pid)
                if current:
                    signal_verified_process(current.identity, signal.SIGKILL)

    def test_reuse_shared_owner_last_release_stops_detached_children(self):
        first = self.start()
        self.assertEqual(first['action'], 'started')
        self.wait_condition(lambda: (self.root / 'tree.json').exists())
        tree = json.loads((self.root / 'tree.json').read_text())
        child_identity = read_linux_process(tree['child']).identity
        second = self.start('fixture-b')
        self.assertEqual(second['action'], 'reused')
        self.assertEqual(len((self.portless / 'starts.txt').read_text().splitlines()), 1)
        self.assertEqual(set(second['owners']), {'fixture-a', 'fixture-b'})
        released = self.invoke('release', 'fixture-a', '--app-dir', str(self.repo))
        self.assertEqual(released['status'], 'running')
        self.assertTrue(process_identity_alive(child_identity))
        final = self.invoke('release', 'fixture-b', '--app-dir', str(self.repo))
        self.assertEqual(final['status'], 'stopped')
        self.assertFalse(process_identity_alive(child_identity))
        self.assertEqual(json.loads((self.portless / 'routes.json').read_text()), [])

    def test_concurrent_start_has_one_launcher_and_two_owners(self):
        processes = [subprocess.Popen([*self.arguments(session), 'start', '--app-dir', str(self.repo),
                                       '--ready-timeout', '3', '--grace', '0.2', '--', *self.command],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=self.environment)
                     for session in ('fixture-a', 'fixture-b')]
        try:
            results = []
            for process in processes:
                stdout, stderr = process.communicate(timeout=12)
                self.assertEqual(process.returncode, 0, stderr)
                results.append(json.loads(stdout))
            self.assertEqual({value['action'] for value in results}, {'started', 'reused'})
            self.assertEqual(len((self.portless / 'starts.txt').read_text().splitlines()), 1)
            self.assertEqual(len(next(iter(self.records().values()))['owners']), 2)
        finally:
            for process in processes:
                if process.poll() is None:
                    process.terminate()
                    process.communicate(timeout=5)
        self.invoke('finalize', 'fixture-a')
        self.invoke('finalize', 'fixture-b')

    def test_explicit_keep_preserves_then_owner_clears_it(self):
        self.start()
        kept = self.invoke('release', 'fixture-a', '--app-dir', str(self.repo), '--keep')
        self.assertTrue(kept['keep'])
        supervisor = ProcessIdentity.from_json(kept['supervisor'])
        self.assertTrue(process_identity_alive(supervisor))
        self.invoke('recover', 'fixture-a')
        self.assertTrue(process_identity_alive(supervisor))
        self.start('fixture-b')
        self.invoke('unkeep', 'fixture-b', '--app-dir', str(self.repo))
        final = self.invoke('finalize', 'fixture-b')
        self.assertEqual(final['records'][0]['status'], 'stopped')

    def test_current_owner_only_and_pid_reuse_protects_unrelated(self):
        self.start()
        wrong = self.invoke('release', 'fixture-b', '--app-dir', str(self.repo), check=False)
        self.assertNotEqual(wrong.returncode, 0)
        self.assertIn('current recorded', wrong.stderr)
        unrelated = subprocess.Popen([sys.executable, '-c', 'import signal; signal.pause()'])
        try:
            identity = read_linux_process(unrelated.pid).identity
            reused = ProcessIdentity(identity.pid, identity.start_ticks + 1, identity.boot_id, identity.uid)
            self.assertFalse(signal_verified_process(reused, signal.SIGKILL))
            self.assertIsNone(unrelated.poll())
            self.invoke('finalize')
            self.assertIsNone(unrelated.poll())
        finally:
            unrelated.terminate()
            unrelated.wait(timeout=3)

    def test_failed_start_and_unknown_alias_do_not_overwrite_routes(self):
        failed = self.invoke('start', 'fixture-a', '--app-dir', str(self.repo), '--ready-timeout', '1', '--grace', '0.2',
                             '--', *self.command, check=False,
                             environment=self.environment | {'FIXTURE_PORTLESS_BEHAVIOR': 'fail'})
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('LAUNCH_FAILED', failed.stderr)
        self.wait_condition(lambda: next(iter(self.records().values()))['status'] == 'stopped')
        old = [{'hostname': 'fixture-app.localhost', 'port': self.port, 'pid': 0}]
        (self.portless / 'routes.json').write_text(json.dumps(old))
        conflict = self.invoke('start', 'fixture-a', '--app-dir', str(self.repo), '--ready-timeout', '1', '--grace', '0.2',
                               '--', *self.command, check=False)
        self.assertNotEqual(conflict.returncode, 0)
        self.assertIn('UNTRACKED_ALIAS', conflict.stderr)
        self.assertEqual(json.loads((self.portless / 'routes.json').read_text()), old)

    def test_interrupted_launch_cleans_owned_children(self):
        process = subprocess.Popen([*self.arguments(), 'start', '--app-dir', str(self.repo), '--ready-timeout', '5',
                                    '--grace', '0.2', '--', *self.command], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, env=self.environment | {'FIXTURE_PORTLESS_BEHAVIOR': 'slow'})
        try:
            self.wait_condition(lambda: (self.root / 'tree.json').exists())
            tree = json.loads((self.root / 'tree.json').read_text())
            identities = [read_linux_process(pid).identity for pid in tree.values()]
            process.terminate()
            process.communicate(timeout=5)
            self.wait_condition(lambda: all(not process_identity_alive(value) for value in identities))
            self.wait_condition(lambda: next(iter(self.records().values()))['status'] == 'stopped')
        finally:
            if process.poll() is None:
                process.terminate()
                process.communicate(timeout=5)

    def test_verified_owner_death_triggers_scoped_cleanup(self):
        script = self.root / 'owner.py'
        script.write_text('import subprocess, os, sys, json, signal\n'
                          'args=json.loads(sys.argv[1])\n'
                          'subprocess.run(args+["--owner-pid",str(os.getpid()),"start","--app-dir",os.getcwd(),'
                          '"--ready-timeout","3","--grace","0.2","--"]+json.loads(sys.argv[2]),check=True)\n'
                          'signal.pause()\n')
        base = [sys.executable, str(SERVER), '--worktree', str(self.repo), '--session', 'dead-owner',
                '--state-dir', str(self.state), '--portless-state-dir', str(self.portless)]
        owner = subprocess.Popen([sys.executable, str(script), json.dumps(base), json.dumps(self.command)],
                                 cwd=self.repo, env=self.environment, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            self.wait_condition(lambda: self.records() and next(iter(self.records().values()))['status'] == 'running')
            supervisor = ProcessIdentity.from_json(next(iter(self.records().values()))['supervisor'])
            owner.terminate()
            owner.wait(timeout=5)
            self.wait_condition(lambda: not process_identity_alive(supervisor))
            self.assertEqual(next(iter(self.records().values()))['status'], 'stopped')
        finally:
            if owner.poll() is None:
                owner.terminate()
                owner.wait(timeout=5)

    def test_inventory_read_only_no_argv_and_unsupported_platform(self):
        self.start()
        raw = (self.portless / 'routes.json').read_bytes()
        inventory = self.invoke('inventory')
        self.assertEqual(inventory['mode'], 'read-only')
        self.assertTrue(inventory['routes'][0]['current_listener'])
        self.assertGreater(inventory['routes'][0]['route_tree_rss_bytes'], 0)
        self.assertNotIn('command', json.dumps(inventory))
        self.assertFalse(inventory['routes'][0]['cleanup_eligible'])
        self.assertEqual((self.portless / 'routes.json').read_bytes(), raw)
        with patch('tools.workflow.linux_process.sys.platform', 'darwin'):
            with self.assertRaisesRegex(WorkflowError, 'No process was changed'):
                read_linux_process(os.getpid())
        self.invoke('finalize')


if __name__ == '__main__':
    unittest.main()
