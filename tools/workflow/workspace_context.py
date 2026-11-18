"""Exact git workspace binding and input checks for private checkpoints."""

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit, unquote

from .private_state import WorkflowError

SECRET_PATTERNS = (
    r'\bsk-[A-Za-z0-9_-]{16,}\b',
    r'\b(?:sk|rk)_live_[A-Za-z0-9]{16,}\b',
    r'\b(?:gh[oprsu]_|github_pat_|npm_|hf_)[A-Za-z0-9_]{16,}\b',
    r'\bAIza[A-Za-z0-9_-]{16,}\b',
    r'\bxox[baprs]-[A-Za-z0-9-]{10,}\b',
    r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
    r'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----',
    r'\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b',
    r'\b(?:password|passwd|api[_-]?key|access[_-]?token|refresh[_-]?token|secret|cookie|authorization)\s*[=:]\s*\S+',
    r'\bBearer\s+[A-Za-z0-9_.~+/-]{8,}',
)
SECRET_REGEXES = tuple(re.compile(pattern, re.IGNORECASE) for pattern in SECRET_PATTERNS)
OPAQUE_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z')
CHECKPOINT_ID = re.compile(r'cp_[0-9a-f]{32}\Z')


def validate_context_text(value: object, label: str, maximum: int, *, multiline: bool = False) -> str:
    """Bound reviewed context and reject known secret shapes without printing them."""
    if not isinstance(value, str) or not value.strip() or len(value.encode('utf-8')) > maximum:
        raise WorkflowError('CHECKPOINT_INPUT', f'{label} must be non-empty and at most {maximum} bytes.')
    for character in value:
        code = ord(character)
        if ((code < 32 and not (multiline and character in '\n\t\r')) or 127 <= code <= 159
                or 0x202a <= code <= 0x202e or 0x2066 <= code <= 0x2069):
            raise WorkflowError('CHECKPOINT_INPUT', f'{label} contains unsafe control characters.')
    if any(pattern.search(value) for pattern in SECRET_REGEXES):
        raise WorkflowError('CHECKPOINT_SECRET', 'Checkpoint input contains a possible secret. Remove it before saving.')
    return value.strip()


def validate_session_id(value: object) -> str:
    """Accept an explicit session identity, never a path or an inferred recent transcript."""
    text = validate_context_text(value, 'Session', 128)
    if not OPAQUE_ID.fullmatch(text):
        raise WorkflowError('WORKFLOW_SESSION', 'Session must be an opaque identifier without path separators.')
    return text


def validate_checkpoint_id(value: object) -> str:
    """Keep direct checkpoint reads inside the selected session directory."""
    if not isinstance(value, str) or not CHECKPOINT_ID.fullmatch(value):
        raise WorkflowError('CHECKPOINT_ID', 'Checkpoint id must have the cp_ hexadecimal format.')
    return value


def git_workspace_value(worktree: Path, *arguments: str) -> str:
    """Read git metadata without invoking user shell configuration or changing the checkout."""
    try:
        result = subprocess.run(['git', '-C', str(worktree), *arguments], capture_output=True, text=True,
                                timeout=3, check=True)
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise WorkflowError('WORKFLOW_GIT', 'The exact git workspace could not be read.') from exc


@dataclass(frozen=True)
class WorkspaceBinding:
    repository: str
    worktree: str
    session: str

    @property
    def scope_digest(self) -> str:
        """Hash the exact repository, worktree, and session without broadening search."""
        raw = json.dumps(asdict(self), sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()

    def to_json(self) -> dict:
        return asdict(self)


def bind_git_workspace(worktree: Path, session: str) -> WorkspaceBinding:
    """Bind a checkpoint to the common git directory and this exact worktree root."""
    requested = worktree.expanduser().resolve(strict=True)
    root = Path(git_workspace_value(requested, 'rev-parse', '--show-toplevel')).resolve(strict=True)
    common = Path(git_workspace_value(root, 'rev-parse', '--path-format=absolute', '--git-common-dir')).resolve(strict=True)
    for path in (root, common):
        validate_context_text(str(path), 'Workspace path', 4096)
    return WorkspaceBinding(str(common), str(root), validate_session_id(session))


def capture_workspace_revision(binding: WorkspaceBinding) -> dict:
    """Record HEAD and working diff identity without storing diff or transcript contents."""
    root = Path(binding.worktree)
    head = git_workspace_value(root, 'rev-parse', '--verify', 'HEAD')
    status = git_workspace_value(root, 'status', '--porcelain=v1', '-uno')
    # Only a digest is retained. Untracked evidence is checked by explicit artifact links.
    try:
        diff = subprocess.run(['git', '-C', str(root), 'diff', '--no-ext-diff', '--no-textconv', 'HEAD', '--'],
                              capture_output=True, timeout=3, check=True).stdout
    except (OSError, subprocess.SubprocessError) as exc:
        raise WorkflowError('WORKFLOW_GIT', 'The working revision could not be read.') from exc
    digest = hashlib.sha256(status.encode() + b'\0' + diff).hexdigest()
    return {'head': head, 'working_digest': digest}


def validate_artifact_link(value: object, worktree: Path) -> dict:
    """Link existing evidence by path or safe HTTPS URL; never copy its body."""
    text = validate_context_text(value, 'Artifact', 4096)
    validate_context_text(unquote(text), 'Artifact', 4096)
    parsed = urlsplit(text)
    if parsed.scheme:
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.query:
            raise WorkflowError('CHECKPOINT_LINK', 'External artifacts require HTTPS without credentials or query strings.')
        return {'kind': 'url', 'target': text, 'freshness': 'recheck-source'}
    path = Path(text).expanduser()
    path = (worktree / path if not path.is_absolute() else path).resolve(strict=True)
    if not path.is_file() and not path.is_dir():
        raise WorkflowError('CHECKPOINT_LINK', 'Local artifacts must already exist.')
    forbidden = {'.env', 'kiys', 'auth.json', 'cookies.json', 'credentials.json'}
    if any(part.lower() in forbidden or part.lower().endswith(('.pem', '.key'))
           or part.lower().startswith('.env.') for part in path.parts):
        raise WorkflowError('CHECKPOINT_LINK', 'Credential files are not checkpoint artifacts.')
    stat = path.stat()
    return {'kind': 'file' if path.is_file() else 'directory', 'target': str(path),
            'mtime_ns': stat.st_mtime_ns, 'size': stat.st_size, 'freshness': 'recheck-source'}


def artifact_link_changed(link: dict) -> bool:
    """Mark changed or missing evidence explicitly; external sources always need a live recheck."""
    if link['kind'] == 'url':
        return False
    try:
        stat = Path(link['target']).stat()
        return stat.st_mtime_ns != link['mtime_ns'] or stat.st_size != link['size']
    except OSError:
        return True
