"""Private Node CLI launchers. Never replace an external binary or app runtime."""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess

RUNTIME_RELATIVE = '.local/share/dotfiles/cli'


def read_cli_manifest(home):
    """Read only the small managed CLI manifest, not user/provider settings."""
    path = Path(home) / RUNTIME_RELATIVE / 'runtime.json'
    try:
        if not path.is_file() or path.stat().st_size > 65536:
            return None
        data = json.loads(path.read_text())
        if not isinstance(data, dict) or data.get('version') != 1:
            return None
        if (not isinstance(data.get('commands'), dict)
                or not isinstance(data.get('node'), str) or not Path(data['node']).is_absolute()
                or not isinstance(data.get('abi'), str)
                or not isinstance(data.get('unmanaged', []), list)
                or any(not isinstance(name, str) for name in data.get('unmanaged', []))
                or any(not isinstance(key, str) or not isinstance(value, str) or not Path(value).is_absolute()
                       for key, value in data['commands'].items())):
            return None
        return data
    except (OSError, ValueError):
        return None


def node_runtime_info(node):
    """Probe Node version and ABI with a five second bound and no native imports."""
    result = subprocess.run([str(node), '-p', 'JSON.stringify({node:process.version,abi:process.versions.modules})'],
                            capture_output=True, text=True, timeout=5, check=True)
    info = json.loads(result.stdout)
    if not isinstance(info, dict) or not isinstance(info.get('node'), str) or not isinstance(info.get('abi'), str):
        raise ValueError('Managed CLI runtime probe returned invalid metadata')
    if int(info['node'].lstrip('v').split('.')[0]) < 24:
        raise ValueError('Managed CLI runtime requires Node 24 or newer')
    return info


def node_entrypoint(path):
    """Accept a JavaScript bin with a Node shebang; other runtimes stay unmanaged."""
    if not path:
        return None
    try:
        target = Path(path).resolve(strict=True)
        with target.open('rb') as stream:
            first = stream.readline(512).decode('utf-8', errors='replace')
        words = first.removeprefix('#!').strip().split()
        return target if first.startswith('#!') and any(Path(word).name == 'node' for word in words) else None
    except (OSError, RuntimeError):
        return None


def install_cli_runtime(home, binaries, search, node, *, dry_run=False):
    """Create private launchers using a fixed Node path, preserving all external bins."""
    home = Path(home)
    base = home / RUNTIME_RELATIVE
    manifest = read_cli_manifest(home)
    # A repeated install retains the selected runtime unless explicitly changed.
    selected = Path(node or (manifest or {}).get('node', '/usr/bin/node')).expanduser()
    if not selected.is_absolute() or not selected.is_file():
        raise ValueError('Managed CLI runtime needs an existing absolute Node path; use --cli-node')
    selected = selected.resolve()
    info = node_runtime_info(selected)
    commands, unmanaged = {}, []
    for binary in binaries:
        external = shutil.which(binary, path=search)
        entry = node_entrypoint(external) if external else None
        if entry:
            commands[binary] = str(entry)
        elif external:
            unmanaged.append(binary)
    data = {'version': 1, 'node': str(selected), 'node_version': info['node'],
            'abi': info['abi'], 'commands': commands, 'unmanaged': unmanaged}
    print(f"{'would configure' if dry_run else 'configure'} managed CLI Node {selected} ({info['node']}, ABI {info['abi']})")
    if dry_run:
        for binary in commands:
            print(f'would write managed launcher {base / "bin" / binary}')
        return
    # Refuse writes through links, including directories, even inside our namespace.
    paths_to_check = [base, base / 'runtime-bin', base / 'bin', base / 'runtime.json']
    paths_to_check.extend(parent for parent in base.parents if parent.is_relative_to(home) and parent != home)
    for path in paths_to_check:
        if path.is_symlink():
            raise ValueError('Managed CLI runtime path conflicts with an external symlink')
    for binary in commands:
        launcher = base / 'bin' / binary
        if launcher.exists() or launcher.is_symlink():
            if (launcher.is_symlink() or launcher.stat().st_size > 65536
                    or not launcher.read_text().startswith('#!/bin/sh\n# dotfiles managed CLI runtime\n')):
                raise ValueError(f'Managed CLI launcher conflict: {binary}')
    base.mkdir(parents=True, exist_ok=True)
    base.chmod(0o700)
    runtime_bin = base / 'runtime-bin'
    runtime_bin.mkdir(exist_ok=True)
    node_link = runtime_bin / 'node'
    if node_link.exists() or node_link.is_symlink():
        if not node_link.is_symlink():
            raise ValueError('Managed CLI runtime node path is occupied by an unmanaged file')
        if node_link.resolve() != selected:
            node_link.unlink()
    if not node_link.is_symlink():
        node_link.symlink_to(selected)
    manifest_path = base / 'runtime.json'
    text = json.dumps(data, indent=2) + '\n'
    if not manifest_path.exists() or manifest_path.read_text() != text:
        manifest_path.write_text(text)
    manifest_path.chmod(0o600)
    launcher_dir = base / 'bin'
    launcher_dir.mkdir(exist_ok=True)
    for binary, entry in commands.items():
        launcher = launcher_dir / binary
        # Do not prepend a Node shim to PATH. Portless and similar tools launch
        # app commands, whose Node selection must remain the user's selection.
        text = ('#!/bin/sh\n# dotfiles managed CLI runtime\n'
                + 'exec ' + shlex.join([str(selected), entry]) + ' "$@"\n')
        if launcher.exists() or launcher.is_symlink():
            if launcher.is_symlink() or not launcher.read_text().startswith('#!/bin/sh\n# dotfiles managed CLI runtime\n'):
                raise ValueError(f'Managed CLI launcher conflict: {binary}')
            if launcher.read_text() == text:
                launcher.chmod(0o755)
                continue
        launcher.write_text(text)
        launcher.chmod(0o755)


def managed_cli_command(home, binary):
    """Return a managed launcher only when its manifest and executable exist."""
    if Path(binary).name != binary or binary in ('', '.', '..'):
        return None
    manifest = read_cli_manifest(home)
    command = Path(home) / RUNTIME_RELATIVE / 'bin' / binary
    if manifest and binary in manifest['commands'] and command.is_file() and os.access(command, os.X_OK):
        return command
    return None


def mcp_registration_status(agent, name, env, *, timeout=5):
    """Use Codex's config-only get; classify absence separately from CLI errors."""
    command = [agent, 'mcp', 'get', name]
    if agent == 'codex':
        command.append('--json')
    try:
        result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return 'unknown'
    if result.returncode == 0:
        return 'present'
    # Do not treat arbitrary parse, permission or CLI failures as missing servers.
    error = (result.stdout + result.stderr).lower()
    if any(marker in error for marker in ('no mcp server named', 'no server named', 'no mcp server found')) or ('mcp server' in error and 'not found' in error):
        return 'missing'
    return 'unknown'
