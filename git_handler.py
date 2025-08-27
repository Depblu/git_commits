import sys
import git
from datetime import datetime
from typing import List
from models import Commit, ListCommits

def find_commits(repo_path: str, branch: str, since: str = None, until: str = None, skip: int = 0, max_count: int = 50) -> ListCommits:
    """
    Retrieves a list of commits from a Git repository based on the specified criteria.

    Args:
        repo_path: Absolute path to the Git repository.
        branch: The branch name to retrieve commits from.
        since: The start date for the commit search (ISO 8601 format).
        until: The end date for the commit search (ISO 8601 format).
        skip: The number of commits to skip (for pagination).
        max_count: The maximum number of commits to return.

    Returns:
        A list of Commit objects.
    """
    try:
        repo = git.Repo(repo_path)

        kwargs = {
            'rev': branch,
            'skip': skip,
            'max_count': max_count
        }
        if since:
            kwargs['since'] = since
        if until:
            kwargs['until'] = until

        commit_iterator = repo.iter_commits(**kwargs)

        results = []
        for commit in commit_iterator:
            results.append(Commit(
                hexsha=commit.hexsha,
                author_name=commit.author.name,
                author_email=commit.author.email,
                authored_date=commit.authored_datetime.isoformat(),
                message=commit.message.strip()
            ))
        
        return ListCommits(commits=results)

    except git.exc.NoSuchPathError:
        _log_error(f"Error: Repository path not found at '{repo_path}'")
        return ListCommits(commits=[])
    except git.exc.GitCommandError as e:
        _log_error(f"Error: Git command failed. Is branch '{branch}' correct? Details: {e}")
        return ListCommits(commits=[])
    except Exception as e:
        _log_error(f"An unexpected error occurred: {e}")
        return ListCommits(commits=[])

def _log_error(message: str):
    """Helper function to log messages to stderr."""
    print(message, file=sys.stderr)
