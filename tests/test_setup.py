import json
import pathlib
import runpy
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
            for agent in ('.grok', '.pi', '.config/opencode'):
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
