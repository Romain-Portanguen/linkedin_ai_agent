"""
Main entry point for the LinkedIn Post Generator.
Provides high-level functions to interact with the workflow.
"""

from typing import Dict, Any
from src.models.state import OverallState
from src.workflow import build_linkedin_workflow
from src.services.linkedin_agent import LinkedInAgent

def generate_linkedin_post(
    text: str,
    target_audience: str,
    n_drafts: int = 3
) -> Dict[str, Any]:
    """
    Generate an optimized LinkedIn post from input text.
    
    Args:
        text: Original text to transform
        target_audience: Target audience for the post
        n_drafts: Number of iterations to perform
        
    Returns:
        Dictionary containing the workflow results
    """
    # Initialize workflow
    workflow = build_linkedin_workflow()
    
    # Prepare initial state
    initial_state = {
        "user_text": text,
        "target_audience": target_audience,
        "edit_text": "",
        "linkedin_post": {"drafts": [], "feedback": None},
        "n_drafts": n_drafts,
        "workflow_status": "starting"
    }
    
    # Run workflow
    result = workflow.invoke(initial_state)
    if result is None:
        return None
        
    # Create agent to access results
    agent = LinkedInAgent()
    
    return {
        "final_post": agent.get_final_post(result),
        "all_versions": agent.get_all_versions(result),
        "workflow_status": result["workflow_status"]
    } 