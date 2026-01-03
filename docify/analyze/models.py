from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

@dataclass(frozen=True)
class RepoTree:
    text: str
    file_count: int
    dir_count: int

@dataclass(frozen=True)
class RepoStats:
    total_files: int
    total_dirs: int
    total_bytes: int
    total_lines: int
    languages: dict[str, dict[str, int]]  # lang -> {files, lines, bytes}

@dataclass(frozen=True)
class AnalysisResult:
    root: str
    tree: RepoTree
    stats: RepoStats

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def rel(root: Path, p: Path) -> str:
        return p.resolve().relative_to(root.resolve()).as_posix()

