"""Discover agent configuration profiles without walking their contents."""

import os
from pathlib import Path

AGENTS = ('codex', 'claude', 'grok', 'pi', 'opencode')
ENV_DIRS = {
    'codex': ('CODEX_HOME',),
    'claude': ('CLAUDE_CONFIG_DIR',),
    'grok': ('GROK_HOME', 'GROK_CONFIG_DIR'),
    'pi': ('PI_CODING_AGENT_DIR', 'PI_AGENT_DIR'),
    'opencode': ('OPENCODE_CONFIG_DIR',),
}


def agent_profile_dirs(home: Path, agent: str, *, include_default: bool = True) -> list[Path]:
    """Find existing prefix profiles and active overrides, keeping isolated homes isolated."""
    home = home.expanduser().resolve()
    default = home / ('.config/opencode' if agent == 'opencode' else f'.{agent}')
    if agent == 'pi':
        default /= 'agent'
    found = [default] if include_default else []
    for parent in (home, home / '.config'):
        if not parent.is_dir():
            continue
        for path in sorted(parent.iterdir()):
            name = path.name.removeprefix('.')
            if not name.startswith(agent) or not path.is_dir():
                continue
            # Avoid treating Pictures or pip caches as Pi configuration profiles.
            if agent == 'pi' and name != 'pi' and name[2:3] not in ('-', '_', '.'):
                continue
            found.append(path / 'agent' if agent == 'pi' else path)
    if home == Path.home().resolve():
        for key in ENV_DIRS[agent]:
            if os.environ.get(key):
                found.append(Path(os.environ[key]).expanduser())
        if agent == 'opencode' and os.environ.get('OPENCODE_CONFIG'):
            found.append(Path(os.environ['OPENCODE_CONFIG']).expanduser().parent)
    return list(dict.fromkeys(path.resolve() for path in found))


def discover_agent_profiles(home: Path, agents: list[str], *, include_existing: bool = False) -> dict[str, list[Path]]:
    """Selected agents get defaults; existing profiles can opt other supported agents in."""
    profiles = {}
    for agent in dict.fromkeys([*agents, *(AGENTS if include_existing else ())]):
        paths = agent_profile_dirs(home, agent, include_default=agent in agents)
        if paths:
            profiles[agent] = paths
    return profiles
