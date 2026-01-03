from __future__ import annotations

import os
import shutil
import stat
import time
from pathlib import Path

from .shell import run


def repo_parts_from_url(url: str) -> tuple[str, str]:
    """
    URL is guaranteed normalized:
      https://github.com/<owner>/<repo>.git

    Returns (owner, repo).
    """
    url = url.strip().rstrip("/")
    parts = url.split("/")

    # Expect: ['https:', '', 'github.com', '<owner>', '<repo>.git']
    if len(parts) != 5 or parts[0] != "https:" or parts[2] != "github.com":
        raise ValueError(f"Unexpected normalized GitHub URL format: {url!r}")

    owner = parts[3]
    repo_git = parts[4]

    if not repo_git.endswith(".git"):
        raise ValueError(f"Expected .git suffix in URL: {url!r}")

    repo = repo_git[:-4]

    if not owner or not repo:
        raise ValueError(f"Invalid owner/repo in URL: {url!r}")

    return owner, repo


def repo_name_from_url(url: str) -> str:
    """
    Extract repo name from normalized GitHub URL.
    Example: https://github.com/owner/repo.git -> repo
    """
    _, repo = repo_parts_from_url(url)
    return repo


def _on_rm_error(func, path, exc_info) -> None:
    """
    shutil.rmtree onerror handler:
    - clears read-only bit
    - retries the failed operation once
    """
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        # Let the caller handle retries / final failure
        raise


def safe_rmtree(path: Path, *, retries: int = 8, delay: float = 0.15) -> None:
    """
    Robust directory delete for Windows file-locking scenarios.
    Retries multiple times to get past OneDrive/AV locks.
    """
    if not path.exists():
        return

    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            shutil.rmtree(path, onerror=_on_rm_error)
            return
        except Exception as e:
            last_err = e
            # Small backoff; locks often clear quickly
            time.sleep(delay * (attempt + 1))

    raise RuntimeError(f"Failed to remove {path} after {retries} attempts: {last_err}") from last_err


def clone_repo(url: str, work_dir: Path) -> Path:
    """
    Clone repository into work_dir/<owner>/<repo>.
    If the destination already exists, it will be removed and replaced.
    Returns the path to the cloned repository.
    """
    work_dir = work_dir.resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    owner, repo = repo_parts_from_url(url)
    dest = (work_dir / owner / repo).resolve()

    # Safety: ensure dest is inside work_dir
    try:
        dest.relative_to(work_dir)
    except ValueError:
        raise RuntimeError("Refusing to operate outside of work directory.")

    # Replace existing directory (robust on Windows)
    if dest.exists():
        safe_rmtree(dest)

    # Ensure parent dirs exist (work_dir/owner)
    dest.parent.mkdir(parents=True, exist_ok=True)

    code, out, err = run(["git", "clone", "--depth", "1", url, str(dest)])
    if code != 0:
        raise RuntimeError((err or out).strip() or "Failed to clone repository.")

    return dest


def cleanup(dest: Path, allowed_root: Path) -> None:
    """
    Safely remove dest directory, only if it's inside allowed_root.
    """
    dest = dest.resolve()
    allowed_root = allowed_root.resolve()

    try:
        dest.relative_to(allowed_root)
    except ValueError:
        raise RuntimeError("Refusing to delete outside of work directory.")

    safe_rmtree(dest)
