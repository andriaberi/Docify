# Directory names that should never be traversed or counted
DEFAULT_IGNORES = {
    ".git", ".idea", ".vscode", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".tox", ".venv", "venv", "node_modules", "dist", "build",
    ".work", ".results",
}

# Mapping of programming languages to recognized file extensions / filenames
LANGUAGE_MAP = {
    "Python": [".py"],
    "JavaScript": [".js", ".mjs"],
    "TypeScript": [".ts", ".tsx"],
    "C": [".c"],
    "C++": [".cpp", ".cc", ".cxx", ".hpp", ".h"],
    "C#": [".cs"],
    "Java": [".java"],
    "Go": [".go"],
    "Rust": [".rs"],
    "PHP": [".php"],
    "Ruby": [".rb"],
    "Kotlin": [".kt"],
    "Swift": [".swift"],
    "Shell": [".sh", ".bash", ".zsh"],
    "PowerShell": [".ps1"],
    "Lua": [".lua"],
    "R": [".r"],
    "Dart": [".dart"],
    "Scala": [".scala"],
    "Perl": [".pl"],
    "HTML": [".html", ".htm"],
    "CSS": [".css"],
    "SCSS": [".scss"],
    "Vue": [".vue"],
    "Svelte": [".svelte"],
    "JSON": [".json"],
    "YAML": [".yml", ".yaml"],
    "TOML": [".toml"],
    "INI": [".ini", ".cfg"],
    "XML": [".xml"],
    "CSV": [".csv"],
    "Markdown": [".md"],
    "Text": [".txt"],
    "Docker": ["Dockerfile"],
    "Makefile": ["Makefile"],
    "CMake": [".cmake"],
    "Gradle": [".gradle"],
    "Bazel": [".bazel"],
    "Nix": [".nix"],
    "SQL": [".sql"],
}

SUPPORTED_LANGUAGES = [
    "Python",
    "JavaScript"
]

__all__ = [
    "DEFAULT_IGNORES",
    "LANGUAGE_MAP"
]