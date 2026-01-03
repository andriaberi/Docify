from __future__ import annotations

from pathlib import Path

from docify.constants import DEFAULT_IGNORES, LANGUAGE_MAP
from docify.error import handle
from .models import RepoStats


def get_file_lang(name: str) -> str | None:
    """
    Return language name for a filename based on its extension / known filenames.
    """
    if "." not in name:
        return None

    extension = "." + name.rsplit(".", 1)[-1].lower()

    for lang, exts in LANGUAGE_MAP.items():
        if extension in exts:
            return lang

    return None


def _count_lines_from_bytes(raw: bytes) -> int:
    """
    Best-effort line count from raw bytes.
    - Treat binary-ish files as 0 lines (common for images / archives / etc.)
    - Decode as UTF-8 with errors ignored to avoid crashes on mixed encodings.
    """
    if not raw:
        return 0

    # Quick binary sniff: null bytes early usually indicates non-text content
    if b"\x00" in raw[:1024]:
        return 0

    text = raw.decode("utf-8", errors="ignore")
    if not text:
        return 0

    # Count lines without splitlines() to avoid big intermediate lists
    lines = text.count("\n")
    if not text.endswith("\n"):
        lines += 1
    return lines


def get_stats(root: Path, ignores: set[str] | None = None) -> RepoStats:
    """
    Recursively analyze a repository and return aggregated statistics.
    """
    ignores = ignores or DEFAULT_IGNORES

    total_files = 0
    total_dirs = 0
    total_bytes = 0
    total_lines = 0
    languages: dict[str, dict[str, int]] = {}

    def walk(dir_path: Path) -> None:
        nonlocal total_files, total_dirs, total_bytes, total_lines, languages

        try:
            entries = sorted(dir_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except PermissionError:
            return
        except OSError as e:
            handle(str(e))
            return

        entries = [e for e in entries if e.name not in ignores]

        for entry in entries:
            if entry.is_dir():
                total_dirs += 1
                walk(entry)
                continue

            total_files += 1

            file_lang = get_file_lang(entry.name)
            if file_lang is None:
                continue

            try:
                raw = entry.read_bytes()
                byte_count = len(raw)
                line_count = _count_lines_from_bytes(raw)

                total_bytes += byte_count
                total_lines += line_count

                bucket = languages.get(file_lang)
                if bucket is None:
                    bucket = {"files": 0, "bytes": 0, "lines": 0}
                    languages[file_lang] = bucket

                bucket["files"] += 1
                bucket["bytes"] += byte_count
                bucket["lines"] += line_count

            except Exception as e:
                handle(str(e))

    root = root.resolve()
    walk(root)

    # Keep dict, but enforce deterministic "top languages first" ordering
    languages = {
        k: v
        for k, v in sorted(
            languages.items(),
            key=lambda item: (
                -item[1]["files"],
                -item[1]["lines"],
                -item[1]["bytes"],
                item[0],
            ),
        )
    }

    return RepoStats(
        total_files=total_files,
        total_dirs=total_dirs,
        total_bytes=total_bytes,
        total_lines=total_lines,
        languages=languages,
    )
