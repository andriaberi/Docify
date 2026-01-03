from __future__ import annotations

from pathlib import Path

from .models import AnalysisResult
from .stats import get_stats
from .tree import build_tree


def analyze_repo(root: Path):
    tree = build_tree(root)
    stats = get_stats(root)

    return AnalysisResult(
        root = str(root),
        tree = tree,
        stats = stats
    )