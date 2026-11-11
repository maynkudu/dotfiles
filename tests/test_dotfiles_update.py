import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / 'bin/dotfiles-update'


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.remote = self.root / 'remote.git'
        self.writer = self.root / 'writer'
        self.checkout = self.root / 'checkout'
        self.env = dict(os.environ, XDG_CACHE_HOME=str(self.root / 'cache'))
        self.env.pop('DOTFILES_UPDATE_CHECK', None)
        subprocess.run(['git', 'init', '--bare', '--initial-branch=main', str(self.remote)],
                       check=True, capture_output=True)
        subprocess.run(['git', 'clone', str(self.remote), str(self.writer)], check=True, capture_output=True)
        (self.writer / 'README.md').write_text('Initial setup\n')
        self.commit(self.writer, 'Initial setup')
        self.git(self.writer, 'push', 'origin', 'main')
        subprocess.run(['git', 'clone', str(self.remote), str(self.checkout)], check=True, capture_output=True)
        self.head = self.git(self.checkout, 'rev-parse', 'HEAD')

    def git(self, folder, *args):
        return subprocess.run(['git', '-C', str(folder), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def commit(self, folder, subject):
        self.git(folder, 'add', '.')
        self.git(folder, '-c', 'user.name=Dotfiles fixture', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-m', subject)

    def add_update(self):
        (self.writer / 'skills.json').write_text('{"skills":["yt-script"]}\n')
        self.commit(self.writer, 'Add YouTube skills')
        self.git(self.writer, 'push', 'origin', 'main')

    def check(self, *args, env=None):
        return subprocess.run([sys.executable, str(CHECKER), '--repo', str(self.checkout), *args],
                              capture_output=True, text=True, env=env or self.env, timeout=5)

    def test_current_checkout_is_quiet_at_startup(self):
        result = self.check('--startup')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr, '')
        self.assertIn('up to date', self.check().stdout)

    def test_new_remote_commit_lists_changes_and_preserves_local_edits(self):
        self.add_update()
        local = self.checkout / 'README.md'
        local.write_text('Keep my local edit\n')
        result = self.check('--startup')
        self.assertEqual(result.returncode, 0)
        self.assertIn('1 new commit on origin/main', result.stdout)
        self.assertIn('Add YouTube skills', result.stdout)
        self.assertIn('skills.json', result.stdout)
        self.assertIn('Local changes are present', result.stdout)
        self.assertIn('pull --ff-only', result.stdout)
        self.assertEqual(local.read_text(), 'Keep my local edit\n')
        self.assertEqual(self.git(self.checkout, 'rev-parse', 'HEAD'), self.head)
        self.assertFalse((self.checkout / 'skills.json').exists())

    def test_diverged_checkout_requires_review_and_lists_only_incoming_files(self):
        self.add_update()
        local = self.checkout / 'local.txt'
        local.write_text('Local work\n')
        self.commit(self.checkout, 'Keep local work')
        head = self.git(self.checkout, 'rev-parse', 'HEAD')
        result = self.check('--startup')
        self.assertEqual(result.returncode, 0)
        self.assertIn('1 new commit', result.stdout)
        self.assertIn('1 local commit', result.stdout)
        self.assertIn('Review the branches', result.stdout)
        self.assertNotIn('pull --ff-only', result.stdout)
        self.assertNotIn('local.txt', result.stdout)
        self.assertEqual(self.git(self.checkout, 'rev-parse', 'HEAD'), head)
        self.assertEqual(local.read_text(), 'Local work\n')

    def test_agent_hook_includes_the_notice_and_requires_user_instruction(self):
        self.add_update()
        result = self.check('--hook')
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn('Add YouTube skills', data['systemMessage'])
        hook = data['hookSpecificOutput']
        self.assertEqual(hook['hookEventName'], 'SessionStart')
        self.assertIn('Tell the user', hook['additionalContext'])
        self.assertIn('requires their instruction', hook['additionalContext'])

    def test_github_ssh_remote_uses_https_without_changing_the_remote(self):
        self.add_update()
        ssh_remote = 'git@github.com:fixture/dotfiles.git'
        self.git(self.checkout, 'remote', 'set-url', 'origin', ssh_remote)
        # Route the public HTTPS address to the local fixture without network access.
        self.git(self.checkout, 'config', f'url.{self.remote}.insteadOf', 'https://github.com/fixture/dotfiles.git')
        result = self.check('--startup')
        self.assertEqual(result.returncode, 0)
        self.assertIn('Add YouTube skills', result.stdout)
        self.assertEqual(self.git(self.checkout, 'remote', 'get-url', 'origin'), ssh_remote)
        self.assertEqual(self.git(self.checkout, 'rev-parse', 'HEAD'), self.head)

    def test_missing_remote_does_not_block_startup(self):
        self.git(self.checkout, 'remote', 'set-url', 'origin', str(self.root / 'missing.git'))
        result = self.check('--startup')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout + result.stderr, '')
        explicit = self.check()
        self.assertEqual(explicit.returncode, 1)
        self.assertIn('update check failed', explicit.stderr)
        self.assertEqual(self.git(self.checkout, 'rev-parse', 'HEAD'), self.head)

    def test_slow_remote_times_out_and_startup_continues(self):
        paused_ssh = self.root / 'paused_ssh.py'
        paused_ssh.write_text('import signal\nsignal.pause()\n')
        self.git(self.checkout, 'remote', 'set-url', 'origin', 'ssh://fixture.invalid/dotfiles.git')
        env = dict(self.env, GIT_SSH_COMMAND=shlex.join([sys.executable, str(paused_ssh)]))
        started = time.monotonic()
        result = self.check('--startup', '--timeout', '0.2', env=env)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout + result.stderr, '')
        self.assertLess(time.monotonic() - started, 2)
        self.assertEqual(self.git(self.checkout, 'rev-parse', 'HEAD'), self.head)

    def test_checks_can_be_disabled_by_environment_or_configuration(self):
        self.add_update()
        result = self.check('--startup', env=dict(self.env, DOTFILES_UPDATE_CHECK='0'))
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout + result.stderr, '')
        (self.checkout / 'setup.toml').write_text('[updates]\nenabled = false\n')
        result = self.check('--startup')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout + result.stderr, '')


if __name__ == '__main__':
    unittest.main()
