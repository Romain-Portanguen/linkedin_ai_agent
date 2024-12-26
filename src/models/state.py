from enum import Enum
from typing import TypedDict, Dict, Any

class WorkflowStatus(str, Enum):
    """Possible workflow states"""
    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class OverallState(TypedDict):
    """Global workflow state"""
    user_text: str
    target_audience: str
    edit_text: str
    linkedin_post: Dict[str, Any]  # Post serialized
    n_drafts: int
    workflow_status: str 