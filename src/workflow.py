from langgraph.graph import END, StateGraph
from src.models.state import OverallState
from src.models.config import Configuration
from src.services.linkedin_agent import LinkedInAgent

def build_linkedin_workflow() -> StateGraph:
    """Build and return the LinkedIn workflow"""
    workflow = StateGraph(schema=OverallState)
    agent = LinkedInAgent()

    # Adding nodes
    workflow.add_node("editor", agent.editor_node)
    workflow.add_node("linkedin_writer", agent.linkedin_writer_node)
    workflow.add_node("linkedin_critique", agent.critique_linkedin_node)
    workflow.add_node("supervisor", agent.supervisor_node)

    # Adding edges with conditional routing
    workflow.set_entry_point("editor")
    workflow.add_edge("editor", "linkedin_writer")
    workflow.add_edge("linkedin_writer", "supervisor")
    
    # Configurer le routage conditionnel uniquement
    workflow.add_conditional_edges(
        "supervisor",
        lambda x: END if x["workflow_status"] == "completed" else "linkedin_critique"
    )
    
    workflow.add_edge("linkedin_critique", "linkedin_writer")

    return workflow.compile() 