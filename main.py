import os

from docify.error import handle_error
from docify.git.prompt import prompt_for_accessible_repo
from docify.git.validate import require_git
from docify.ui.banner import clear, print_banner

def main() -> None:
    clear()
    print_banner()
    print("Paste a GitHub repository URL (example: https://github.com/psf/requests)\n")

    try:
        require_git()
        repo_url = prompt_for_accessible_repo()

        print("Repository verified.")
        print(f"Ready to process {repo_url}")
    except Exception as e:
        handle_error(str(e), True)


if __name__ == '__main__':
    main()
