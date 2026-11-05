import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

BLANK = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'bin/blank'))


class BlankTests(unittest.TestCase):
    def test_search_routes_preserve_query_and_section(self):
        namespace = BLANK['main'].__globals__
        query = 'retry queue & cache'
        for command, arguments, endpoint in (
            ('search', [], '/direction/discover'),
            ('registry-search', ['--section', 'backend'], '/registry/search'),
        ):
            paths = []
            with self.subTest(command=command), patch.dict(namespace, fetch=paths.append), \
                 patch.object(sys, 'argv', ['blank', command, query, *arguments]):
                BLANK['main']()
                request = urlsplit(paths[0])
                self.assertEqual(request.path, endpoint)
                expected = {'q': [query]}
                if command == 'registry-search':
                    expected['section'] = ['backend']
                self.assertEqual(parse_qs(request.query), expected)

    def test_registry_token_uses_stdin_and_child_environment(self):
        token = 'blank_dummy_test_credential'
        namespace = BLANK['credential'].__globals__
        with patch.dict(namespace, credential=lambda name: token), patch('subprocess.run') as run:
            BLANK['fetch']('/r/registry.json', authenticated=True)
            self.assertNotIn(token, repr(run.call_args.args))
            self.assertEqual(run.call_args.kwargs['input'], f'Authorization: Bearer {token}\n')
        with patch.dict(namespace, credential=lambda name: token), patch('os.execvpe') as execute:
            with patch.object(sys, 'argv', ['blank', 'shadcn', 'view', '@compronents/cell-portrait']):
                BLANK['main']()
            binary, arguments, environment = execute.call_args.args
            self.assertEqual(binary, 'shadcn')
            self.assertNotIn(token, repr(arguments))
            self.assertEqual(environment['BLANK_REGISTRY_TOKEN'], token)

    def test_configure_preserves_project_and_is_idempotent(self):
        original = {'style': 'new-york', 'aliases': {'ui': '@/ui'},
                    'registries': {'@other': 'https://example.com/{name}.json'}}
        with tempfile.TemporaryDirectory() as folder, patch('builtins.print'):
            project = Path(folder)
            path = project / 'components.json'
            path.write_text(json.dumps(original))
            BLANK['configure'](project)
            first = path.read_text()
            updated = json.loads(first)
            entry = updated['registries'].pop('@compronents')
            self.assertEqual(updated, original)
            self.assertEqual(entry['headers']['Authorization'], 'Bearer ${BLANK_REGISTRY_TOKEN}')
            BLANK['configure'](project)
            self.assertEqual(path.read_text(), first)

    def test_configure_refuses_conflicting_namespace(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'components.json'
            original = '{"registries":{"@compronents":"https://example.com/{name}.json"}}\n'
            path.write_text(original)
            with self.assertRaises(ValueError):
                BLANK['configure'](Path(folder))
            self.assertEqual(path.read_text(), original)

    def test_credential_file_must_be_owner_only(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'kiys'
            path.write_text('Registry token: blank_dummy_test_credential\n')
            path.chmod(0o644)
            with patch.dict('os.environ', BLANK_KEYS_FILE=str(path)):
                with self.assertRaises(ValueError):
                    BLANK['credential']('registry_token')
                path.chmod(0o600)
                self.assertEqual(BLANK['credential']('registry_token'), 'blank_dummy_test_credential')


if __name__ == '__main__':
    unittest.main()
