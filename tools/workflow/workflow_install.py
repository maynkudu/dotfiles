"""Standalone additive local workflow installation, without public downloads."""

from datetime import datetime, timezone
import os
from pathlib import Path
import shutil

from .workflow_health import WORKFLOW_COMMANDS, WORKFLOW_SKILLS


def install_workflow_links(root: Path, home: Path, agents: list[str], *, dry_run: bool = False) -> list[str]:
    """Install individually owned links while retaining unrelated commands and skills."""
    actions = []

    def link(source: Path, destination: Path):
        if destination.is_symlink() and destination.resolve() == source.resolve():
            return
        if destination.exists() or destination.is_symlink():
            actions.append(f'keep unrelated existing {destination}')
            return
        actions.append(f'link {destination} -> {source}')
        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(source)

    for name in WORKFLOW_COMMANDS:
        link(root / 'bin' / name, home / '.local/bin' / name)
    for name in WORKFLOW_SKILLS:
        source = root / 'skills/skills' / name
        shared = home / '.agents/skills' / name
        link(source, shared)
        for agent in agents:
            directory = {'claude': '.claude/skills', 'pi': '.pi/agent/skills', 'opencode': '.config/opencode/skills',
                         'grok': '.grok/skills'}.get(agent)
            if directory:
                link(shared, home / directory / name)
    return actions
