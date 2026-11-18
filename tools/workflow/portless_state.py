"""Read-only Portless state, deterministic names, and current listener inventory."""

import hashlib
import json
import os
from pathlib import Path
import re
import stat

from .linux_process import (current_process_inventory, identify_listener_processes,
                            read_listener_inodes, read_linux_process)
from .private_state import WorkflowError
from .workspace_context import WorkspaceBinding, git_workspace_value, validate_context_text

MAX_ROUTES = 256


def read_portless_file(path: Path, *, maximum: int = 128 * 1024) -> str | None:
    """Read bounded metadata without changing shared Portless state or revealing its raw contents."""
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise WorkflowError('PORTLESS_STATE_UNKNOWN', 'Portless metadata could not be opened safely.') from exc
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_size > maximum:
            raise WorkflowError('PORTLESS_STATE_UNKNOWN', 'Portless metadata is not a bounded regular file.')
        with os.fdopen(descriptor, 'rb', closefd=False) as stream:
            raw = stream.read(maximum + 1)
        if len(raw) > maximum:
            raise WorkflowError('PORTLESS_STATE_UNKNOWN', 'Portless metadata exceeds its read limit.')
        return raw.decode('utf-8')
    except UnicodeError as exc:
        raise WorkflowError('PORTLESS_STATE_UNKNOWN', 'Portless metadata is not valid UTF-8.') from exc
    finally:
        os.close(descriptor)


def portless_state_directory(value: Path | None = None) -> Path:
    return (value or Path(os.environ.get('PORTLESS_STATE_DIR', Path.home() / '.portless'))).expanduser().resolve()


def read_portless_routes(directory: Path) -> list[dict]:
    """Keep dead aliases visible as conflicts; routes alone never prove a current listener."""
    raw = read_portless_file(directory / 'routes.json')
    if raw is None:
        return []
    try:
        values = json.loads(raw)
    except ValueError as exc:
        raise WorkflowError('PORTLESS_STATE_UNKNOWN', 'Portless routes are malformed. Do not assume the collection is empty.') from exc
    if not isinstance(values, list) or len(values) > MAX_ROUTES:
        raise WorkflowError('PORTLESS_STATE_UNKNOWN', 'Portless route inventory is invalid or exceeds 256 routes.')
    routes = []
    names = set()
    for value in values:
        if (not isinstance(value, dict) or type(value.get('pid')) is not int or value['pid'] < 0
                or type(value.get('port')) is not int or not 0 < value['port'] < 65536
                or not isinstance(value.get('hostname'), str)
                or not re.fullmatch(r'[a-z0-9][a-z0-9.-]{0,252}', value['hostname'])
                or value['hostname'] in names):
            raise WorkflowError('PORTLESS_STATE_UNKNOWN', 'Portless route metadata is invalid. Existing routes remain protected.')
        names.add(value['hostname'])
        routes.append({key: value[key] for key in ('hostname', 'port', 'pid')})
    return routes


def read_portless_proxy(directory: Path) -> dict:
    """Read the existing proxy configuration; never start, stop, or replace the shared proxy."""
    try:
        pid = int(read_portless_file(directory / 'proxy.pid') or '0')
        port = int(read_portless_file(directory / 'proxy.port') or '0')
        tls = (read_portless_file(directory / 'proxy.tls') or '').strip() == '1'
        lan = (read_portless_file(directory / 'proxy.lan') or '').strip() == '1'
        tld = (read_portless_file(directory / 'proxy.tld') or 'localhost').strip()
    except ValueError as exc:
        raise WorkflowError('PORTLESS_STATE_UNKNOWN', 'Portless proxy metadata is invalid.') from exc
    snapshot = read_linux_process(pid) if pid > 1 else None
    listeners = read_listener_inodes()
    alive = snapshot is not None and snapshot.state not in ('Z', 'X')
    return {'pid': pid, 'port': port, 'tls': tls, 'lan': lan, 'tld': tld,
            'live': alive and bool(identify_listener_processes(port, {pid: snapshot})[0]) if snapshot else False}


def require_ready_portless_proxy(directory: Path) -> dict:
    """Fail before launch if using Portless would create or reconfigure a global proxy."""
    proxy = read_portless_proxy(directory)
    if not proxy['live']:
        raise WorkflowError('PORTLESS_PROXY_UNAVAILABLE', 'Start or repair the named Portless proxy explicitly. This helper does not change it.')
    if proxy['lan'] or proxy['tld'] != 'localhost':
        raise WorkflowError('PORTLESS_PROXY_UNSUPPORTED', 'This helper currently supports loopback .localhost routes only. The shared proxy remains unchanged.')
    return proxy


def named_portless_url(hostname: str, proxy: dict) -> str:
    protocol = 'https' if proxy['tls'] else 'http'
    standard = 443 if proxy['tls'] else 80
    suffix = '' if proxy['port'] == standard else f":{proxy['port']}"
    return f'{protocol}://{hostname}{suffix}'


def sanitize_name_label(value: str) -> str:
    label = re.sub(r'-+', '-', re.sub(r'[^a-z0-9-]', '-', value.lower())).strip('-')
    if len(label) > 63:
        label = label[:56].rstrip('-') + '-' + hashlib.sha256(label.encode()).hexdigest()[:6]
    return label


