from docify.error.handler import handle
from docify.git import *


def prompt_for_accessible_repo(prompt: str = "> ") -> str:
    """
    Prompts until the user provides a GitHub repository URL that:
    - is valid
    - exists
    - is accessible with current git credentials
    Returns normalized HTTPS .git URL.
    """
    while True:
        raw = input(prompt).strip()

        if not raw:
            print("Please enter a GitHub repository URL.\n")
            continue

        try:
            url = normalize_github_url(raw)
            check_repo_access(url)
            return url
        except Exception as e:
            handle(str(e))
            print("Try again.\n")

    return ""

