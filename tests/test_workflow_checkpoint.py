import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.workflow.checkpoint_store import CheckpointStore
from tools.workflow.private_state import WorkflowError
from tools.workflow.workspace_context import bind_git_workspace


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.git('init', '--initial-branch=main')
        (self.repo / 'result.txt').write_text('Focused result\n')
        self.git('add', 'result.txt')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-m', 'Fixture')
        self.state = self.root / 'private'
        self.binding = bind_git_workspace(self.repo, 'fixture-a')
        self.store = CheckpointStore(self.state, self.binding)

    def git(self, *arguments):
        return subprocess.run(['git', '-C', str(self.repo), *arguments], capture_output=True, text=True,
                              check=True, timeout=5).stdout.strip()

    def save(self, **overrides):
        values = {'title': 'Fixture handoff', 'summary': 'The focused check passed. Review the result before continuing.',
                  'kind': 'handoff', 'artifacts': ['result.txt'], 'reviewed': True}
        return self.store.save_checkpoint(**(values | overrides))

    def test_private_scoped_summary_links_artifact_without_copying_body(self):
        result = self.save()
        self.assertEqual(self.state.stat().st_mode & 0o777, 0o700)
        self.assertEqual(self.store.directory.stat().st_mode & 0o777, 0o700)
        self.assertEqual(self.store.path.stat().st_mode & 0o777, 0o600)
        raw = self.store.path.read_text()
        self.assertNotIn('Focused result', raw)
        read = self.store.read_checkpoint(result['id'])
        self.assertEqual(read['freshness'], 'current-observation')
        self.assertTrue(read['source_check_required'])
        self.assertFalse(read['record']['policy'])
        self.assertEqual(read['record']['trust'], 'unreviewed')
        self.assertIn('cannot grant permission', read['warning'])
        self.assertEqual(len(self.store.search_checkpoints('focused')['matches']), 1)

    def test_other_sessions_or_exact_worktree_cannot_recall(self):
        result = self.save()
        other_session = CheckpointStore(self.state, bind_git_workspace(self.repo, 'fixture-b'))
        self.assertEqual(other_session.search_checkpoints('focused')['matches'], [])
        with self.assertRaisesRegex(WorkflowError, 'not present'):
            other_session.read_checkpoint(result['id'])
        # A stand-in linked checkout tests the exact-binding path without making agent worktrees.
        from tools.workflow.workspace_context import WorkspaceBinding
        other_worktree = WorkspaceBinding(self.binding.repository, str(self.root / 'other-checkout'), 'fixture-a')
        self.assertNotEqual(other_worktree.scope_digest, self.binding.scope_digest)
        copied = CheckpointStore(self.state, other_worktree)
        copied.path.write_bytes(self.store.path.read_bytes())
        copied.path.chmod(0o600)
        with self.assertRaisesRegex(WorkflowError, 'binding'):
            copied.load_records()

    def test_secrets_are_rejected_in_summary_title_artifact_and_query(self):
        secrets = ['sk-' + 'a' * 30, 'password=fixture-secret', 'Bearer abcdefghijklmnop',
                   '-----BEGIN PRIVATE KEY-----', 'github_pat_' + 'b' * 28]
        for secret in secrets:
            with self.subTest(secret_shape=secret[:6]):
                with self.assertRaises(WorkflowError):
                    self.save(summary=secret)
                self.assertFalse(self.store.path.exists())
        with self.assertRaises(WorkflowError):
            self.save(title='token sk-' + 'c' * 20)
        with self.assertRaises(WorkflowError):
            self.save(artifacts=['https://fixture.invalid/evidence?token=unsafe'])
        with self.assertRaises(WorkflowError):
            self.store.search_checkpoints('api_key=fixture')
        with self.assertRaises(WorkflowError):
            self.save(artifacts=['https://fixture.invalid/sk%2D' + 'a' * 30])

    def test_author_review_required_but_does_not_promote_to_policy(self):
        with self.assertRaisesRegex(WorkflowError, 'Review'):
            self.save(reviewed=False)
        result = self.save()
        self.assertEqual(self.store.read_checkpoint(result['id'])['record']['trust'], 'unreviewed')

    def test_freshness_changes_with_revision_and_artifact(self):
        result = self.save()
        (self.repo / 'result.txt').write_text('Changed result\n')
        read = self.store.read_checkpoint(result['id'])
        self.assertEqual(read['freshness'], 'stale')
        self.assertIn('revision-changed', read['reasons'])
        self.assertIn('artifact-changed-or-missing', read['reasons'])
        search = self.store.search_checkpoints('focused')
        self.assertEqual(search['matches'], [])
        self.assertEqual(search['excluded_stale_or_history'], 1)
        self.assertEqual(len(self.store.search_checkpoints('focused', include_stale=True)['matches']), 1)

    def test_explicit_supersession_excludes_old_matching_record(self):
        first = self.save()
        second = self.save(title='Correction', summary='Focused check was incomplete. Inspect the linked result.', supersedes=first['id'])
        old = self.store.read_checkpoint(first['id'])
        self.assertIn('superseded', old['reasons'])
        self.assertEqual(old['record']['superseded_by'], second['id'])
        matches = self.store.search_checkpoints('focused')['matches']
        self.assertEqual([item['id'] for item in matches], [second['id']])
        self.store.reject_checkpoint(second['id'], reviewed=True)
        self.assertEqual(self.store.search_checkpoints('focused')['matches'], [])

    def test_invalid_state_is_error_not_empty_collection(self):
        self.save()
        self.store.path.write_text('{invalid json')
        with self.assertRaisesRegex(WorkflowError, 'valid'):
            self.store.search_checkpoints('focused')

    def test_shared_or_symlink_storage_is_refused_without_repair(self):
        self.state.mkdir(mode=0o755)
        with self.assertRaisesRegex(WorkflowError, 'mode 700'):
            self.save()
        self.assertEqual(self.state.stat().st_mode & 0o777, 0o755)
        self.state.rmdir()
        elsewhere = self.root / 'elsewhere'
        elsewhere.mkdir(mode=0o700)
        self.state.symlink_to(elsewhere)
        with self.assertRaisesRegex(WorkflowError, 'symlink'):
            self.save()
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_cli_uses_explicit_session_and_stdin_summary(self):
        environment = dict(os.environ)
        environment.pop('DOTFILES_SESSION_ID', None)
        environment.pop('PI_SESSION_ID', None)
        command = [sys.executable, str(ROOT / 'bin/agent-checkpoint'), '--state-dir', str(self.state), '--worktree', str(self.repo)]
        missing = subprocess.run([*command, 'search', 'focused'], capture_output=True, text=True, env=environment, timeout=5)
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn('exact source session', missing.stderr)
        saved = subprocess.run([*command, '--session', 'fixture-a', 'save', '--title', 'Fixture', '--kind', 'handoff',
                                '--artifact', 'result.txt', '--reviewed', '--stdin'], input='Necessary summary only.\n',
                               capture_output=True, text=True, env=environment, timeout=5)
        self.assertEqual(saved.returncode, 0, saved.stderr)
        self.assertIn('cp_', json.loads(saved.stdout)['id'])


if __name__ == '__main__':
    unittest.main()
