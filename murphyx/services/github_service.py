"""
GitHub service — PR/issue helpers.

Scaffold; uses GITHUB_TOKEN from env only — never commit token.
"""

# TODO: Optional octokit or httpx calls for PR creation from agent output.


def create_pr(title: str, body: str, branch: str) -> dict:
    """Open PR — stub."""
    raise NotImplementedError
