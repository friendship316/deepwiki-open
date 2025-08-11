import os
import shutil
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

load_dotenv()

from api.data_pipeline import get_gitlab_file_content, download_repo  # noqa: E402


@pytest.mark.network
@pytest.mark.integration
def test_get_gitlab_file_content_with_token():
    """
    Verify that we can fetch a file from a private GitLab repository using a token.

    Required environment variables:
    - GITLAB_TOKEN: Personal access token with read_api or api scope
    - GITLAB_REPO_URL: e.g., https://gitlab.com/group/project or self-hosted domain
    Optional:
    - GITLAB_FILE_PATH: path to a file to fetch (default: README.md)
    """
    token = os.getenv("GITLAB_TOKEN")
    repo_url = os.getenv("GITLAB_REPO_URL")
    file_path = os.getenv("GITLAB_FILE_PATH", "README.md")

    if not token or not repo_url:
        pytest.skip("GITLAB_TOKEN and/or GITLAB_REPO_URL not set; skipping network test")

    content = get_gitlab_file_content(repo_url=repo_url, file_path=file_path, access_token=token)
    assert isinstance(content, str) and len(content) > 0, "Expected non-empty file content from GitLab API"


@pytest.mark.network
@pytest.mark.integration
def test_gitlab_clone_with_token(tmp_path: Path):
    """
    Optionally verify cloning a private GitLab repository using a token.
    Set RUN_GIT_CLONE_TEST=1 to enable (clones can be slow and require network).

    Required:
    - GITLAB_TOKEN
    - GITLAB_REPO_URL
    """
    if os.getenv("RUN_GIT_CLONE_TEST") != "1":
        pytest.skip("Set RUN_GIT_CLONE_TEST=1 to run clone test")

    token = os.getenv("GITLAB_TOKEN")
    repo_url = os.getenv("GITLAB_REPO_URL")

    if not token or not repo_url:
        pytest.skip("GITLAB_TOKEN and/or GITLAB_REPO_URL not set; skipping clone test")

    clone_dir = tmp_path / "gitlab_clone"
    clone_dir.mkdir(parents=True, exist_ok=True)

    # This will raise ValueError on failure; we simply assert no exception and that directory has files
    output = download_repo(repo_url=repo_url, local_path=str(clone_dir), type="gitlab", access_token=token)
    assert clone_dir.exists(), "Clone directory should exist"
    # Repo should contain at least .git or source files
    entries = list(clone_dir.iterdir())
    assert len(entries) > 0, f"Expected files in clone directory, got: {entries} (output: {output})"

