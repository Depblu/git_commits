from typing import Optional, List
from mcp.server.fastmcp import FastMCP
from git_handler import find_commits
from models import Commit, ListCommits

# 1. Initialize the FastMCP server
mcp = FastMCP(
    name="GitCommitRetriever",
    instructions="A tool to retrieve git commit history from a repository."
)

# 2. Define the tool using the @mcp.tool decorator
@mcp.tool(structured_output=True)
def get_commits(
    repo_path: str,
    branch: str,
    since: Optional[str] = None,
    until: Optional[str] = None,
    skip: int = 0,
    max_count: int = 50
) -> ListCommits:
    """
    Retrieves commit history from a specified git repository and branch.
    Supports filtering by date range and pagination.

    Args:
        repo_path: Absolute path to the Git repository.
        branch: The branch name to retrieve commits from.
        since: The start date for the commit search (ISO 8601 format).
        until: The end date for the commit search (ISO 8601 format).
        skip: The number of commits to skip (for pagination).
        max_count: The maximum number of commits to return.
    """
    # 3. Call the core business logic from the separate handler
    return find_commits(
        repo_path=repo_path,
        branch=branch,
        since=since,
        until=until,
        skip=skip,
        max_count=max_count
    )

# 4. Run the server
if __name__ == "__main__":
    mcp.run() # Defaults to stdio transport