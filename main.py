from __future__ import annotations

from pathlib import Path
from time import sleep

from docify.error import handle_error
from docify.ui.prompt import prompt_for_accessible_repo
from docify.git.validate import require_git
from docify.git.workspace import clone_repo, cleanup
from docify.ui.banner import clear, print_banner

BASE_DIR = Path(__file__).resolve().parent
WORK_DIR = BASE_DIR / ".work"


def main() -> None:
    clear()
    print_banner()
    print("Paste a GitHub repository URL (example: https://github.com/psf/requests)\n")

    dest: Path | None = None

    try:
        require_git()
        repo_url = prompt_for_accessible_repo()

        print("Repository verified.")
        print(f"Ready to process: {repo_url}\n")

        WORK_DIR.mkdir(parents=True, exist_ok=True)

        print(f"Cloning repository into {WORK_DIR} ...")
        # Expect clone_repo to return the destination Path it cloned into
        dest = clone_repo(repo_url, work_dir=WORK_DIR)
        print(f"Repository cloned to: {dest}\n")

        # Your processing step goes here
        sleep(2)

    except Exception as e:
        handle_error(str(e), True)

    finally:
        if dest is not None:
            try:
                print(f"Cleaning up: {dest} ...")
                cleanup(dest, allowed_root=WORK_DIR)
                print("Cleanup complete.")
            except Exception as e:
                handle_error(f"Cleanup failed: {e}", False)


if __name__ == "__main__":
    main()
