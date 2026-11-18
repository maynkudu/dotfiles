"""Synthetic session fixtures. No private transcripts or tool outputs are copied."""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/bin'))
from agent_history import HistoryScope, parse_history_records

TS = '2026-10-01T12:00:00Z'
PROJECT = '/fixture/project'
SECRET = 'fixture-secret-do-not-export'


def stats():
    return {key: 0 for key in ('unknown_records', 'unknown_completions', 'unknown_tools', 'unpaired_results')}


def record(kind, payload, agent='claude'):
    return {'type': kind, 'timestamp': TS, 'message' if agent in ('claude', 'pi') else 'payload': payload}


def fixtures(agent, *, outcome='success', complete=True, string_user=True):
    text = 'Build a new website component ' + SECRET
    user = text if string_user else [{'type': 'text' if agent != 'codex' else 'input_text', 'text': text}]
    if agent == 'codex':
        rows = [{'type': 'session_meta', 'timestamp': TS, 'payload': {'cwd': PROJECT}},
                record('event_msg', {'type': 'user_message', 'message': text}, agent),
                record('response_item', {'role': 'user', 'content': [{'type': 'input_text', 'text': text}]}, agent),
                record('response_item', {'type': 'function_call', 'name': 'exec_command', 'call_id': 'call',
                                         'arguments': json.dumps({'cmd': "blank registry-search 'cli tools' " + SECRET})}, agent)]
        if outcome != 'unknown':
            rows.append(record('response_item', {'type': 'function_call_output', 'call_id': 'call',
                                                 'output': f'Process exited with code {0 if outcome == "success" else 1}\n' + SECRET}, agent))
        rows.append(record('response_item', {'type': 'message', 'role': 'assistant', 'channel': 'commentary',
                                             'content': [{'type': 'output_text', 'text': 'progress'}]}, agent))
        if complete:
            rows.append(record('response_item', {'type': 'message', 'role': 'assistant', 'channel': 'final',
                                                 'content': [{'type': 'output_text', 'text': 'done'}]}, agent))
        return rows
    call_type = 'toolCall' if agent == 'pi' else 'tool_use'
    rows = [{'type': 'session', 'timestamp': TS, 'cwd': PROJECT},
            {**record('message' if agent == 'pi' else 'user', {'role': 'user', 'content': user}, agent), 'cwd': PROJECT},
            record('message' if agent == 'pi' else 'assistant', {'role': 'assistant', 'content': [
                {'type': call_type, 'id': 'call', 'name': 'bash' if agent == 'pi' else 'Bash',
                 'arguments' if agent == 'pi' else 'input': {'command': "blank search 'cli tools' " + SECRET}}]}, agent)]
    if outcome != 'unknown':
        result = {'role': 'toolResult', 'toolCallId': 'call', 'isError': outcome == 'failed',
                  'content': [{'type': 'text', 'text': SECRET}]} if agent == 'pi' else {
                      'role': 'user', 'content': [{'type': 'tool_result', 'tool_use_id': 'call',
                                                   'is_error': outcome == 'failed', 'content': SECRET}]}
        rows.append(record('message' if agent == 'pi' else 'user', result, agent))
    rows.append(record('message' if agent == 'pi' else 'assistant', {'role': 'assistant', 'content': [{'type': 'text', 'text': 'progress'}]}, agent))
    if complete:
        rows.append(record('message' if agent == 'pi' else 'assistant', {
            'role': 'assistant', 'content': [{'type': 'text', 'text': 'done'}],
            'stopReason' if agent == 'pi' else 'stop_reason': 'stop' if agent == 'pi' else 'end_turn'}, agent))
    return rows


