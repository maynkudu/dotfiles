"""Linux process identities, pidfd signals, and bounded descendant/listener reads."""

import ctypes
from dataclasses import asdict, dataclass
import errno
import os
from pathlib import Path
import signal
import sys

from .private_state import WorkflowError

MAX_PROCESSES = 32768
MAX_DESCENDANTS = 512


@dataclass(frozen=True)
class ProcessIdentity:
    pid: int
    start_ticks: int
    boot_id: str
    uid: int

    def to_json(self) -> dict:
        return asdict(self)

    @classmethod
    def from_json(cls, value: object):
        if (not isinstance(value, dict) or set(value) != {'pid', 'start_ticks', 'boot_id', 'uid'}
                or any(type(value[key]) is not int or value[key] < 0 for key in ('pid', 'start_ticks', 'uid'))
                or value['pid'] <= 1 or not isinstance(value['boot_id'], str) or len(value['boot_id']) != 36):
            raise WorkflowError('SERVER_STATE_INVALID', 'Server process identity is invalid.')
        return cls(**value)


@dataclass(frozen=True)
class ProcessSnapshot:
    identity: ProcessIdentity
    parent_pid: int
    group_pid: int
    session_pid: int
    rss_bytes: int
    state: str


def require_linux_process_support() -> None:
    """Fail safely before server mutations on unsupported hosts or kernels."""
    if sys.platform != 'linux' or not hasattr(os, 'pidfd_open') or not hasattr(signal, 'pidfd_send_signal'):
        raise WorkflowError('SERVER_UNSUPPORTED', 'Managed servers require Linux /proc and pidfd support. No process was changed.')


def read_linux_process(pid: int) -> ProcessSnapshot | None:
    """Read process start identity and RSS without reading command lines or environment."""
    require_linux_process_support()
    folder = Path('/proc') / str(pid)
    try:
        raw = (folder / 'stat').read_text()
        fields = raw[raw.rfind(')') + 2:].split()
        # /proc stat field 3 begins at index zero. Field 22 is process start time.
        boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
        identity = ProcessIdentity(pid, int(fields[19]), boot, folder.stat().st_uid)
        return ProcessSnapshot(identity, int(fields[1]), int(fields[2]), int(fields[3]),
                               max(0, int(fields[21])) * os.sysconf('SC_PAGE_SIZE'), fields[0])
    except (FileNotFoundError, ProcessLookupError):
        return None
    except (PermissionError, ValueError, IndexError, OSError) as exc:
        raise WorkflowError('SERVER_PROCESS_UNKNOWN', 'A process identity could not be read. It remains protected.') from exc


def process_identity_alive(identity: ProcessIdentity) -> bool:
    """A reused PID or zombie is not the recorded owner."""
    current = read_linux_process(identity.pid)
    return current is not None and current.identity == identity and current.state not in ('Z', 'X')


def signal_verified_process(identity: ProcessIdentity, signum: int) -> bool:
    """Pin a pidfd, then recheck identity so PID reuse cannot target an unrelated process."""
    require_linux_process_support()
    try:
        descriptor = os.pidfd_open(identity.pid)
    except ProcessLookupError:
        return False
    except OSError as exc:
        raise WorkflowError('SERVER_SIGNAL_UNAVAILABLE', 'The process could not be pinned for safe signaling.') from exc
    try:
        if identity.uid != os.getuid() or not process_identity_alive(identity):
            return False
        signal.pidfd_send_signal(descriptor, signum)
        return True
    except ProcessLookupError:
        return False
    finally:
        os.close(descriptor)


def current_ancestor_identity(pid: int) -> ProcessIdentity:
    """Require a live current ancestor as owner, not an arbitrary session/PID claim."""
    requested = read_linux_process(pid)
    if requested is None or requested.identity.uid != os.getuid() or requested.state in ('Z', 'X'):
        raise WorkflowError('SERVER_OWNER', 'The owner must be a live process of the current user.')
    current_pid = os.getpid()
    for _ in range(64):
        current = read_linux_process(current_pid)
        if current is None:
            break
        if current_pid == pid:
            return requested.identity
        if current.parent_pid <= 1 or current.parent_pid == current_pid:
            break
        current_pid = current.parent_pid
    raise WorkflowError('SERVER_OWNER', 'The owner PID must be the current harness or another stable current ancestor.')


