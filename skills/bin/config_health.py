"""Bounded read-only checks for owned CLI wiring, agent config and skill links."""
import json
import os
from pathlib import Path
import shlex
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'bin'))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools.workflow.workflow_health import workflow_health_report
from cli_runtime import RUNTIME_RELATIVE, read_cli_manifest

CONFIG_LIMIT = 1024 * 1024


def read_health_config(path, *, toml=False):
    """Read one known configuration file; errors never include file contents."""
    try:
        if not path.is_file():
            return 'missing', {}
        if path.stat().st_size > CONFIG_LIMIT:
            return 'unknown', {}
        data = tomllib.loads(path.read_text()) if toml else json.loads(path.read_text())
        return ('ok', data) if isinstance(data, dict) else ('unknown', {})
    except (OSError, ValueError):
        return 'unknown', {}


def installed_health(home, repo, cfg, *, runtime=True):
    """Inspect only expected files and links. No server, auth, home scan or writes."""
    home, repo = Path(home), Path(repo)
    codex_home = home / '.codex'
    if home.resolve() == Path.home().resolve() and os.environ.get('CODEX_HOME'):
        codex_home = Path(os.environ['CODEX_HOME']).expanduser().resolve()
    rows = []

    def report(label, state):
        rows.append({'check': label, 'status': state})

    manifest = read_cli_manifest(home)
    if runtime:
        report('managed CLI manifest', 'ok' if manifest else 'missing')
        if manifest:
            node = Path(manifest.get('node', ''))
            report('managed Node executable', 'ok' if node.is_absolute() and node.is_file() and os.access(node, os.X_OK) else 'failed')
            for name in cfg['npm']:
                if name in manifest.get('unmanaged', []):
                    report(f'CLI runtime {name} external non-Node binary', 'unknown')
                    continue
                entry = manifest['commands'].get(name)
                launcher = home / RUNTIME_RELATIVE / 'bin' / name
                ok = isinstance(entry, str) and Path(entry).is_absolute() and Path(entry).is_file()
                ok = ok and launcher.is_file() and not launcher.is_symlink() and os.access(launcher, os.X_OK)
                if ok:
                    expected = ('#!/bin/sh\n# dotfiles managed CLI runtime\n'
                                + 'exec ' + shlex.join([str(node), entry]) + ' "$@"\n')
                    ok = launcher.stat().st_size < 65536 and launcher.read_text() == expected
                report(f'managed CLI launcher {name}', 'ok' if ok else 'missing')
            link = home / RUNTIME_RELATIVE / 'runtime-bin/node'
            report('managed rebuild Node shim', 'ok' if link.is_symlink() and link.resolve() == node else 'failed')
    shared = home / '.agents/skills'
    lock = json.loads((repo / 'skills/sources.lock.json').read_text())
    required = set(cfg['skills']['local'])
    required.update(entry['name'] for source in lock['sources'] for entry in source['skills'])
    required.update(p.parent.name for p in (repo / 'pi/skills').glob('*/SKILL.md'))
    for name in sorted(required):
        report(f'required shared skill {name}', 'ok' if (shared / name / 'SKILL.md').is_file() else 'missing')
    for agent in cfg['agents']:
        if agent in ('claude', 'pi'):
            directory = home / ('.claude/skills' if agent == 'claude' else '.pi/agent/skills')
            for name in sorted(required):
                report(f'{agent} required skill link {name}', 'ok' if (directory / name / 'SKILL.md').is_file() else 'missing')
        if agent == 'pi':
            for filename, target in (('blank-direction-gate.ts', 'pi-blank-direction.ts'), ('dotfiles-update.ts', 'pi-dotfiles-update.ts'), ('workflow-lifecycle.ts', 'pi-workflow-lifecycle.ts'), ('dotfiles-rules.ts', 'pi-dotfiles-rules.ts')):
                path = home / '.pi/agent/extensions' / filename
                report(f'pi owned extension {filename}', 'ok' if path.is_symlink() and path.resolve() == repo / 'skills/hooks' / target else 'missing')
            report('pi MCP registration capability', 'unknown')
            continue
        if agent == 'opencode':
            path = home / '.config/opencode/plugins/dotfiles-rules.ts'
            report('opencode owned rule loader', 'ok' if path.is_symlink() and path.resolve() == repo / 'skills/hooks/opencode-dotfiles-rules.ts' else 'missing')
            state, settings = read_health_config(home / '.config/opencode/opencode.json')
            source = repo / 'skills/hooks/opencode-dotfiles-rules.ts'
            groups = (settings.get('plugins'), settings.get('plugin'))
            entries = [entry for group in groups if isinstance(group, list) for entry in group]
            target = str(repo / 'skills/hooks/opencode-rules-plugin')
            registered = any(entry in (target, source.as_uri()) if isinstance(entry, str)
                             else isinstance(entry, dict) and entry.get('package') == target for entry in entries)
            report('opencode rule plugin registration', 'ok' if registered else 'missing')
        if agent not in ('claude', 'codex'):
            report(f'{agent} configuration adapter', 'unknown')
            continue
        settings_path = home / '.claude/settings.json' if agent == 'claude' else codex_home / 'hooks.json'
        state, settings = read_health_config(settings_path)
        report(f'{agent} hook configuration', state)
        hooks = settings.get('hooks', {})
        if not isinstance(hooks, dict):
            report(f'{agent} owned hooks', 'unknown')
        else:
            for event, owner, mode in (('SessionStart', repo / 'bin/dotfiles-update', '--hook'),
                                       ('SessionStart', repo / 'bin/dotfiles-health', '--hook'),
                                       ('SessionStart', repo / 'bin/agent-workflow-check', '--startup'),
                                       ('SessionStart', repo / 'skills/bin/dotfiles-rules', '--hook'),
                                       ('UserPromptSubmit', repo / 'skills/bin/dotfiles-rules', '--hook'),
                                       ('PreToolUse', repo / 'skills/hooks/blank-direction-gate', 'gate'),
                                       ('PostToolUse', repo / 'skills/hooks/blank-direction-gate', 'mark')):
                groups = hooks.get(event, [])
                found = False
                if isinstance(groups, list):
                    for group in groups:
                        if not isinstance(group, dict) or not isinstance(group.get('hooks'), list):
                            continue
                        for hook in group['hooks']:
                            if not isinstance(hook, dict) or not isinstance(hook.get('command'), str):
                                continue
                            try:
                                words = shlex.split(hook['command'])
                            except ValueError:
                                continue
                            if str(owner) in words and mode in words and owner.is_file() and os.access(owner, os.X_OK):
                                found = True
                report(f'{agent} owned hook {event}', 'ok' if found else 'missing')
            groups = hooks.get('PostToolUseFailure', [])
            if agent == 'claude':
                report('claude owned failure hook', 'ok' if isinstance(groups, list) and any(
                    isinstance(group, dict) and isinstance(group.get('hooks'), list) and any(
                        isinstance(hook, dict) and str(repo / 'skills/hooks/blank-direction-gate') in hook.get('command', '')
                        for hook in group['hooks']) for group in groups) else 'missing')
        config_path = home / '.claude.json' if agent == 'claude' else codex_home / 'config.toml'
        state, config = read_health_config(config_path, toml=agent == 'codex')
        report(f'{agent} MCP configuration', state)
        servers = config.get('mcpServers' if agent == 'claude' else 'mcp_servers', {})
        if not isinstance(servers, dict):
            report(f'{agent} MCP format', 'unknown')
            continue
        for name, binary, arguments in (('argent', 'argent', ['mcp']), ('agentation', 'agentation-mcp', ['server'])):
            server = servers.get(name)
            if not isinstance(server, dict):
                report(f'{agent} MCP {name}', 'missing' if state != 'unknown' else 'unknown')
                continue
            if server.get('enabled') is False:
                report(f'{agent} MCP {name}', 'failed')
                continue
            expected = str(home / RUNTIME_RELATIVE / 'bin' / binary)
            if server.get('command') == expected and server.get('args', []) == arguments:
                report(f'{agent} MCP {name}', 'ok')
            else:
                # Existing remote/custom registrations are retained, not treated as owned.
                report(f'{agent} MCP {name} unmanaged runtime', 'unknown')
        if agent == 'codex':
            # Presence does not verify Codex's computed trust digest. Native review owns that.
            report('codex native hook trust', 'unknown')
    # Startup checks inspect only installer-recorded paths, without scanning home.
    state, manifest = read_health_config(home / '.local/state/dotfiles/agent-profiles.json')
    recorded = manifest.get('profiles', {})
    if not isinstance(recorded, dict):
        recorded = {}
    for agent in ('codex', 'claude', 'grok', 'pi', 'opencode'):
        profiles = recorded.get(agent, [])
        if not isinstance(profiles, list) or len(profiles) > 128:
            report(f'{agent} profile manifest', 'unknown')
            continue
        for index, directory in enumerate(profiles, 1):
            if not isinstance(directory, str) or not Path(directory).is_absolute():
                report(f'{agent} profile manifest', 'unknown')
                continue
            profile = Path(directory)
            if agent in ('codex', 'claude', 'grok'):
                filename = {'codex': 'hooks.json', 'claude': 'settings.json', 'grok': 'hooks/blank-direction-gate.json'}[agent]
                state, settings = read_health_config(profile / filename)
                hooks = settings.get('hooks', {})
                for event in ('SessionStart', 'UserPromptSubmit'):
                    groups = hooks.get(event, []) if isinstance(hooks, dict) else []
                    found = isinstance(groups, list) and any(
                        isinstance(group, dict) and isinstance(group.get('hooks'), list) and any(
                            isinstance(hook, dict) and str(repo / 'skills/bin/dotfiles-rules') in hook.get('command', '')
                            for hook in group['hooks']) for group in groups)
                    report(f'{agent} profile {index} rule hook {event}', 'ok' if found else 'missing')
            elif agent == 'pi':
                path = profile / 'extensions/dotfiles-rules.ts'
                report(f'pi profile {index} rule loader', 'ok' if path.is_symlink() and path.resolve() == repo / 'skills/hooks/pi-dotfiles-rules.ts' else 'missing')
            else:
                path = profile / 'plugins/dotfiles-rules.ts'
                report(f'opencode profile {index} rule loader', 'ok' if path.is_symlink() and path.resolve() == repo / 'skills/hooks/opencode-dotfiles-rules.ts' else 'missing')
    # Only references explicitly named by owned rules are required.
    import re
    references = set()
    for rule in (repo / 'skills/rules/shared').glob('*.md'):
        references.update(re.findall(r'~/dotfiles/(skills/reference/[A-Za-z0-9._/-]+\.md)', rule.read_text()))
    for reference in sorted(references):
        report(f'required rule reference {reference}', 'ok' if (repo / reference).is_file() else 'missing')
    report_data = workflow_health_report(repo, home, cfg['agents'])
    for finding in report_data['findings']:
        report(finding, 'missing')
    report('bounded server/workflow configuration', 'ok' if report_data['healthy'] else 'failed')
    return rows
