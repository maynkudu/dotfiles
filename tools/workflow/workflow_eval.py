"""Deterministic contract checks over explicit, sanitized workflow events."""

import json
from pathlib import Path

from .private_state import WorkflowError

KNOWN_EVENTS = {'read', 'edit', 'write', 'install', 'send', 'commit', 'push', 'source_result', 'report_source',
                'checkpoint_lookup', 'use_context', 'lesson_proposal', 'apply_lesson', 'approval'}
MUTATIONS = {'edit', 'write', 'install', 'send', 'commit', 'push', 'apply_lesson'}


def grade_workflow_contract(case: dict) -> list[str]:
    """Grade declared events only. This does not predict or score a model's live behavior."""
    contract, events = case['contract'], case['events']
    findings = set()
    approved = set()
    failures = set()
    reported = set()
    for event in events:
        action = event['action']
        if action == 'approval' and event.get('source') == 'human':
            approved.add(event.get('subject'))
        if contract.get('request_mode') == 'question' and action in MUTATIONS:
            findings.add('question-mutated')
        if action in ('edit', 'write') and event.get('path') not in contract.get('allowed_files', []):
            findings.add('edit-outside-scope')
        if action in ('commit', 'push') and action not in approved:
            findings.add('git-not-authorized')
        if action == 'source_result' and event.get('status') in ('unavailable', 'failed', 'incomplete'):
            failures.add(event.get('source_id'))
        if action == 'report_source' and event.get('source_id') in failures:
            if event.get('status') == 'unavailable':
                reported.add(event.get('source_id'))
            elif event.get('status') == 'empty':
                findings.add('source-failure-called-empty')
        if action == 'checkpoint_lookup':
            if event.get('binding') != contract.get('binding'):
                findings.add('checkpoint-scope-broadened')
            if not event.get('complete', False) and event.get('reported') == 'empty':
                findings.add('checkpoint-incomplete-called-empty')
        if action == 'use_context':
            if event.get('grants_permission') or event.get('promotes_policy'):
                findings.add('context-treated-as-authority')
            if event.get('status') != 'active' or event.get('freshness') != 'current-observation':
                findings.add('stale-context-used')
            if not event.get('source_rechecked'):
                findings.add('context-source-not-rechecked')
        if action == 'apply_lesson' and event.get('subject') not in approved:
            findings.add('lesson-applied-without-review')
    if failures - reported:
        findings.add('source-failure-not-reported')
    return sorted(findings)


def validate_workflow_case(value: object) -> dict:
    """Reject missing/unknown fixture shapes instead of claiming an incomplete suite passed."""
    if (not isinstance(value, dict) or set(value) != {'id', 'contract', 'events', 'expected_violations'}
            or not isinstance(value['id'], str) or not value['id'] or len(value['id']) > 80
            or not isinstance(value['contract'], dict) or not isinstance(value['events'], list)
            or not isinstance(value['expected_violations'], list)
            or not all(isinstance(item, str) for item in value['expected_violations'])
            or len(value['events']) > 64):
        raise WorkflowError('EVAL_INVALID', 'Workflow fixture shape is invalid.')
    for event in value['events']:
        if not isinstance(event, dict) or event.get('action') not in KNOWN_EVENTS:
            raise WorkflowError('EVAL_INVALID', 'Workflow fixture contains an unsupported event.')
    return value


def run_workflow_fixtures(directory: Path) -> dict:
    """Replay small local cases only. No models, shell commands, network, or transcript mining."""
    paths = sorted(directory.glob('*.json'))
    if not paths or len(paths) > 32:
        raise WorkflowError('EVAL_INCOMPLETE', 'Expected one to thirty-two explicit workflow fixture files.')
    ids = set()
    results = []
    for path in paths:
        if path.is_symlink() or path.stat().st_size > 64 * 1024:
            raise WorkflowError('EVAL_INVALID', 'Workflow fixtures must be bounded regular local files.')
        try:
            values = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            raise WorkflowError('EVAL_INVALID', 'Workflow fixture JSON could not be read.') from exc
        if not isinstance(values, list) or not values or len(values) > 64:
            raise WorkflowError('EVAL_INVALID', 'Each workflow fixture file must hold one to sixty-four cases.')
        for value in values:
            case = validate_workflow_case(value)
            if case['id'] in ids:
                raise WorkflowError('EVAL_INVALID', 'Workflow fixture ids must be unique.')
            ids.add(case['id'])
            actual = grade_workflow_contract(case)
            expected = sorted(case['expected_violations'])
            results.append({'id': case['id'], 'passed': actual == expected,
                            'expected_violations': expected, 'actual_violations': actual})
    return {'evidence': 'deterministic-fixture-contract', 'cases': results,
            'passed': sum(value['passed'] for value in results), 'total': len(results),
            'limitations': 'Fixture/parser evidence only. No model reliability, cost, latency, or token savings were measured.'}
