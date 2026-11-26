import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'bin'))
from agent_profiles import agent_profile_dirs, discover_agent_profiles


class AgentProfileTests(unittest.TestCase):
    def test_prefix_discovery_is_shallow_and_deduplicates_directory_aliases(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            for name in ('.codex-fast', 'codex-team', '.config/codex-extra', '.claude-work',
                         'claude-personal', '.grok-test', '.pi-fast/agent', '.config/opencode-dev', 'pictures'):
                (home / name).mkdir(parents=True)
            (home / '.codex-backup.json').write_text('keep file')
            (home / '.codex-alias').symlink_to(home / '.codex-fast', target_is_directory=True)
            profiles = discover_agent_profiles(home, ['codex', 'claude', 'pi', 'opencode'], include_existing=True)
            self.assertEqual(len(profiles['codex']), 4)
            self.assertIn(home / '.config/codex-extra', profiles['codex'])
            self.assertIn(home / '.claude-work', profiles['claude'])
            self.assertIn(home / '.grok-test', profiles['grok'])
            self.assertNotIn(home / '.grok', profiles['grok'])
            self.assertIn(home / '.pi-fast/agent', profiles['pi'])
            self.assertNotIn(home / 'pictures/agent', profiles['pi'])
            self.assertEqual((home / '.codex-backup.json').read_text(), 'keep file')

    def test_environment_overrides_apply_only_to_the_real_target_home(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            env = {'CODEX_HOME': str(home / 'custom-codex'),
                   'CLAUDE_CONFIG_DIR': str(home / 'custom-claude'),
                   'PI_CODING_AGENT_DIR': str(home / 'custom-pi')}
            with patch.dict(os.environ, env):
                self.assertNotIn(home / 'custom-codex', agent_profile_dirs(home, 'codex'))
                with patch.object(Path, 'home', return_value=home):
                    for agent in ('codex', 'claude', 'pi'):
                        self.assertIn(home / f'custom-{agent}', agent_profile_dirs(home, agent))

    def test_install_covers_existing_variants_preserves_hooks_and_repeats_cleanly(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            profiles = {agent: home / name for agent, name in (
                ('codex', '.codex-work'), ('claude', '.claude-work'), ('grok', '.grok-work'),
                ('pi', '.pi-work/agent'), ('opencode', '.config/opencode-work'))}
            for profile in profiles.values():
                profile.mkdir(parents=True)
            foreign = {'hooks': [{'type': 'command', 'command': 'keep-this-hook'}]}
            claude = profiles['claude'] / 'settings.json'
            claude.write_text(json.dumps({'model': 'keep-model', 'hooks': {'UserPromptSubmit': [foreign]}}))
            cmd = [sys.executable, ROOT / 'skills/bin/install', '--home', home]
            before = sorted(str(p) for p in home.rglob('*'))
            subprocess.run([*cmd, '--dry-run'], check=True, capture_output=True, text=True, timeout=15)
            self.assertEqual(before, sorted(str(p) for p in home.rglob('*')))
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=20)
            for agent, profile in profiles.items():
                if agent == 'claude':
                    self.assertTrue((profile / 'rules/dotfiles-rules.md').is_file())
                    settings = json.loads(claude.read_text())
                    self.assertEqual(settings['model'], 'keep-model')
                    self.assertIn(foreign, settings['hooks']['UserPromptSubmit'])
                else:
                    self.assertEqual((profile / 'AGENTS.md').read_text(),
                                     (ROOT / 'skills/build' / agent / 'AGENTS.md').read_text())
                if agent in ('codex', 'claude', 'grok'):
                    name = {'codex': 'hooks.json', 'claude': 'settings.json', 'grok': 'hooks/blank-direction-gate.json'}[agent]
                    self.assertIn('UserPromptSubmit', json.loads((profile / name).read_text())['hooks'])
            def installed_files():
                names = {'AGENTS.md', 'settings.json', 'hooks.json', 'config.toml', 'opencode.json'}
                return {str(p): p.stat().st_mtime_ns for p in home.rglob('*')
                        if p.is_file() and not p.is_symlink() and (p.name in names or '.before-dotfiles-' in p.name)}
            first = installed_files()
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=20)
            self.assertEqual(first, installed_files())

    def test_explicit_agent_selection_leaves_other_profiles_untouched(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            (home / '.codex-unused').mkdir()
            subprocess.run([sys.executable, ROOT / 'skills/bin/install', '--home', home, '--agents', 'claude'],
                           check=True, capture_output=True, text=True, timeout=15)
            self.assertEqual(list((home / '.codex-unused').iterdir()), [])
            self.assertFalse((home / '.codex').exists())


if __name__ == '__main__':
    unittest.main()
