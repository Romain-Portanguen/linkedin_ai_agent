from typing import Optional, List
from pydantic import BaseModel, Field

class Post(BaseModel):
    """
    Represents a LinkedIn post being created
    
    Attributes:
        drafts: List of different versions of the post
        feedback: Last analysis of the reviewer
    """
    drafts: List[str] = Field(default_factory=list)
    feedback: Optional[str] = None

    def add_draft(self, draft: str) -> None:
        """Add a new version of the post"""
        self.drafts.append(draft)

    def get_latest_draft(self) -> Optional[str]:
        """Get the latest version of the post"""
        return self.drafts[-1] if self.drafts else None 