def validate_named_app(value: str) -> str:
    if (len(value) > 240 or not all(re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', part)
                                  for part in value.split('.'))):
        raise WorkflowError('PORTLESS_NAME', 'The configured app name must be a valid lowercase DNS name.')
    return value


def read_app_config(path: Path) -> dict:
    raw = read_portless_file(path)
    if raw is None:
        return {}
    try:
        output = json.loads(raw)
    except ValueError as exc:
        raise WorkflowError('PORTLESS_CONFIG', 'App configuration is malformed. Resolve it before launching.') from exc
    if not isinstance(output, dict):
        raise WorkflowError('PORTLESS_CONFIG', 'App configuration must be a JSON object.')
    return output


def derive_portless_app(binding: WorkspaceBinding, app_directory: Path) -> dict:
    """Use a configured name, else the repository name; let Portless apply its worktree prefix."""
    root = Path(binding.worktree)
    app = app_directory.expanduser().resolve(strict=True)
    if not app.is_dir() or not app.is_relative_to(root):
        raise WorkflowError('SERVER_SCOPE', 'The app directory must be inside the exact worktree.')
    config = read_app_config(app / 'portless.json')
    package = read_app_config(app / 'package.json')
    if not config and 'portless' in package:
        value = package['portless']
        config = {'name': value} if isinstance(value, str) else value
        if not isinstance(config, dict):
            raise WorkflowError('PORTLESS_CONFIG', 'The package Portless setting is invalid.')
    if not config and app != root:
        top = read_app_config(root / 'portless.json')
        if top.get('worktree'):
            raise WorkflowError('PORTLESS_CONFIG', 'Custom workspace worktree naming needs a verified adapter before managed launch.')
        if isinstance(top.get('apps'), dict):
            config = top['apps'].get(app.relative_to(root).as_posix(), {})
        if not config:
            raise WorkflowError('PORTLESS_CONFIG', 'Pin this package name in its existing app config before launching.')
    if 'apps' in config:
        raise WorkflowError('PORTLESS_CONFIG', 'Select one app directory. Managed startup does not launch an entire monorepo.')
    if config.get('appPort') is not None or config.get('proxy') is False or config.get('worktree'):
        raise WorkflowError('PORTLESS_CONFIG', 'Managed apps need Portless-assigned ports and default worktree naming; custom naming needs a verified adapter.')
    if os.environ.get('PORTLESS_PREFIX') is not None:
        raise WorkflowError('PORTLESS_CONFIG', 'Unset custom worktree-prefix overrides before managed startup.')
    base = config.get('name')
    if base is None:
        # A linked worktree's temporary directory is not the original repository name.
        repository_root = Path(binding.repository).parent
        base = sanitize_name_label(repository_root.name)
    if not isinstance(base, str):
        raise WorkflowError('PORTLESS_NAME', 'The configured app name is invalid.')
    base = validate_named_app(base)
    git_dir = git_workspace_value(root, 'rev-parse', '--path-format=absolute', '--git-dir')
    prefix = ''
    if Path(git_dir).resolve() != Path(binding.repository):
        branch = git_workspace_value(root, 'rev-parse', '--abbrev-ref', 'HEAD')
        if branch not in ('HEAD', 'main', 'master'):
            prefix = sanitize_name_label(branch.split('/')[-1])
    effective = (prefix + '.' if prefix else '') + base
    validate_named_app(effective)
    return {'base_name': base, 'hostname': effective + '.localhost', 'app_directory': str(app)}


def portless_listener_inventory(directory: Path) -> dict:
    """Report current routes, listeners and RSS without command-line secrets or cleanup."""
    routes = read_portless_routes(directory)
    proxy = read_portless_proxy(directory)
    snapshots, unreadable = current_process_inventory()
    inodes = read_listener_inodes()
    output = []
    for route in routes:
        listeners, skipped = identify_listener_processes(route['port'], snapshots, inodes)
        root = snapshots.get(route['pid'])
        tree = {root.identity.pid} if root else set()
        changed = True
        while changed:
            changed = False
            for pid, snapshot in snapshots.items():
                if pid not in tree and snapshot.parent_pid in tree:
                    tree.add(pid)
                    changed = True
        rss = sum(snapshots[pid].rss_bytes for pid in tree)
        output.append({'url': named_portless_url(route['hostname'], proxy), 'hostname': route['hostname'],
                       'port': route['port'], 'route_kind': 'alias' if route['pid'] == 0 else 'process',
                       'route_process_live': root is not None and root.state not in ('Z', 'X'),
                       'current_listener': route['port'] in inodes,
                       'listeners': [{'identity': value.identity.to_json(), 'rss_bytes': value.rss_bytes}
                                     for value in listeners],
                       'route_tree_rss_bytes': rss, 'route_tree_processes': len(tree),
                       'listener_processes_unreadable': skipped, 'cleanup_eligible': False})
    return {'mode': 'read-only', 'proxy': proxy, 'routes': output, 'processes_unreadable': unreadable,
            'warning': 'A route or RSS measurement does not establish cleanup ownership. Unknown servers remain untouched.'}
