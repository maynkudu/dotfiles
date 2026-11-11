import json
import pathlib
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def run_installer(self, home, *args):
        return subprocess.run(
            ['python3', str(ROOT / 'skills/bin/install'), '--home', str(home), *args],
            capture_output=True, text=True, check=True,
        )

    def test_dry_run_does_not_create_directories(self):
        with tempfile.TemporaryDirectory() as folder:
            home = pathlib.Path(folder)
            self.run_installer(home, '--dry-run')
            self.assertEqual(list(home.iterdir()), [])

    def test_fresh_home_dry_run_shows_the_hooks_to_be_installed(self):
        with tempfile.TemporaryDirectory() as folder:
            home = pathlib.Path(folder)
            result = self.run_installer(home, '--agents', 'codex', '--dry-run')
            self.assertIn('PreToolUse', result.stdout)
            self.assertIn('PostToolUse', result.stdout)
            self.assertEqual(list(home.iterdir()), [])

    def test_defaults_backups_and_idempotence(self):
        with tempfile.TemporaryDirectory() as folder:
            home = pathlib.Path(folder)
            rules = home / '.claude/rules'
            rules.mkdir(parents=True)
            (rules / 'about-me.md').write_text('personal original')
            (rules / 'local.md').write_text('keep local')
            (home / '.codex').mkdir()
            external = home / 'original.md'
            external.write_text('original codex')
            (home / '.codex/AGENTS.md').symlink_to(external)
            self.run_installer(home)
            self.assertEqual(external.read_text(), 'original codex')
            self.assertEqual((rules / 'local.md').read_text(), 'keep local')
            backups = list(rules.glob('about-me.md.before-dotfiles-*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), 'personal original')
            self.assertTrue((home / '.pi/agent/AGENTS.md').is_file())
            self.assertEqual((home / '.pi/agent/extensions/dotfiles-update.ts').resolve(),
                             ROOT / 'skills/hooks/pi-dotfiles-update.ts')
            for agent in ('.grok', '.config/opencode'):
                self.assertFalse((home / agent).exists())
            before = sorted(str(p.relative_to(home)) for p in home.rglob('*'))
            self.run_installer(home)
            self.assertEqual(before, sorted(str(p.relative_to(home)) for p in home.rglob('*')))

    def test_shell_preserves_existing_configuration(self):
        with tempfile.TemporaryDirectory() as folder:
            home = pathlib.Path(folder)
            (home / '.bashrc').write_text('alias existing=true\n')
            cmd = ['python3', str(ROOT / 'bin/setup'), '--home', str(home), '--shell']
            subprocess.run(cmd, check=True, capture_output=True)
            content = (home / '.bashrc').read_text()
            self.assertTrue(content.startswith('alias existing=true\n'))
            subprocess.run(cmd, check=True, capture_output=True)
            self.assertEqual(content, (home / '.bashrc').read_text())
            self.assertEqual(len(list(home.glob('.bashrc.before-dotfiles-*'))), 1)

    def test_hook_install_preserves_unrelated_handlers_and_settings(self):
        with tempfile.TemporaryDirectory() as folder:
            home = pathlib.Path(folder)
            path = home / '.claude/settings.json'
            path.parent.mkdir()
            gate = ROOT / 'skills/hooks/blank-direction-gate'
            foreign = {'type': 'command', 'command': 'printf keep'}
            updater = ROOT / 'bin/dotfiles-update'
            original = {'model': 'keep-current-model', 'permissions': {'allow': ['Read']},
                        'hooks': {'SessionStart': [{'hooks': [
                            {'type': 'command', 'command': f'{updater} --hook'}, foreign]}],
                                  'PreToolUse': [{'matcher': 'Bash', 'hooks': [
                            {'type': 'command', 'command': f'{gate} gate'}, foreign]}]}}
            path.write_text(json.dumps(original))
            self.run_installer(home, '--agents', 'claude')
            first = path.read_text()
            settings = json.loads(first)
            self.assertEqual(settings['model'], original['model'])
            self.assertIn('Read', settings['permissions']['allow'])
            groups = settings['hooks']['PreToolUse']
            self.assertIn({'matcher': 'Bash', 'hooks': [foreign]}, groups)
            self.assertEqual(sum(str(gate) in hook.get('command', '') for group in groups for hook in group['hooks']), 1)
            starts = settings['hooks']['SessionStart']
            self.assertIn({'hooks': [foreign]}, starts)
            self.assertIn(str(updater), starts[0]['hooks'][0]['command'])
            self.assertEqual(sum(str(updater) in hook.get('command', '') for group in starts for hook in group['hooks']), 1)
            self.run_installer(home, '--agents', 'claude')
            self.assertEqual(path.read_text(), first)
            self.assertEqual(len(list(path.parent.glob('settings.json.before-dotfiles-*'))), 1)

    def test_hook_install_does_not_write_through_an_external_symlink(self):
        with tempfile.TemporaryDirectory() as folder:
            home = pathlib.Path(folder)
            original = home / 'external-settings.json'
            original.write_text('{"model":"keep-current-model"}\n')
            settings = home / '.claude/settings.json'
            settings.parent.mkdir()
            settings.symlink_to(original)
            self.run_installer(home, '--agents', 'claude')
            self.assertEqual(original.read_text(), '{"model":"keep-current-model"}\n')
            self.assertFalse(settings.is_symlink())
            self.assertIn('PreToolUse', json.loads(settings.read_text())['hooks'])
            backups = list(settings.parent.glob('settings.json.before-dotfiles-*'))
            self.assertEqual(len(backups), 1)
            self.assertTrue(backups[0].is_symlink())

    def test_optional_agent_adapters_are_installed_only_when_selected(self):
        with tempfile.TemporaryDirectory() as folder:
            home = pathlib.Path(folder)
            self.run_installer(home, '--agents', 'pi', 'opencode', 'grok')
            self.assertEqual((home / '.pi/agent/extensions/blank-direction-gate.ts').resolve(),
                             ROOT / 'skills/hooks/pi-blank-direction.ts')
            self.assertEqual((home / '.config/opencode/plugins/blank-direction-gate.ts').resolve(),
                             ROOT / 'skills/hooks/opencode-blank-direction.ts')
            self.assertIn('PreToolUse', json.loads((home / '.grok/hooks/blank-direction-gate.json').read_text())['hooks'])
            self.assertFalse((home / '.codex').exists())
            self.assertFalse((home / '.claude').exists())

    @unittest.skipUnless(shutil.which('codex'), 'Codex CLI is needed to verify its hook trust')
    def test_codex_loads_and_trusts_the_installed_gate(self):
        with tempfile.TemporaryDirectory() as folder:
            home = pathlib.Path(folder)
            self.run_installer(home, '--agents', 'codex')
            args = ['install', '--home', str(home)]
            with patch.object(sys, 'argv', args):
                installer = runpy.run_path(str(ROOT / 'skills/bin/install'))
            gate = str(ROOT / 'skills/hooks/blank-direction-gate')
            hooks = [hook for hook in installer['codex_hook_hashes'](pathlib.Path(shutil.which('codex')))
                     if gate in hook.get('command', '')]
            self.assertEqual(len(hooks), 2)
            self.assertTrue(all(hook['trustStatus'] == 'trusted' for hook in hooks))
            startup = [hook for hook in installer['codex_hook_hashes'](pathlib.Path(shutil.which('codex')))
                       if str(ROOT / 'bin/dotfiles-update') in hook.get('command', '')]
            self.assertEqual(len(startup), 1)
            self.assertEqual(startup[0]['eventName'], 'sessionStart')
            self.assertEqual(startup[0]['trustStatus'], 'trusted')

    def test_shared_skills_are_linked_for_all_selected_clients_without_replacing_local_skills(self):
        source = {'repo': 'fixture/skills', 'ref': '0' * 40,
                  'skills': [{'name': name, 'path': f'skills/{name}'} for name in ('yt-script', 'yt-package')]}
        with tempfile.TemporaryDirectory() as folder:
            home = pathlib.Path(folder)
            shared = home / '.agents/skills/yt-script'
            shared.mkdir(parents=True)
            (shared / 'SKILL.md').write_text('---\nname: yt-script\ndescription: fixture\n---\n')
            package = home / '.agents/skills/yt-package'
            package.mkdir()
            (package / 'SKILL.md').write_text('---\nname: yt-package\ndescription: fixture\n---\n')
            local = home / '.pi/agent/skills/yt-script'
            local.mkdir(parents=True)
            (local / 'SKILL.md').write_text('local skill')
            for dry_run in (True, False, False):
                args = [str(ROOT / 'bin/setup'), '--skills', '--home', str(home)]
                if dry_run:
                    args.append('--dry-run')
                with (patch.object(sys, 'argv', args),
                      patch('json.loads', return_value={'sources': [source]}),
                      patch('subprocess.run') as commands, patch('builtins.print')):
                    setup = runpy.run_path(str(ROOT / 'bin/setup'))
                    setup['main']()
                claude = home / '.claude/skills/yt-script'
                self.assertEqual(claude.exists(), not dry_run)
                if not dry_run:
                    self.assertEqual(claude.resolve(), shared)
                    self.assertEqual((home / '.pi/agent/skills/yt-package').resolve(), package)
                else:
                    self.assertFalse((home / '.pi/agent/skills/yt-package').exists())
                self.assertEqual((local / 'SKILL.md').read_text(), 'local skill')
                self.assertFalse(any('--repo' in call.args[0] for call in commands.call_args_list))

    def test_skill_helpers_restore_executable_permissions_without_changing_content(self):
        source = {
            'repo': 't3dotgg/tstack',
            'ref': '1085050f3baed1ac724caa4a8166145fb2ac88af',
            'skills': [{'name': 'babysit-pr', 'path': 'skills/babysit-pr',
                        'executables': ['scripts/pr-wait']}],
        }
        with tempfile.TemporaryDirectory() as folder:
            home = pathlib.Path(folder)
            skill = home / '.agents/skills/babysit-pr'
            helper = skill / 'scripts/pr-wait'
            helper.parent.mkdir(parents=True)
            helper.write_text('print("ready")\n')
            helper.chmod(0o644)
            (skill / 'SKILL.md').write_text('---\nname: babysit-pr\n---\n')
            for dry_run in (True, False, False):
                args = [str(ROOT / 'bin/setup'), '--skills', '--home', str(home)]
                if dry_run:
                    args.append('--dry-run')
                with (
                    patch.object(sys, 'argv', args),
                    patch('json.loads', return_value={'sources': [source]}),
                    patch('subprocess.run'),
                    patch('builtins.print'),
                ):
                    setup = runpy.run_path(str(ROOT / 'bin/setup'))
                    setup['main']()
                self.assertEqual(helper.stat().st_mode & 0o777, 0o644 if dry_run else 0o755)
                self.assertEqual(helper.read_text(), 'print("ready")\n')

    def test_webreel_patch_respects_version_dry_run_and_backups(self):
        original = 'const args = [\n                "--enable-begin-frame-control",\n];\n'
        for version, dry_run in [('0.1.4', True), ('0.1.4', False), ('0.1.5', False)]:
            with self.subTest(version=version, dry_run=dry_run), tempfile.TemporaryDirectory() as folder:
                home = pathlib.Path(folder)
                core = home / '.local/lib/node_modules/webreel/node_modules/@webreel/core'
                (core / 'dist').mkdir(parents=True)
                (core / 'package.json').write_text(json.dumps({'version': version}))
                chrome = core / 'dist/chrome.js'
                chrome.write_text(original)
                args = [str(ROOT / 'bin/setup'), '--tools', '--home', str(home)]
                if dry_run:
                    args.append('--dry-run')
                with patch.object(sys, 'argv', args), patch('subprocess.run'), patch('builtins.print'):
                    setup = runpy.run_path(str(ROOT / 'bin/setup'))
                    setup['main']()
                    setup['main']()
                changed = version == '0.1.4' and not dry_run
                self.assertEqual('--enable-begin-frame-control' not in chrome.read_text(), changed)
                backups = list(chrome.parent.glob('chrome.js.before-dotfiles-*'))
                self.assertEqual(len(backups), int(changed))
                if changed:
                    self.assertEqual(backups[0].read_text(), original)
                else:
                    self.assertEqual(chrome.read_text(), original)


if __name__ == '__main__':
    unittest.main()
