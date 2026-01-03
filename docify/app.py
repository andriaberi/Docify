from pathlib import Path

from docify.cli import *
from docify.git import require_git, clone_repo, cleanup
from docify.error import handle
from docify.analyze import *
from docify.output import *

def run(work_dir: Path, results_dir: Path) -> None:
    print_banner()
    print("Paste a GitHub repository URL (example: https://github.com/psf/requests)\n")

    root: Path | None = None

    try:
        require_git()

        repo_url = prompt_for_accessible_repo()
        print(f"\nRepository verified: {repo_url}\n")

        print("Cloning repository...")
        root = clone_repo(repo_url, work_dir)
        print(f"Cloned into: {root}\n")

        # Get repo analysis
        print("Analyzing repository...")
        analysis = analyze_repo(root)
        print(f"Analysis complete.\n")

        # Return tree.txt + stats.json
        print("Writing output to file...")
        owner, repo = repo_url.split("/")[-2], repo_url.split("/")[-1].split(".")[0]
        output_path = write_results(results_dir, analysis, owner, repo)
        print(f"Written output to: {output_path}\n")

    except Exception as e:
        handle(str(e), exit_program=True)

    finally:
        if root is not None:
            try:
                print("Cleaning up temporary files...")
                cleanup(root, work_dir)
                print("Cleanup complete\n")

                print("Done.")
            except Exception as e:
                handle(f"Cleanup failed: {e}", exit_program=True)

