import re
from .shell import run

def require_git() -> None:
    code, _, _ = run(["git", "--version"])
    if code != 0:
        raise Exception("Git is required but was not found in PATH.")

def normalize_github_url(url: str) -> str:
        """
        Accepts:
          - https://github.com/owner/repo
          - https://github.com/owner/repo.git
          - git@github.com:owner/repo
          - git@github.com:owner/repo.git
          - github.com/owner/repo
          - owner/repo

        Returns a cloneable HTTPS URL ending in .git
        """
        url = url.strip()

        # owner/repo shorthand
        if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", url):
            url = f"https://github.com/{url}"

        # github.com/owner/repo (no scheme)
        if url.startswith("github.com/"):
            url = "https://" + url

        # SSH → HTTPS
        m = re.match(r"git@github\.com:(.+?)(\.git)?$", url)
        if m:
            url = f"https://github.com/{m.group(1)}"

        # Basic validation
        if "github.com/" not in url:
            raise Exception("Invalid URL. Use: https://github.com/<owner>/<repo>")

        parts = url.split("github.com/")[-1].strip("/").split("/")
        if len(parts) < 2 or not parts[0] or not parts[1]:
            raise Exception("Invalid GitHub repository URL. Use: https://github.com/<owner>/<repo>")

        # Ensure .git suffix
        if not url.endswith(".git"):
            url = url.rstrip("/") + ".git"

        return url

def check_repo_access(url: str) -> None:
    """
    Checks repo exists + you have access (public OR private with your credentials).
    Uses `git ls-remote` (lightweight, no clone).
    """
    code, out, err = run(["git", "ls-remote", url])
    if code == 0:
        return

    msg = (err or out).strip() or "Unknown git error"
    raise Exception(friendly_git_error(msg))

def friendly_git_error(msg: str) -> str:
    msg = msg.strip()
    if "Repository not found" in msg:
        return "Repository not found or access denied."
    if "Authentication failed" in msg:
        return "Authentication failed."
    if "Permission denied" in msg:
        return "Permission denied."
    if "Could not resolve host" in msg or "Name or service not known" in msg:
        return "Network or DNS error."
    if "fatal:" in msg:
        return msg.replace("fatal:", "", 1).strip()
    return msg or "Unknown git error."