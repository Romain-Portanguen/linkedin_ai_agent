from langgraph.graph import END, StateGraph, START
from models.state import OverallState
from models.config import Configuration
from services.linkedin_agent import LinkedInAgent

def build_linkedin_workflow() -> StateGraph:
    """Build and return the LinkedIn workflow"""
    workflow = StateGraph(OverallState, config_schema=Configuration)
    agent = LinkedInAgent()

    # Adding nodes
    workflow.add_node("editor", agent.editor_node)
    workflow.add_node("linkedin_writer", agent.linkedin_writer_node)
    workflow.add_node("linkedin_critique", agent.critique_linkedin_node)
    workflow.add_node("supervisor", agent.supervisor_node)

    # Adding edges
    workflow.add_edge("editor", "linkedin_writer")
    workflow.add_edge("linkedin_writer", "supervisor")
    workflow.add_conditional_edges("supervisor", agent.should_continue)
    workflow.add_edge("linkedin_critique", "linkedin_writer")
    workflow.add_edge(START, "editor")

    return workflow.compile() 