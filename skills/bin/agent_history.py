"""Bounded local history parsing for Codex, Claude and Pi. Raw text stays in memory."""
import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re

AGENTS = ('codex', 'claude', 'pi')
HISTORY_DIRS = {'codex': '.codex/sessions', 'claude': '.claude/projects', 'pi': '.pi/agent/sessions'}


@dataclass
class HistoryEvent:
    """Private event data; export only explicit metadata fields, never this object."""
    kind: str
    timestamp: str
    ordinal: int
    text: str = ''
    name: str = ''
    call_id: str = ''
    outcome: str = 'unknown'
    outcome_timestamp: str = ''


def metadata_id(value):
    """Hash paths/session names rather than exporting potentially private names."""
    return hashlib.sha256(str(value).encode()).hexdigest()[:16]


def history_text(content):
    """Normalize string and list message content without including tool blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return ' '.join(part.get('text', '') for part in content
                        if isinstance(part, dict) and part.get('type') in ('text', 'input_text', 'output_text')
                        and isinstance(part.get('text'), str))
    return ''


def event_timestamp(value):
    """Normalize timestamps to UTC; invalid timestamps cannot satisfy a window."""
    try:
        if isinstance(value, (float, int)):
            return datetime.fromtimestamp(value / 1000, timezone.utc).isoformat()
        if isinstance(value, str):
            parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc).isoformat()
    except (ValueError, OverflowError, OSError):
        pass
    return ''


def tool_outcome(result):
    """Prefer structured errors/exit codes; mere tool invocation is not success."""
    if isinstance(result, str):
        try:
            decoded = json.loads(result)
        except ValueError:
            decoded = None
        if isinstance(decoded, dict):
            return tool_outcome(decoded)
        # Codex shell tool output carries its exit code in this exact header.
        match = re.search(r'(?:Process exited with code|Exit code:)\s*(-?\d+)', result)
        if match:
            return 'success' if int(match[1]) == 0 else 'failed'
        return 'unknown'
    if not isinstance(result, dict):
        return 'unknown'
    if result.get('isError') is True or result.get('is_error') is True or result.get('error'):
        return 'failed'
    for key in ('exit_code', 'exitCode', 'returncode'):
        if isinstance(result.get(key), int):
            return 'success' if result[key] == 0 else 'failed'
    nested = result.get('metadata') or result.get('details')
    if isinstance(nested, dict):
        outcome = tool_outcome(nested)
        if outcome != 'unknown':
            return outcome
    outcome = tool_outcome(history_text(result.get('content')) or result.get('output', ''))
    if outcome != 'unknown':
        return outcome
    if result.get('isError') is False or result.get('is_error') is False:
        return 'success'
    # Claude's tool_result schema omits is_error on normal successful results.
    if result.get('type') == 'tool_result':
        return 'success'
    return 'unknown'


def parse_history_records(records, agent, stats):
    """Pair calls/results by ID and accept only explicit final/stop records."""
    events, pending = [], {}
    cwd = ''
    last_entry = None
    last_user = None
    for ordinal, item in records:
        if not isinstance(item, dict):
            stats['unknown_records'] += 1
            continue
        kind = item.get('type')
        if kind == 'history_gap':
            events.append(HistoryEvent('boundary', '', ordinal))
            pending.clear()
            stats['unknown_records'] += 1
            continue
        message = item.get('message') or item.get('payload') or {}
        if not isinstance(message, dict):
            stats['unknown_records'] += 1
            continue
        timestamp = event_timestamp(item.get('timestamp') or message.get('timestamp'))
        raw_cwd = item.get('cwd') or (message.get('cwd') if kind in ('session_meta', 'turn_context') else None)
        if isinstance(raw_cwd, str):
            cwd = raw_cwd
        elif raw_cwd:
            stats['unknown_records'] += 1
        if agent == 'pi' and item.get('id') and kind != 'session':
            if last_entry is not None and item.get('parentId') != last_entry:
                events.append(HistoryEvent('boundary', timestamp, ordinal))
                pending.clear()
            last_entry = item['id']
        role = message.get('role')
        is_user = role == 'user' and bool(history_text(message.get('content')))
        if not is_user and not (kind == 'event_msg' and message.get('type') == 'user_message') and kind not in ('turn_context', 'session_meta'):
            last_user = None
        content = message.get('content')
        blocks = content if isinstance(content, list) else []
        payload_type = message.get('type')
        if kind == 'event_msg':
            if payload_type == 'user_message':
                text = message.get('message', '')
                if isinstance(text, str) and last_user != (text, 'response_item'):
                    events.append(HistoryEvent('user', timestamp, ordinal, text))
                last_user = (text, 'event_msg')
            elif payload_type in ('task_complete', 'task_completed'):
                events.append(HistoryEvent('final', timestamp, ordinal))
            elif payload_type in ('turn_aborted', 'task_failed', 'task_interrupted'):
                events.append(HistoryEvent('boundary', timestamp, ordinal))
            continue
        if role == 'user':
            text = history_text(content)
            if text:
                pending.clear()  # Results from earlier user turns cannot prove this turn's work.
            # Codex records the same user text in event_msg and response_item.
            if text and not (agent == 'codex' and last_user == (text, 'event_msg')):
                events.append(HistoryEvent('user', timestamp, ordinal, text))
            if text and agent == 'codex':
                last_user = (text, 'response_item')
        calls = [block for block in blocks if isinstance(block, dict) and block.get('type') in ('tool_use', 'toolCall')]
        if kind == 'response_item' and payload_type in ('function_call', 'custom_tool_call'):
            calls.append(message)
        for call in calls:
            arguments = call.get('input', call.get('arguments', ''))
            if not isinstance(arguments, str):
                arguments = json.dumps(arguments)
            call_id = call.get('id') or call.get('call_id') or ''
            event = HistoryEvent('tool', timestamp, ordinal, arguments,
                                 call.get('name', '') if isinstance(call.get('name', ''), str) else '',
                                 call_id if isinstance(call_id, str) else '')
            events.append(event)
            if isinstance(call_id, str) and call_id:
                pending[call_id] = event
        results = [block for block in blocks if isinstance(block, dict) and block.get('type') == 'tool_result']
        if role == 'toolResult' or payload_type in ('function_call_output', 'custom_tool_call_output'):
            results.append(message)
        for result in results:
            call_id = result.get('tool_use_id') or result.get('toolCallId') or result.get('call_id')
            if isinstance(call_id, str) and call_id in pending:
                event = pending.pop(call_id)
                event.outcome = tool_outcome(result)
                event.outcome_timestamp = timestamp
            else:
                stats['unpaired_results'] += 1
        if role == 'assistant' and not calls and history_text(content):
            explicit = message.get('stop_reason') == 'end_turn' or message.get('stopReason') == 'stop'
            if kind == 'response_item':
                explicit = message.get('channel') == 'final' or message.get('phase') == 'final_answer'
            if explicit:
                events.append(HistoryEvent('final', timestamp, ordinal))
            else:
                stats['unknown_completions'] += 1
    stats['unknown_tools'] += sum(e.kind == 'tool' and e.outcome == 'unknown' for e in events)
    return cwd, events


class HistoryScope:
    """Scan only known agent directories with fixed file, byte and event budgets."""
    def __init__(self, root, project, since, before, *, max_files=200, max_events=100000, max_bytes=32 * 1024 * 1024):
        self.root = Path(root).expanduser().resolve()
        self.project = Path(project).expanduser().resolve() if project else None
        self.since, self.before = event_timestamp(since), event_timestamp(before)
        self.max_files, self.max_events, self.max_bytes = max_files, max_events, max_bytes
        self.stats = {key: 0 for key in ('files_read', 'events_read', 'bytes_read', 'invalid_records', 'unknown_records',
                                        'unknown_completions', 'unknown_tools', 'unpaired_results', 'unscoped_sessions')}
        self.stats['truncated'] = False

    def paths(self):
        """Do not follow directory symlinks or enumerate arbitrary home subtrees."""
        examined = 0
        candidates = []
        for agent in AGENTS:
            queue = [(self.root / HISTORY_DIRS[agent], 0)]
            while queue:
                directory, depth = queue.pop()
                if directory.is_symlink() or depth > 6:
                    continue
                try:
                    with os.scandir(directory) as entries:
                        for entry in entries:
                            examined += 1
                            if examined > 10000:
                                self.stats['truncated'] = True
                                break
                            if entry.is_symlink():
                                continue
                            if entry.is_dir(follow_symlinks=False):
                                if entry.name not in ('subagents', 'subagent-artifacts'):
                                    queue.append((Path(entry.path), depth + 1))
                            elif entry.name.endswith('.jsonl') and not entry.name.startswith('agent-'):
                                candidates.append((entry.stat(follow_symlinks=False).st_mtime_ns, agent, Path(entry.path)))
                except OSError:
                    continue
                if examined > 10000:
                    break
            if examined > 10000:
                break
        # Budgets should cover recent work across all agents, not whichever
        # directory the filesystem happened to enumerate first.
        for _, agent, path in sorted(candidates, reverse=True):
            yield agent, path

    def sessions(self):
        """Filter sessions to exact project and time bounds before exposing events."""
        for agent, path in self.paths():
            if (self.stats['files_read'] >= self.max_files
                    or self.stats['bytes_read'] >= self.max_bytes):
                self.stats['truncated'] = True
                break
            self.stats['files_read'] += 1
            if self.project:
                # Session cwd is metadata near the beginning of supported logs.
                # Reject other projects before they consume the full read budget.
                # An absent/unreadable header stays unknown, never broadens scope.
                try:
                    with path.open('rb') as stream:
                        header = stream.read(min(65536, self.max_bytes - self.stats['bytes_read']))
                    self.stats['bytes_read'] += len(header)
                    cwd = ''
                    for line in header.splitlines():
                        try:
                            item = json.loads(line)
                        except (ValueError, UnicodeError):
                            continue
                        if not isinstance(item, dict):
                            continue
                        payload = item.get('payload') or {}
                        value = item.get('cwd') or (payload.get('cwd') if isinstance(payload, dict) else None)
                        if isinstance(value, str) and value:
                            cwd = value
                            break
                    if not cwd:
                        self.stats['unscoped_sessions'] += 1
                        continue
                    if Path(cwd).resolve() != self.project:
                        continue
                except OSError:
                    self.stats['unscoped_sessions'] += 1
                    continue
            records = []
            budget_exhausted = False
            try:
                with path.open('rb') as stream:
                    for ordinal in range(1, self.max_events + 1):
                        remaining = min(1024 * 1024, self.max_bytes - self.stats['bytes_read'])
                        if remaining <= 0 or self.stats['events_read'] >= self.max_events:
                            self.stats['truncated'] = True
                            budget_exhausted = True
                            break
                        line = stream.readline(remaining + 1)
                        if not line:
                            break
                        self.stats['bytes_read'] += len(line)
                        self.stats['events_read'] += 1
                        if len(line) > remaining:
                            self.stats['truncated'] = True
                            # Drop oversized content without losing every later
                            # session. Drain only within the total byte budget.
                            while not line.endswith(b'\n'):
                                allowance = self.max_bytes - self.stats['bytes_read']
                                if allowance <= 0:
                                    budget_exhausted = True
                                    break
                                line = stream.readline(min(65536, allowance))
                                self.stats['bytes_read'] += len(line)
                                if not line:
                                    break
                            records.append((ordinal, {'type': 'history_gap'}))
                            if budget_exhausted:
                                break
                            continue
                        try:
                            records.append((ordinal, json.loads(line)))
                        except (ValueError, UnicodeError):
                            self.stats['invalid_records'] += 1
            except OSError:
                continue
            cwd, events = parse_history_records(records, agent, self.stats)
            if not cwd:
                self.stats['unscoped_sessions'] += 1
            if self.project and (not cwd or Path(cwd).resolve() != self.project):
                continue
            for event in events:
                if event.kind == 'tool' and (not event.outcome_timestamp or not self.since <= event.outcome_timestamp < self.before):
                    event.outcome = 'unknown'
            # Keep out-of-window events as boundaries so a result cannot cross a cutoff.
            selected = [event if event.timestamp and self.since <= event.timestamp < self.before
                        else HistoryEvent('boundary', event.timestamp, event.ordinal) for event in events]
            yield agent, metadata_id(path.relative_to(self.root)), metadata_id(cwd), selected
            if budget_exhausted:
                break

    def metadata(self):
        """Safe scan metadata, without paths, prompt text, tool names or arguments."""
        return {'schema_version': 1, 'agents': list(AGENTS), 'scope_id': metadata_id(self.project or 'all-projects'),
                'all_projects': self.project is None, 'since': self.since, 'before': self.before,
                'limits': {'files': self.max_files, 'events': self.max_events, 'bytes': self.max_bytes}, **self.stats}


def add_history_arguments(parser):
    """Default to the current project and the last 30 days, not all home history."""
    parser.add_argument('--root', type=Path, default=Path.home(), help='Home or isolated fixture root; only known history directories are read')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--project', type=Path, default=Path.cwd(), help='Exact session cwd, defaults to current directory')
    group.add_argument('--all-projects', action='store_true', help='Explicitly include other project sessions within the same budgets')
    parser.add_argument('--since', default=(datetime.now(timezone.utc) - timedelta(days=30)).date().isoformat())
    parser.add_argument('--before', default='9999-12-31', help='Exclusive ISO timestamp/date cutoff')
    parser.add_argument('--max-files', type=int, default=200)
    parser.add_argument('--max-events', type=int, default=100000)
    parser.add_argument('--max-bytes', type=int, default=32 * 1024 * 1024)


def scope_from_args(parser, args):
    """Validate user bounds without silently broadening scope."""
    if not all(value > 0 for value in (args.max_files, args.max_events, args.max_bytes)):
        parser.error('history budgets must be positive')
    since, before = event_timestamp(args.since), event_timestamp(args.before)
    if not since or not before or since >= before:
        parser.error('expected a valid --since before --before')
    return HistoryScope(args.root, None if args.all_projects else args.project, since, before,
                        max_files=args.max_files, max_events=args.max_events, max_bytes=args.max_bytes)
