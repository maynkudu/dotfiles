import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.workflow.workflow_eval import run_workflow_fixtures
from tools.workflow.workflow_health import workflow_health_report
from tools.workflow.workflow_install import install_workflow_links


class WorkflowIntegrationTests(unittest.TestCase):
    def test_repository_contracts_and_skills(self):
        report = run_workflow_fixtures(ROOT / 'tests/fixtures/workflow')
        self.assertEqual(report['passed'], report['total'])
        self.assertEqual(report['total'], 14)
        health = workflow_health_report(ROOT, Path.home(), ['codex', 'claude', 'pi'], repo_only=True)
        self.assertEqual(health['findings'], [])

    def test_installation_preserves_external_links_and_dry_run(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            commands = home / '.local/bin'
            actions = install_workflow_links(ROOT, home, ['pi'], dry_run=True)
            self.assertTrue(actions)
            self.assertFalse(commands.exists())
            commands.mkdir(parents=True)
            existing = commands / 'agent-server'
            existing.write_text('user-owned command')
            install_workflow_links(ROOT, home, ['pi'])
            self.assertEqual(existing.read_text(), 'user-owned command')
            self.assertEqual((commands / 'agent-checkpoint').resolve(), ROOT / 'bin/agent-checkpoint')
            before = (home / '.pi/agent/skills/private-checkpoint').lstat().st_mtime_ns
            install_workflow_links(ROOT, home, ['pi'])
            self.assertEqual((home / '.pi/agent/skills/private-checkpoint').lstat().st_mtime_ns, before)

    def test_pi_lifecycle_uses_real_shutdown_not_turn_end(self):
        script = '''
import extension from './skills/hooks/pi-workflow-lifecycle.ts';
import assert from 'node:assert/strict';
const handlers = new Map();
const commands = new Map();
const calls = [];
const pi = {
  on: (name, handler) => handlers.set(name, handler),
  registerCommand: (name, command) => commands.set(name, command),
  exec: async (command, args, options) => { calls.push({ command, args, options }); return { code: 0, stdout: '', stderr: '' }; },
  sendMessage: () => {},
};
const ctx = { cwd: process.cwd(), sessionManager: { getSessionId: () => 'fixture-session' }, hasUI: false };
extension(pi);
assert(!handlers.has('turn_end'));
assert(!handlers.has('agent_end'));
await handlers.get('session_start')({ reason: 'startup' }, ctx);
assert.equal(calls.length, 2);
assert(calls.every(call => call.options.timeout === 5000));
calls.length = 0;
await handlers.get('session_shutdown')({ reason: 'reload' }, ctx);
assert.equal(calls.length, 0);
await handlers.get('session_shutdown')({ reason: 'new' }, ctx);
assert.equal(calls.length, 1);
assert(calls[0].args.includes('fixture-session'));
assert(calls[0].args.includes(String(process.pid)));
assert(calls[0].args.includes('finalize'));
assert(calls[0].args.includes('--no-wait'));
calls.length = 0;
await commands.get('workflow-finalize').handler('keep', ctx);
assert(calls[0].args.includes('--keep'));
console.log('Pi lifecycle contract passed');
'''
        result = subprocess.run(['/usr/bin/node', '--input-type=module', '-e', script], cwd=ROOT,
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_startup_hooks_have_five_second_bounds_and_preserve_unrelated(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            settings = home / '.claude/settings.json'
            settings.parent.mkdir(parents=True)
            settings.write_text(json.dumps({'hooks': {'SessionStart': [{'hooks': [{'type': 'command', 'command': 'keep-existing'}]}]}}))
            subprocess.run([sys.executable, ROOT / 'skills/bin/install', '--home', home, '--agents', 'claude', 'pi'],
                           capture_output=True, text=True, check=True, timeout=15)
            data = json.loads(settings.read_text())
            handlers = [handler for group in data['hooks']['SessionStart'] for handler in group['hooks']]
            self.assertTrue(any(handler['command'] == 'keep-existing' for handler in handlers))
            for name in ('dotfiles-health', 'agent-workflow-check'):
                handler = next(handler for handler in handlers if name in handler['command'])
                self.assertEqual(handler['timeout'], 5)
            self.assertTrue((home / '.pi/agent/extensions/workflow-lifecycle.ts').is_symlink())


if __name__ == '__main__':
    unittest.main()