class HistoryParserTests(unittest.TestCase):
    def parse(self, agent, **kwargs):
        rows = fixtures(agent, **kwargs)
        return parse_history_records(list(enumerate(rows, 1)), agent, stats())[1]

    def test_three_agents_string_and_list_messages_tool_outcomes_and_explicit_final(self):
        adherence = runpy.run_path(str(ROOT / 'skills/bin/audit-adherence'))
        for agent in ('codex', 'claude', 'pi'):
            for string_user in (True, False):
                for outcome in ('success', 'failed', 'unknown'):
                    with self.subTest(agent=agent, string_user=string_user, outcome=outcome):
                        events = self.parse(agent, outcome=outcome, string_user=string_user)
                        self.assertEqual(sum(e.kind == 'user' for e in events), 1)
                        self.assertEqual(sum(e.kind == 'final' for e in events), 1)
                        self.assertEqual([e.outcome for e in events if e.kind == 'tool'], [outcome])
                        tasks = list(adherence['candidate_tasks'](events, agent, 'session', 'project'))
                        self.assertEqual(len(tasks), 1)
                        self.assertTrue(tasks[0]['complete'])
                        self.assertTrue(tasks[0]['discovery_attempted'])
                        self.assertEqual(tasks[0]['discovery_before_choice'], outcome == 'success')
                        self.assertEqual(tasks[0]['discovery_failed'], outcome == 'failed')
            self.assertFalse(any(e.kind == 'final' for e in self.parse(agent, complete=False)))

    def test_codex_repeated_user_after_final_is_not_deduplicated(self):
        rows = fixtures('codex')
        rows.extend(fixtures('codex')[1:])
        events = parse_history_records(list(enumerate(rows, 1)), 'codex', stats())[1]
        self.assertEqual(sum(e.kind == 'user' for e in events), 2)

    def test_interrupt_and_pi_branch_split_task_completion(self):
        rows = fixtures('codex', complete=False)
        rows.append(record('event_msg', {'type': 'turn_aborted'}, 'codex'))
        rows.append(record('event_msg', {'type': 'task_complete'}, 'codex'))
        events = parse_history_records(list(enumerate(rows, 1)), 'codex', stats())[1]
        adherence = runpy.run_path(str(ROOT / 'skills/bin/audit-adherence'))
        tasks = list(adherence['candidate_tasks'](events, 'codex', 's', 'p'))
        self.assertFalse(tasks[0]['complete'])
        rows = fixtures('pi')
        for index, row in enumerate(rows[1:], 1):
            row['id'] = str(index)
            row['parentId'] = str(index - 1) if index > 1 else None
        rows[-1]['parentId'] = None
        events = parse_history_records(list(enumerate(rows, 1)), 'pi', stats())[1]
        self.assertTrue(any(e.kind == 'boundary' for e in events))

    def write_fixture(self, home, agent, rows=None):
        paths = {'codex': '.codex/sessions/date', 'claude': '.claude/projects/name', 'pi': '.pi/agent/sessions/name'}
        path = home / paths[agent] / (SECRET + '.jsonl')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('\n'.join(json.dumps(row) for row in (rows or fixtures(agent))) + '\n')
        return path

    def test_scope_window_budgets_and_symlinks(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            for agent in ('codex', 'claude', 'pi'):
                self.write_fixture(home, agent)
            scope = HistoryScope(home, PROJECT, '2026-09-01', '2026-11-01')
            self.assertEqual(len(list(scope.sessions())), 3)
            self.assertEqual(scope.metadata()['unknown_tools'], 0)
            scope = HistoryScope(home, '/other/project', '2026-09-01', '2026-11-01')
            self.assertEqual(list(scope.sessions()), [])
            scope = HistoryScope(home, PROJECT, '2026-10-02', '2026-11-01')
            self.assertFalse(any(e.kind == 'user' for _, _, _, events in scope.sessions() for e in events))
            scope = HistoryScope(home, None, '2026-09-01', '2026-11-01', max_files=1)
            list(scope.sessions())
            self.assertEqual(scope.stats['files_read'], 1)
            self.assertTrue(scope.stats['truncated'])
            scope = HistoryScope(home, None, '2026-09-01', '2026-11-01', max_bytes=50)
            list(scope.sessions())
            self.assertTrue(scope.stats['truncated'])
            self.assertLessEqual(scope.stats['bytes_read'], 51)
            (home / '.codex/sessions/link.jsonl').symlink_to(home / 'outside.jsonl')
            scope = HistoryScope(home, None, '2026-09-01', '2026-11-01')
            list(scope.sessions())
            self.assertEqual(scope.stats['files_read'], 3)

    def test_recent_scoped_sessions_survive_foreign_and_oversized_records(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            foreign = self.write_fixture(home, 'codex')
            foreign_rows = fixtures('codex')
            foreign_rows[0]['payload']['cwd'] = '/another/project'
            foreign.write_text('\n'.join(json.dumps(row) for row in foreign_rows) + '\n')
            recent = self.write_fixture(home, 'pi')
            rows = fixtures('pi')
            rows.insert(2, record('message', {'role': 'assistant', 'content': [
                {'type': 'text', 'text': 'x' * (1024 * 1024 + 100)}]}, 'pi'))
            recent.write_text('\n'.join(json.dumps(row) for row in rows) + '\n')
            os.utime(foreign, (2000000000, 2000000000))
            os.utime(recent, (1999999999, 1999999999))
            scope = HistoryScope(home, PROJECT, '2026-09-01', '2026-11-01', max_bytes=4 * 1024 * 1024)
            sessions = list(scope.sessions())
            self.assertEqual(len(sessions), 1)
            self.assertEqual(sessions[0][0], 'pi')
            self.assertTrue(scope.stats['truncated'])
            self.assertTrue(any(event.kind == 'tool' and event.outcome == 'success' for event in sessions[0][3]))
            self.assertLess(scope.stats['bytes_read'], 4 * 1024 * 1024)

    def test_tool_result_outside_window_stays_unknown(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            rows = fixtures('codex')
            for row in rows:
                if (row.get('payload') or {}).get('type') == 'function_call_output':
                    row['timestamp'] = '2026-11-02T12:00:00Z'
            self.write_fixture(home, 'codex', rows)
            scope = HistoryScope(home, PROJECT, '2026-09-01', '2026-11-01')
            events = next(scope.sessions())[3]
            self.assertEqual([e.outcome for e in events if e.kind == 'tool'], ['unknown'])

    def test_cli_reports_and_corpus_never_export_contents_or_names(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            for agent in ('codex', 'claude', 'pi'):
                self.write_fixture(home, agent)
            corpus = home / 'corpus.jsonl'
            for tool in ('audit', 'audit-adherence', 'compliance'):
                args = [sys.executable, ROOT / 'skills/bin' / tool, '--root', home, '--project', PROJECT,
                        '--since', '2026-09-01', '--before', '2026-11-01', '--json']
                if tool == 'audit':
                    args.extend(['--corpus', corpus])
                result = subprocess.run(args, capture_output=True, text=True, check=True)
                report = json.loads(result.stdout)
                self.assertNotIn(SECRET, result.stdout)
                self.assertNotIn(PROJECT, result.stdout)
                self.assertNotIn(folder, result.stdout)
                self.assertEqual(report['metadata']['agents'], ['codex', 'claude', 'pi'])
                if tool == 'audit-adherence':
                    self.assertEqual(report['count'], 3)
                if tool == 'compliance':
                    discovery = next(row for row in report['checks'] if row['behaviour'] == 'BLANK discovery')
                    self.assertTrue(all(data['success'] == 1 for data in discovery['agents'].values()))
            self.assertNotIn(SECRET, corpus.read_text())
            self.assertEqual(corpus.stat().st_mode & 0o777, 0o600)


if __name__ == '__main__':
    unittest.main()
