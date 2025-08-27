from pydantic import BaseModel, Field
from typing import List

class Commit(BaseModel):
    """Represents a single Git commit."""

    hexsha: str = Field(..., description="The full commit hash.")
    author_name: str = Field(..., description="The name of the commit author.")
    author_email: str = Field(..., description="The email of the commit author.")
    authored_date: str = Field(..., description="The authored date in ISO 8601 format.")
    message: str = Field(..., description="The full commit message.")
    
class ListCommits(BaseModel):
    """Represents a list of Git commits."""
    commits: List[Commit] = Field(..., description="A list of Commit objects.")