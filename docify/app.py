from pathlib import Path
from time import sleep

from docify.cli import *
from docify.git import require_git, clone_repo, cleanup
from docify.error import handle

def run(work_dir: Path, results_dir: Path) -> None:
    print_banner()
    print("Paste a GitHub repository URL (example: https://github.com/psf/requests)\n")

    repo_path: Path | None = None

    try:
        require_git()

        repo_url = prompt_for_accessible_repo()
        print(f"\nRepository verified: {repo_url}\n")

        print("Cloning repository...")
        repo_path = clone_repo(repo_url, work_dir)
        print(f"Cloned into: {repo_path}\n")

        # Next: analyze -> generate -> results

    except Exception as e:
        handle(str(e), exit_program=True)

    finally:
        if repo_path is not None:
            try:
                print("Cleaning up temporary files...")
                cleanup(repo_path, work_dir)
                print("Cleanup complete\n")

                print("Done.")
            except Exception as e:
                handle(f"Cleanup failed: {e}", exit_program=True)

