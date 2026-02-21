import re
from dataclasses import dataclass

import httpx


@dataclass
class GitHubRepo:
    owner: str
    repo: str


"""
Matches https and http github urls
Raises:
- ValueError if the URL is not a valid GitHub repository URL
"""


def match_github_url(url) -> GitHubRepo:
    needle = r"(?:https?://github\.com/|git@github\.com[:/])(?P<owner>[\w-]+)/(?P<repo>[\w.-]+?)(?:\.git)?(?:/.*)?$"

    match = re.search(needle, url)

    # if no match, raise ValueError
    if match is None:
        raise ValueError("Invalid GitHub repository URL")

    repo = match.group("repo")
    if repo is None:
        raise ValueError("Invalid GitHub repository URL")

    owner = match.group("owner")
    if owner is None:
        raise ValueError("Invalid GitHub repository URL")

    return GitHubRepo(owner=owner, repo=repo)


async def fetch_github_readme(github_repo_url: str) -> str:
    repo = match_github_url(
        github_repo_url
    )  # Validate the URL and extract owner/repo, but we don't actually need them here

    USER_AGENT = "WebbU-Hackathon-hackathon.webbu.se"

    HEADERS = {"User-Agent": USER_AGENT}

    async with httpx.AsyncClient() as client:
        metadata_url = f"https://api.github.com/repos/{repo.owner}/{repo.repo}/readme"
        response_metadata = await client.get(metadata_url, headers=HEADERS)
        response_metadata.raise_for_status()

        content_url = response_metadata.json()["download_url"]
        response_readme_content = await client.get(content_url, headers=HEADERS)
        response_readme_content.raise_for_status()

        return response_readme_content.text
