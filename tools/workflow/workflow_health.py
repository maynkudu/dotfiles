"""Bounded workflow install/reference checks, without process or transcript scanning."""

import json
import os
from pathlib import Path
import re
import tomllib

WORKFLOW_SKILLS = ('private-checkpoint', 'context-recall', 'reviewed-reflection', 'server-lifecycle',
                   'workflow-evaluation', 'workflow-health', 'skill-host-compat')
WORKFLOW_COMMANDS = ('agent-checkpoint', 'agent-server', 'agent-workflow-eval', 'agent-workflow-check')
WORKFLOW_REFERENCES = ('private-checkpoints.md', 'server-lifecycle.md', 'workflow-evaluation.md', 'workflow-hosts.md')
MAX_REFERENCE_BYTES = 32768
LEGACY_ROUTE_MARKER = '## Portable local workflow adapter'


def read_bounded_workflow_text(path: Path) -> str | None:
    """Bound startup reads and report invalid/unavailable files rather than guessing health."""
    try:
        if path.stat().st_size > MAX_REFERENCE_BYTES:
            return None
        with path.open(encoding='utf-8') as stream:
            return stream.read(MAX_REFERENCE_BYTES + 1)
    except (OSError, UnicodeError):
        return None


def check_workflow_repository(root: Path) -> list[str]:
    """Validate only this feature's commands, skills and required references."""
    findings = []
    for name in WORKFLOW_COMMANDS:
        command = root / 'bin' / name
        if not command.is_file() or not os.access(command, os.X_OK):
            findings.append(f'workflow command missing or not executable: bin/{name}')
    for filename in WORKFLOW_REFERENCES:
        if not (root / 'skills/reference' / filename).is_file():
            findings.append(f'workflow reference missing: {filename}')
    for name in WORKFLOW_SKILLS:
        path = root / 'skills/skills' / name / 'SKILL.md'
        text = read_bounded_workflow_text(path)
        if not text or not text.startswith('---\n') or '\n---\n' not in text[4:]:
            findings.append(f'workflow skill unavailable or malformed: {name}')
            continue
        frontmatter, body = text[4:].split('\n---\n', 1)
        metadata = {}
        for line in frontmatter.splitlines():
            key, separator, value = line.partition(':')
            if not separator or key in metadata or key not in ('name', 'description', 'license', 'metadata', 'allowed-tools'):
                findings.append(f'workflow skill has unsupported portable frontmatter: {name}')
                continue
            metadata[key] = value.strip()
        if metadata.get('name') != name or not metadata.get('description'):
            findings.append(f'workflow skill needs matching name and explicit description: {name}')
        for target in re.findall(r'\]\(([^)]+)\)', body):
            if not target.startswith(('https://', '#')) and not (path.parent / target.split('#', 1)[0]).resolve().exists():
                findings.append(f'workflow skill has an unresolved required reference: {name}')
        fences = re.findall(r'```(?:bash|sh|zsh)\n(.*?)```', body, re.DOTALL)
        if any(re.search(r'\$(?:ARGUMENTS|\{?(?:CLAUDE_|CURSOR_))', fence) for fence in fences):
            findings.append(f'workflow skill uses a host-only executable substitution: {name}')
    return findings


def check_workflow_installation(root: Path, home: Path, agents: list[str]) -> list[str]:
    """Check managed entries once at startup, preserving unrelated settings and hooks."""
    findings = []
    for name in WORKFLOW_COMMANDS:
        command = home / '.local/bin' / name
        if not command.is_file() or not os.access(command, os.X_OK) or command.resolve() != (root / 'bin' / name).resolve():
            findings.append(f'workflow launcher missing or not managed: {name}')
    for name in WORKFLOW_SKILLS:
        skill = home / '.agents/skills' / name / 'SKILL.md'
        if not skill.is_file() or skill.resolve() != (root / 'skills/skills' / name / 'SKILL.md').resolve():
            findings.append(f'workflow local skill missing or not managed: {name}')
    for agent in agents:
        if agent == 'pi':
            extension = home / '.pi/agent/extensions/workflow-lifecycle.ts'
            if not extension.is_file() or extension.resolve() != (root / 'skills/hooks/pi-workflow-lifecycle.ts').resolve():
                findings.append('Pi workflow lifecycle extension missing or not managed')
        elif agent in ('codex', 'claude'):
            config = home / ('.codex/hooks.json' if agent == 'codex' else '.claude/settings.json')
            raw = read_bounded_workflow_text(config)
            try:
                data = json.loads(raw) if raw else {}
                groups = data.get('hooks', {}).get('SessionStart', [])
                handlers = [handler for group in groups[:64] for handler in group.get('hooks', [])[:64]]
                if not any(str(root / 'bin/agent-workflow-check') in handler.get('command', '') for handler in handlers):
                    findings.append(f'{agent} bounded workflow startup hook missing')
            except (ValueError, AttributeError, TypeError):
                findings.append(f'{agent} workflow hook configuration unreadable or malformed')
    # These old copies remain usable only through the additive local routing patch.
    for name in ('recall', 'reflect'):
        path = home / '.agents/skills' / name / 'SKILL.md'
        if path.exists():
            text = read_bounded_workflow_text(path)
            if text is None or LEGACY_ROUTE_MARKER not in text:
                findings.append(f'legacy {name} host adapter patch pending; use its local replacement')
    return findings


def workflow_health_report(root: Path, home: Path, agents: list[str], *, repo_only: bool = False) -> dict:
    findings = check_workflow_repository(root)
    if not repo_only:
        findings.extend(check_workflow_installation(root, home, agents))
    return {'evidence': 'bounded-static-configuration-check', 'findings': findings,
            'complete': True, 'healthy': not findings,
            'limitations': ['No process inventory, transcript scan, MCP startup, network, or model call ran.',
                            'Codex/Claude thread-completion hooks are not verified. Explicit finalize and owner-death recovery apply.',
                            'Legacy Cursor bodies remain historical text; the local routing patch supplies the supported procedure.']}
