import json
from pathlib import Path
from datetime import datetime

def write_results(results_dir: Path, analysis, owner: str, repo: str) -> Path:
    """
    Writes analysis outputs for a single run and returns the final output path.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    output_path = results_dir / owner / repo / timestamp
    output_path.mkdir(parents=True, exist_ok=True)

    # Write tree
    (output_path / "tree.txt").write_text(
        analysis.tree.text,
        encoding="utf-8"
    )

    # Write stats
    stats_json = {
        "Total Files": analysis.stats.total_files,
        "Total Directories": analysis.stats.total_dirs,
        "Total_Lines": analysis.stats.total_lines,
        "Languages": analysis.stats.languages,
    }

    (output_path / "stats.json").write_text(
        json.dumps(stats_json, indent=2),
        encoding="utf-8"
    )

    # Write analysis

    return output_path
