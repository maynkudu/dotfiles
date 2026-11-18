"""Owner-only state files and locks for local workflow commands."""

from contextlib import contextmanager
import json
import os
from pathlib import Path
import stat
import tempfile
import time


class WorkflowError(Exception):
    """Expose a stable error code without echoing private input."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def workflow_state_root(value: Path | None = None) -> Path:
    """Resolve workflow storage without following a caller-supplied symlink."""
    base = Path(os.environ.get('XDG_STATE_HOME', Path.home() / '.local/state'))
    return (value or base / 'dotfiles/workflow').expanduser().absolute()


def ensure_private_directory(path: Path, *, create: bool = True) -> bool:
    """Refuse shared or symlinked state directories instead of repairing their permissions."""
    for ancestor in [*reversed(path.parents), path]:
        if ancestor.is_symlink():
            raise WorkflowError('STATE_UNSAFE', 'Workflow storage cannot contain symlink directories.')
    if not path.exists():
        if not create:
            return False
        missing = []
        parent = path
        while not parent.exists():
            missing.append(parent)
            parent = parent.parent
        for folder in reversed(missing):
            try:
                folder.mkdir(mode=0o700)
            except FileExistsError:
                pass
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or not hasattr(os, 'getuid'):
        raise WorkflowError('STATE_UNSUPPORTED', 'Owner-only workflow storage requires a Unix filesystem.')
    if info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise WorkflowError('STATE_UNSAFE', 'Workflow storage must belong to the current user with mode 700.')
    return True


def verify_private_file(info: os.stat_result) -> None:
    """Reject shared, linked, or non-regular private state files."""
    if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
            or info.st_mode & 0o077 or info.st_nlink != 1):
        raise WorkflowError('STATE_UNSAFE', 'Workflow files must be owner-only regular files without hard links.')


def read_private_json(path: Path, *, maximum: int = 1024 * 1024) -> dict | list | None:
    """Read bounded private JSON, treating malformed or unreadable state as an error."""
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise WorkflowError('STATE_UNREADABLE', 'Workflow state could not be opened safely.') from exc
    try:
        verify_private_file(os.fstat(descriptor))
        with os.fdopen(descriptor, 'rb', closefd=False) as stream:
            raw = stream.read(maximum + 1)
        if len(raw) > maximum:
            raise WorkflowError('STATE_INCOMPLETE', 'Workflow state exceeds the bounded read limit.')

        def unique_keys(pairs):
            output = {}
            for key, value in pairs:
                if key in output:
                    raise ValueError('duplicate JSON key')
                output[key] = value
            return output

        return json.loads(raw.decode('utf-8'), object_pairs_hook=unique_keys)
    except (UnicodeError, ValueError) as exc:
        raise WorkflowError('STATE_INVALID', 'Workflow state is not valid unique-key UTF-8 JSON.') from exc
    finally:
        os.close(descriptor)


def write_private_json(path: Path, data: dict | list) -> None:
    """Atomically replace private JSON in a locked, owner-only directory."""
    ensure_private_directory(path.parent)
    if path.exists() or path.is_symlink():
        verify_private_file(path.lstat())
    descriptor, temporary = tempfile.mkstemp(prefix='.workflow-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            json.dump(data, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def private_state_lock(path: Path, *, timeout: float = 5):
    """Serialize state changes with a bounded flock that the OS releases on owner death."""
    try:
        import fcntl
    except ImportError as exc:
        raise WorkflowError('STATE_UNSUPPORTED', 'Workflow locking requires Unix flock support.') from exc
    ensure_private_directory(path.parent)
    try:
        descriptor = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    except OSError as exc:
        raise WorkflowError('STATE_UNSAFE', 'Workflow lock could not be opened safely.') from exc
    try:
        verify_private_file(os.fstat(descriptor))
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise WorkflowError('STATE_BUSY', 'Workflow state lock is busy. Retry the same scope.')
                time.sleep(min(0.05, max(0, deadline - time.monotonic())))
        yield
    finally:
        os.close(descriptor)
