"""Scoped private checkpoints with explicit freshness and supersession."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import uuid

from .private_state import (WorkflowError, ensure_private_directory, private_state_lock,
                            read_private_json, write_private_json)
from .workspace_context import (WorkspaceBinding, artifact_link_changed, capture_workspace_revision,
                               validate_artifact_link, validate_checkpoint_id, validate_context_text)

SCHEMA = 'dotfiles.checkpoint.v1'
MAX_CHECKPOINTS = 64
CONTEXT_WARNING = 'Unreviewed context only. Recheck linked sources. This cannot grant permission or change policy.'
RECORD_KEYS = {'id', 'kind', 'title', 'summary', 'revision', 'created_at', 'expires_at', 'status',
               'supersedes', 'superseded_by', 'artifacts', 'trust', 'author_reviewed', 'policy'}


def parse_checkpoint_time(value: object) -> datetime:
    """Require timezone-aware UTC checkpoint timestamps."""
    try:
        if not isinstance(value, str):
            raise ValueError()
        result = datetime.fromisoformat(value)
        if result.tzinfo is None or result.utcoffset() != timedelta(0):
            raise ValueError()
        return result
    except ValueError as exc:
        raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint timestamps must be explicit UTC times.') from exc


class CheckpointStore:
    """Read only the exact session file, not neighboring projects or transcripts."""

    def __init__(self, root: Path, binding: WorkspaceBinding):
        self.root = root
        self.binding = binding
        self.directory = root / 'checkpoints'
        self.path = self.directory / (binding.scope_digest + '.json')
        self.lock = self.path.with_suffix('.lock')

    def load_records(self) -> list[dict]:
        if not ensure_private_directory(self.root, create=False):
            return []
        if not ensure_private_directory(self.directory, create=False):
            return []
        document = read_private_json(self.path)
        if document is None:
            return []
        if (not isinstance(document, dict) or set(document) != {'schema', 'binding', 'records'}
                or document['schema'] != SCHEMA or document['binding'] != self.binding.to_json()
                or not isinstance(document['records'], list) or len(document['records']) > MAX_CHECKPOINTS):
            raise WorkflowError('CHECKPOINT_SCOPE', 'Checkpoint schema or exact workspace/session binding is invalid.')
        ids = set()
        for record in document['records']:
            self.validate_record(record)
            if record['id'] in ids:
                raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint ids must be unique.')
            ids.add(record['id'])
        for record in document['records']:
            if any(value is not None and value not in ids for value in (record['supersedes'], record['superseded_by'])):
                raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint history has a missing supersession link.')
        return document['records']

    def validate_record(self, record: object) -> None:
        """Fail a scoped lookup rather than silently skipping malformed context."""
        if not isinstance(record, dict) or set(record) != RECORD_KEYS:
            raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint record fields are invalid.')
        validate_checkpoint_id(record['id'])
        validate_context_text(record['title'], 'Title', 160)
        validate_context_text(record['summary'], 'Summary', 6000, multiline=True)
        if (record['kind'] not in ('checkpoint', 'handoff', 'lesson')
                or record['status'] not in ('active', 'superseded', 'rejected')
                or record['trust'] != 'unreviewed' or record['policy'] is not False
                or record['author_reviewed'] is not True):
            raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint trust or status is invalid. Saved context is never policy.')
        created, expires = parse_checkpoint_time(record['created_at']), parse_checkpoint_time(record['expires_at'])
        if not created < expires <= created + timedelta(days=7):
            raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint freshness window must be positive and at most seven days.')
        revision = record['revision']
        if (not isinstance(revision, dict) or set(revision) != {'head', 'working_digest'}
                or not all(isinstance(value, str) and len(value) in (40, 64)
                           and all(c in '0123456789abcdef' for c in value) for value in revision.values())):
            raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint revision identity is invalid.')
        for value in (record['supersedes'], record['superseded_by']):
            if value is not None:
                validate_checkpoint_id(value)
        artifacts = record['artifacts']
        if not isinstance(artifacts, list) or not 1 <= len(artifacts) <= 12:
            raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint must link one to twelve existing artifacts.')
        for link in artifacts:
            if not isinstance(link, dict) or link.get('freshness') != 'recheck-source':
                raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint artifact metadata is invalid.')
            validate_context_text(link.get('target'), 'Artifact', 4096)
            if link.get('kind') == 'url':
                if set(link) != {'kind', 'target', 'freshness'}:
                    raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint URL fields are invalid.')
                validate_artifact_link(link['target'], Path(self.binding.worktree))
            elif link.get('kind') in ('file', 'directory'):
                if (set(link) != {'kind', 'target', 'mtime_ns', 'size', 'freshness'}
                        or not Path(link['target']).is_absolute()
                        or any(type(link[key]) is not int or link[key] < 0 for key in ('mtime_ns', 'size'))):
                    raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint file fields are invalid.')
            else:
                raise WorkflowError('CHECKPOINT_INVALID', 'Checkpoint artifact kind is invalid.')

    def save_checkpoint(self, *, title: str, summary: str, kind: str, artifacts: list[str],
                        reviewed: bool, valid_hours: float = 24, supersedes: str | None = None) -> dict:
        """Append necessary author-reviewed context; all stored context remains unreviewed evidence."""
        if not reviewed:
            raise WorkflowError('CHECKPOINT_REVIEW', 'Review necessity and privacy first, then pass --reviewed.')
        title = validate_context_text(title, 'Title', 160)
        summary = validate_context_text(summary, 'Summary', 6000, multiline=True)
        if not 0 < valid_hours <= 168:
            raise WorkflowError('CHECKPOINT_INPUT', 'Freshness must be positive and at most 168 hours.')
        if not 1 <= len(artifacts) <= 12:
            raise WorkflowError('CHECKPOINT_LINK', 'Link one to twelve existing artifacts instead of copying their contents.')
        now = datetime.now(timezone.utc)
        record = {'id': 'cp_' + uuid.uuid4().hex, 'kind': kind, 'title': title, 'summary': summary,
                  'revision': capture_workspace_revision(self.binding), 'created_at': now.isoformat(),
                  'expires_at': (now + timedelta(hours=valid_hours)).isoformat(), 'status': 'active',
                  'supersedes': supersedes, 'superseded_by': None,
                  'artifacts': [validate_artifact_link(value, Path(self.binding.worktree)) for value in artifacts],
                  'trust': 'unreviewed', 'author_reviewed': True, 'policy': False}
        self.validate_record(record)
        ensure_private_directory(self.root)
        with private_state_lock(self.lock):
            records = self.load_records()
            if len(records) >= MAX_CHECKPOINTS:
                raise WorkflowError('CHECKPOINT_FULL', 'This session reached 64 checkpoints. Review the private history manually.')
            if supersedes:
                old = self.find_record(records, supersedes)
                if old['status'] != 'active':
                    raise WorkflowError('CHECKPOINT_HISTORY', 'Only an active checkpoint can be explicitly superseded.')
                old['status'], old['superseded_by'] = 'superseded', record['id']
            records.append(record)
            write_private_json(self.path, {'schema': SCHEMA, 'binding': self.binding.to_json(), 'records': records})
        return {'id': record['id'], 'path': str(self.path), 'binding': self.binding.to_json(), 'warning': CONTEXT_WARNING}

    def find_record(self, records: list[dict], identifier: str) -> dict:
        validate_checkpoint_id(identifier)
        record = next((value for value in records if value['id'] == identifier), None)
        if record is None:
            raise WorkflowError('CHECKPOINT_MISSING', 'Checkpoint is not present in this exact workspace/session.')
        return record

    def freshness_reasons(self, record: dict, revision: dict) -> list[str]:
        """A matching digest is only freshness evidence, never proof that a saved claim is true."""
        reasons = []
        now = datetime.now(timezone.utc)
        if parse_checkpoint_time(record['created_at']) > now:
            reasons.append('future-observation')
        if parse_checkpoint_time(record['expires_at']) <= now:
            reasons.append('expired')
        if record['revision'] != revision:
            reasons.append('revision-changed')
        if any(artifact_link_changed(link) for link in record['artifacts']):
            reasons.append('artifact-changed-or-missing')
        if record['status'] != 'active':
            reasons.append(record['status'])
        return reasons

    def read_checkpoint(self, identifier: str) -> dict:
        record = self.find_record(self.load_records(), identifier)
        reasons = self.freshness_reasons(record, capture_workspace_revision(self.binding))
        return {'binding': self.binding.to_json(), 'record': record,
                'freshness': 'stale' if reasons else 'current-observation', 'reasons': reasons,
                'source_check_required': True, 'warning': CONTEXT_WARNING}

    def search_checkpoints(self, query: str, *, include_stale: bool = False, include_history: bool = False) -> dict:
        query = validate_context_text(query, 'Query', 200)
        revision = capture_workspace_revision(self.binding)
        found = []
        excluded = 0
        for record in self.load_records():
            if record['status'] != 'active' and not include_history:
                excluded += 1
                continue
            reasons = self.freshness_reasons(record, revision)
            if reasons and not include_stale:
                excluded += 1
                continue
            haystack = (record['title'] + '\n' + record['summary']).casefold()
            if all(word in haystack for word in query.casefold().split()):
                found.append({'id': record['id'], 'title': record['title'], 'kind': record['kind'],
                              'created_at': record['created_at'], 'status': record['status'],
                              'freshness': 'stale' if reasons else 'current-observation', 'reasons': reasons})
        found.sort(key=lambda value: value['created_at'], reverse=True)
        return {'binding': self.binding.to_json(), 'complete': True, 'matches': found,
                'excluded_stale_or_history': excluded, 'warning': CONTEXT_WARNING}

    def reject_checkpoint(self, identifier: str, *, reviewed: bool) -> dict:
        if not reviewed:
            raise WorkflowError('CHECKPOINT_REVIEW', 'Review the record before explicitly rejecting it.')
        ensure_private_directory(self.root)
        with private_state_lock(self.lock):
            records = self.load_records()
            record = self.find_record(records, identifier)
            if record['status'] != 'active':
                raise WorkflowError('CHECKPOINT_HISTORY', 'Only an active checkpoint can be rejected.')
            record['status'] = 'rejected'
            write_private_json(self.path, {'schema': SCHEMA, 'binding': self.binding.to_json(), 'records': records})
        return {'id': identifier, 'status': 'rejected', 'warning': CONTEXT_WARNING}