def read_process_descendants(root: ProcessIdentity) -> dict[int, ProcessSnapshot]:
    """Walk only this process's child links, including detached process groups."""
    if not process_identity_alive(root):
        return {}
    output = {}
    pending = [root.pid]
    while pending:
        pid = pending.pop()
        if pid in output:
            continue
        current = read_linux_process(pid)
        if current is None or current.identity.uid != root.uid:
            continue
        output[pid] = current
        if len(output) >= MAX_DESCENDANTS:
            raise WorkflowError('SERVER_TREE_INCOMPLETE', 'The owned process tree exceeds 512 processes. Cleanup remains incomplete.')
        try:
            children = (Path('/proc') / str(pid) / 'task' / str(pid) / 'children').read_text().split()
            pending.extend(int(child) for child in children)
        except (FileNotFoundError, ProcessLookupError):
            continue
        except (OSError, ValueError) as exc:
            raise WorkflowError('SERVER_TREE_INCOMPLETE', 'Owned child process links could not be read safely.') from exc
    if not process_identity_alive(root):
        return {}
    return output


def enable_child_subreaper() -> None:
    """Adopt orphaned descendants so even double-forked children remain supervised."""
    require_linux_process_support()
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER
        raise WorkflowError('SERVER_UNSUPPORTED', 'Linux child supervision is unavailable. No server was launched.')


def current_process_inventory() -> tuple[dict[int, ProcessSnapshot], int]:
    """Read-only current process inventory; unreadable processes are counted, never inferred absent."""
    require_linux_process_support()
    output, unreadable = {}, 0
    folders = [path for path in Path('/proc').iterdir() if path.name.isdigit()]
    if len(folders) > MAX_PROCESSES:
        raise WorkflowError('SERVER_INVENTORY_INCOMPLETE', 'Process inventory exceeds the bounded limit.')
    for folder in folders:
        try:
            current = read_linux_process(int(folder.name))
            if current:
                output[current.identity.pid] = current
        except WorkflowError:
            unreadable += 1
    return output, unreadable


def read_listener_inodes() -> dict[int, set[str]]:
    """Collect current TCP LISTEN sockets from this network namespace, not route history."""
    require_linux_process_support()
    output = {}
    try:
        for filename in ('tcp', 'tcp6'):
            for line in (Path('/proc/net') / filename).read_text().splitlines()[1:]:
                fields = line.split()
                if fields[3] == '0A':
                    port = int(fields[1].rsplit(':', 1)[1], 16)
                    output.setdefault(port, set()).add(fields[9])
    except (OSError, ValueError, IndexError) as exc:
        raise WorkflowError('SERVER_INVENTORY_INCOMPLETE', 'Current TCP listener state could not be read.') from exc
    return output


def identify_listener_processes(port: int, candidates: dict[int, ProcessSnapshot],
                                 inodes: dict[int, set[str]] | None = None) -> tuple[list[ProcessSnapshot], int]:
    """Match listener socket inodes to verified processes without exposing their arguments."""
    wanted = (inodes if inodes is not None else read_listener_inodes()).get(port, set())
    matches, unreadable = [], 0
    if not wanted:
        return matches, unreadable
    for pid, snapshot in candidates.items():
        try:
            files = (Path('/proc') / str(pid) / 'fd').iterdir()
            matched = False
            for file in files:
                try:
                    target = os.readlink(file)
                    if target.startswith('socket:[') and target[8:-1] in wanted:
                        matched = True
                        break
                except (FileNotFoundError, ProcessLookupError):
                    continue
            if matched and process_identity_alive(snapshot.identity):
                matches.append(snapshot)
        except (FileNotFoundError, ProcessLookupError):
            continue
        except OSError:
            unreadable += 1
    return matches, unreadable


def process_working_directory(identity: ProcessIdentity) -> Path | None:
    """Verify the exact app directory before read-only reuse of an untracked server."""
    try:
        folder = Path(os.readlink(Path('/proc') / str(identity.pid) / 'cwd')).resolve()
        return folder if process_identity_alive(identity) else None
    except OSError:
        return None
