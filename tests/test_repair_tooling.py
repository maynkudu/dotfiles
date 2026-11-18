"""Fixture contracts for managed Node, bounded health checks and registration safety."""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'bin'))
sys.path.insert(0, str(ROOT / 'skills/bin'))
from cli_runtime import install_cli_runtime, managed_cli_command, mcp_registration_status, read_cli_manifest
from config_health import installed_health, read_health_config


class RuntimeRepairTests(unittest.TestCase):
    def fixture_bins(self, home):
        external = home / 'external'
        external.mkdir()
        entry = external / 'agentation-mcp'
        entry.write_text('#!/usr/bin/env node\nconsole.log(process.execPath);\n')
        entry.chmod(0o755)
        node = home / 'fixed-node'
        node.write_text('#!/bin/sh\nif [ "$1" = "-p" ]; then printf \'{"node":"v26.13.1","abi":"147"}\\n\'; else printf "fixed runtime: %s\\n" "$*"; fi\n')
        node.chmod(0o755)
        return external, entry, node

    def test_private_launcher_uses_selected_node_and_preserves_external_binaries(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            external, entry, node = self.fixture_bins(home)
            original = entry.read_bytes()
            with patch('builtins.print'):
                install_cli_runtime(home, ['agentation-mcp'], str(external), node)
            launcher = managed_cli_command(home, 'agentation-mcp')
            result = subprocess.run([launcher, 'server'], text=True, capture_output=True, check=True,
                                    env={**os.environ, 'PATH': '/usr/bin:/bin'})
            self.assertIn('fixed runtime:', result.stdout)
            self.assertIn(str(entry), result.stdout)
            self.assertNotIn('export PATH=', launcher.read_text())
            self.assertEqual(entry.read_bytes(), original)
            self.assertEqual(read_cli_manifest(home)['abi'], '147')
            self.assertEqual((home / '.local/share/dotfiles/cli/runtime-bin/node').resolve(), node)
            self.assertFalse((home / '.node-version').exists())
            before = read_cli_manifest(home)
            with patch('builtins.print'):
                install_cli_runtime(home, ['agentation-mcp'], str(external), None)
            self.assertEqual(before, read_cli_manifest(home))
            self.assertIsNone(managed_cli_command(home, '../../external/agentation-mcp'))

    def test_dry_run_and_external_symlink_conflicts(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            external, _, node = self.fixture_bins(home)
            with patch('builtins.print'):
                install_cli_runtime(home, ['agentation-mcp'], str(external), node, dry_run=True)
            self.assertFalse((home / '.local').exists())
            base = home / '.local/share/dotfiles/cli'
            base.parent.mkdir(parents=True)
            base.symlink_to(external, target_is_directory=True)
            with patch('builtins.print'), self.assertRaises(ValueError):
                install_cli_runtime(home, ['agentation-mcp'], str(external), node)
            self.assertFalse((external / 'runtime.json').exists())

    def test_mcp_absence_is_not_a_parse_error_and_get_is_bounded(self):
        for output, expected in [('No MCP server named argent found.', 'missing'),
                                 ('config.toml: key not found', 'unknown'), ('', 'present')]:
            result = subprocess.CompletedProcess([], int(bool(output)), '', output)
            with patch('subprocess.run', return_value=result) as command:
                self.assertEqual(mcp_registration_status('codex', 'argent', {}), expected)
                self.assertEqual(command.call_args.args[0], ['codex', 'mcp', 'get', 'argent', '--json'])
                self.assertEqual(command.call_args.kwargs['timeout'], 5)
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('codex', 5)):
            self.assertEqual(mcp_registration_status('codex', 'argent', {}), 'unknown')

    def test_setup_adds_only_missing_and_refuses_unknown(self):
        setup = runpy.run_path(str(ROOT / 'bin/setup'))
        with patch.object(sys, 'argv', ['setup', '--mcp', '--dry-run']), patch('builtins.print'), \
                patch.dict(setup['main'].__globals__, {'mcp_registration_status': lambda agent, name, env: 'present'}), \
                patch('subprocess.run') as command:
            setup['main']()
            command.assert_not_called()
        with patch.object(sys, 'argv', ['setup', '--mcp', '--dry-run']), patch('builtins.print'), \
                patch.dict(setup['main'].__globals__, {'mcp_registration_status': lambda agent, name, env: 'missing'}), \
                patch('subprocess.run') as command:
            setup['main']()
            command.assert_not_called()  # dry run is never a registration write
        with patch.object(sys, 'argv', ['setup', '--mcp', '--dry-run']), patch('builtins.print'), \
                patch.dict(setup['main'].__globals__, {'mcp_registration_status': lambda agent, name, env: 'unknown'}), \
                self.assertRaises(SystemExit):
            setup['main']()

    def test_native_rebuild_is_explicit_and_uses_fixed_runtime_without_app_settings(self):
        setup = runpy.run_path(str(ROOT / 'bin/setup'))
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            (home / '.node-version').write_text('24\n')
            (home / '.claude').mkdir()
            (home / '.claude/settings.json').write_text('{"model":"fixture-keep"}')
            def run_command(command, **kwargs):
                if 'rebuild' in command:
                    node_shim = Path(kwargs['env']['PATH'].split(os.pathsep)[0]) / 'node'
                    self.assertEqual(node_shim.resolve(), Path('/usr/bin/node'))
                return subprocess.CompletedProcess(command, 0)
            with patch.object(sys, 'argv', ['setup', '--tools', '--rebuild-native', '--home', str(home)]), \
                    patch('builtins.print'), patch('subprocess.run', side_effect=run_command) as commands, \
                    patch.dict(setup['main'].__globals__, {
                        'install_cli_runtime': lambda *args, **kwargs: None,
                        'node_entrypoint': lambda path: Path('/fixture/npm-cli.js')}), \
                    patch('shutil.which', return_value='/fixture/existing-bin'):
                setup['main']()
                rebuilds = [call for call in commands.call_args_list if 'rebuild' in call.args[0]]
                self.assertEqual(len(rebuilds), 1)
                self.assertEqual(str(rebuilds[0].args[0][0]), '/usr/bin/node')
            self.assertEqual((home / '.node-version').read_text(), '24\n')
            self.assertEqual((home / '.claude/settings.json').read_text(), '{"model":"fixture-keep"}')

    def test_setup_non_dry_mcp_uses_native_add_and_keeps_present_servers(self):
        setup = runpy.run_path(str(ROOT / 'bin/setup'))
        # Run real-home guarded code with native CLI writes mocked, never touching home.
        with patch.object(sys, 'argv', ['setup', '--mcp']), patch('builtins.print'), \
                patch.dict(setup['main'].__globals__, {
                    'mcp_registration_status': lambda agent, name, env: 'missing' if agent == 'codex' else 'present',
                    'managed_cli_command': lambda home, binary: Path('/fixture/managed') / binary}), \
                patch('subprocess.run', return_value=subprocess.CompletedProcess([], 0)) as command:
            setup['main']()
            self.assertEqual([call.args[0] for call in command.call_args_list], [
                ['codex', 'mcp', 'add', 'argent', '--', '/fixture/managed/argent', 'mcp'],
                ['codex', 'mcp', 'add', 'agentation', '--', '/fixture/managed/agentation-mcp', 'server']])
            self.assertTrue(all(call.kwargs['timeout'] == 15 for call in command.call_args_list))

    def test_config_health_does_not_scan_or_export_provider_values(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            (home / '.claude').mkdir()
            secret = 'fixture-provider-secret'
            (home / '.claude/settings.json').write_text(json.dumps({'model': secret, 'hooks': {}}))
            (home / '.codex').mkdir()
            (home / '.codex/config.toml').write_text('model_provider = "' + secret + '"\n')
            cfg = {'agents': ['codex', 'claude', 'pi'], 'npm': {'agentation-mcp': 'fixture'}, 'skills': {'local': ['blank-direction']}}
            def repo_scandir(path):
                if not Path(path).is_relative_to(ROOT):
                    raise AssertionError('must not scan home')
                return original_scandir(path)
            original_scandir = os.scandir
            with patch('os.scandir', side_effect=repo_scandir), patch('subprocess.run', side_effect=AssertionError('must not run')):
                rows = installed_health(home, ROOT, cfg)
            self.assertNotIn(secret, json.dumps(rows))
            statuses = {row['check']: row['status'] for row in rows}
            self.assertEqual(statuses['codex MCP argent'], 'missing')
            self.assertEqual(statuses['pi MCP registration capability'], 'unknown')
            self.assertEqual(statuses['pi owned extension blank-direction-gate.ts'], 'missing')
            broken = home / '.agents/skills/blank-direction'
            broken.parent.mkdir(parents=True)
            broken.symlink_to(home / 'absent')
            self.assertIn({'check': 'required shared skill blank-direction', 'status': 'missing'}, installed_health(home, ROOT, cfg))
            path = home / '.claude/settings.json'
            path.write_text('not json')
            self.assertEqual(read_health_config(path)[0], 'unknown')

    def test_startup_health_is_nonblocking_bounded_and_does_not_write(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            result = subprocess.run([sys.executable, ROOT / 'bin/dotfiles-health', '--hook', '--home', home],
                                    capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(len(result.stdout.splitlines()), 1)
            self.assertIn('unknown', result.stdout)
            self.assertEqual(list(home.iterdir()), [])

    def test_doctor_config_only_is_fixture_safe_and_json_is_metadata(self):
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, ROOT / 'bin/doctor', '--config-only', '--json', '--home', folder],
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 1)
            report = json.loads(result.stdout)
            self.assertGreater(report['failed'], 0)
            self.assertGreater(report['unknown'], 0)
            self.assertNotIn(folder, result.stdout)


if __name__ == '__main__':
    unittest.main()
