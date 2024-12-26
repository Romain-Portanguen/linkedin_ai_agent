from pydantic import BaseModel, Field
from utils.constants import DEFAULT_N_DRAFTS

class Configuration(BaseModel):
    """Configuration parameters"""
    n_drafts: int = Field(default=DEFAULT_N_DRAFTS, gt=0) 