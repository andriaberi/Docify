from __future__ import annotations

from pathlib import Path

from docify.constants import DEFAULT_IGNORES
from .models import RepoTree


def build_tree(root: Path, max_depth: int = 1000, max_entries_per_dir: int = 1000, ignores: set[str] | None = None) -> RepoTree:
    """
    Builds a depth-limited, ignore-aware textual tree of a repository and returns
    the formatted tree along with file and directory counts.
    """

    # Fallback to default ignore set if none provided
    ignores = ignores or DEFAULT_IGNORES

    # Normalize root path for consistent traversal and output
    root = root.resolve()

    lines = [root.name + '/']
    file_count = 0
    dir_count = 0

    def walk(dir_path: Path, prefix: str = "", depth: int = 1) -> None:
        nonlocal file_count, dir_count

        # Hard stop to prevent runaway recursion on deep trees
        if depth > max_depth:
            return

        try:
            # Sort: directories first, then files; case-insensitive for stable output
            entries = sorted(dir_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except PermissionError:
            # Preserve tree structure even when access is denied
            lines.append(prefix + "└── [permission denied]")
            return

        # Apply ignore filter before counting / truncation
        entries = [e for e in entries if e.name not in ignores]

        truncated = False
        if len(entries) > max_entries_per_dir:
            entries = entries[:max_entries_per_dir]
            truncated = True

        for i, entry in enumerate(entries):
            last = i == len(entries) - 1
            branch = "└── " if last else "├── "
            next_prefix = prefix + ("    " if last else "│   ")

            if entry.is_dir():
                dir_count += 1
                lines.append(prefix + branch + entry.name + "/")
                walk(entry, next_prefix, depth + 1)
            else:
                file_count += 1
                lines.append(prefix + branch + entry.name)

        # Explicit marker to signal partial listing
        if truncated:
            lines.append(prefix + "└── … (truncated)")

    walk(root)

    return RepoTree(
        text='\n'.join(lines),
        file_count=file_count,
        dir_count=dir_count
    )