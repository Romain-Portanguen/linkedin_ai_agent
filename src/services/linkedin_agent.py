from typing import Dict, Any, Union, List
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage
from utils.constants import (
    OLLAMA_BASE_URL, 
    OLLAMA_MODEL, 
    OLLAMA_TEMPERATURE,
    DEFAULT_N_DRAFTS
)
from utils.logger import logger
from utils.prompts import EDITOR_PROMPT, LINKEDIN_PROMPT, LINKEDIN_CRITIQUE_PROMPT
from models.post import Post
from models.state import OverallState, WorkflowStatus
from langgraph.graph import END

class LinkedInAgent:
    """
    Main agent coordinating different AI experts for LinkedIn post generation.
    
    This agent orchestrates the workflow between different specialized roles:
    - Editor: Improves text clarity and structure
    - Writer: Creates LinkedIn-optimized content
    - Critic: Provides feedback and suggestions
    - Supervisor: Manages the iteration process
    """
    
    def __init__(self):
        """Initialize the agent with Ollama LLM configuration"""
        self.llm = Ollama(
            model=OLLAMA_MODEL,
            temperature=OLLAMA_TEMPERATURE,
            base_url=OLLAMA_BASE_URL,
        )

    def _get_prompt_response(self, system_prompt: str, user_prompt: str) -> str:
        """
        Get a response from the LLM using system and user prompts.
        
        Args:
            system_prompt: Instructions for the AI role
            user_prompt: Specific task or content to process
            
        Returns:
            Generated response from the LLM
        """
        return self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

    def editor_node(self, state: OverallState) -> Dict[str, Any]:
        """
        Editor node: improves text clarity and structure.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with edited text and initialized post
        """
        logger.info("Entering editor_node")
        
        prompt = f"""
            text:
            ```
            {state["user_text"]}
            ```
        """.strip()
        
        response = self._get_prompt_response(EDITOR_PROMPT, prompt)
        logger.info("Editor completed initial edit")
        
        return {
            "edit_text": response,
            "linkedin_post": Post().model_dump(),
            "n_drafts": DEFAULT_N_DRAFTS,
            "workflow_status": WorkflowStatus.STARTING
        }

    def linkedin_writer_node(self, state: OverallState) -> Dict[str, Any]:
        """
        Writer node: creates a LinkedIn-optimized version of the post.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with new post draft
        """
        logger.info("Entering linkedin_writer_node")
        post = Post(**state["linkedin_post"])
        
        feedback_section = self._build_feedback_section(post)
        prompt = self._build_writer_prompt(state, feedback_section)
        
        response = self._get_prompt_response(LINKEDIN_PROMPT, prompt)
        logger.info("LinkedIn writer generated new version")
        
        post.add_draft(response)
        return {"linkedin_post": post.model_dump()}

    def _build_feedback_section(self, post: Post) -> str:
        """
        Build the feedback section for the writer prompt.
        
        Args:
            post: Current post with drafts and feedback
            
        Returns:
            Formatted feedback section or empty string if no feedback
        """
        if not post.feedback or not post.get_latest_draft():
            return ""
        
        return f"""
        Previous version and feedback:
        ```
        Post: {post.get_latest_draft()}
        Feedback: {post.feedback}
        ```
        """.strip()

    def _build_writer_prompt(self, state: OverallState, feedback_section: str) -> str:
        """
        Build the complete prompt for the LinkedIn writer.
        
        Args:
            state: Current workflow state
            feedback_section: Formatted feedback from critic
            
        Returns:
            Complete prompt for the writer
        """
        return f"""
            text:
            ```
            {state["edit_text"]}
            ```
            
            {feedback_section}
            
            Target audience: {state["target_audience"]}
            
            Write only the post content.
        """.strip()

    def critique_linkedin_node(self, state: OverallState) -> Dict[str, Any]:
        """
        Critic node: analyzes and provides feedback on the post.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with critic's feedback
        """
        logger.info("Entering critique_linkedin_node")
        post = Post(**state["linkedin_post"])
        
        prompt = f"""
            Original text:
            ```
            {state["edit_text"]}
            ```
            
            Current LinkedIn post:
            ```
            {post.get_latest_draft()}
            ```
            
            Target audience: {state["target_audience"]}
        """.strip()

        response = self._get_prompt_response(LINKEDIN_CRITIQUE_PROMPT, prompt)
        logger.info("LinkedIn critique completed")
        
        post.feedback = response
        return {"linkedin_post": post.model_dump()}

    def supervisor_node(self, state: OverallState) -> OverallState:
        """
        Supervisor node: manages workflow state and iterations.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated workflow state
        """
        logger.info("Entering supervisor_node")
        post = Post(**state["linkedin_post"])
        
        if len(post.drafts) >= state["n_drafts"]:
            state["workflow_status"] = WorkflowStatus.COMPLETED
        else:
            state["workflow_status"] = WorkflowStatus.IN_PROGRESS
        return state

    def should_continue(self, state: OverallState) -> Union[str, List[str]]:
        """
        Determines if the workflow should continue or end.
        
        Args:
            state: Current workflow state
            
        Returns:
            END if workflow is complete, or next node(s) to execute
        """
        post = Post(**state["linkedin_post"])
        n_drafts = state["n_drafts"]
        
        if len(post.drafts) >= n_drafts:
            logger.info("Workflow completed")
            return END
        
        logger.info("Continuing to next iteration")    
        return ["linkedin_critique"]

    def get_final_post(self, state: OverallState) -> str:
        """
        Get the final version of the LinkedIn post.
        
        Args:
            state: Final workflow state
            
        Returns:
            The final optimized LinkedIn post
        """
        post = Post(**state["linkedin_post"])
        return post.get_latest_draft() or ""

    def get_all_versions(self, state: OverallState) -> List[Dict[str, str]]:
        """
        Get all versions of the post with their corresponding feedback.
        
        Args:
            state: Final workflow state
            
        Returns:
            List of dictionaries containing each version and its feedback
        """
        post = Post(**state["linkedin_post"])
        versions = []
        
        for i, draft in enumerate(post.drafts):
            versions.append({
                "version": i + 1,
                "content": draft,
                "feedback": post.feedback if i == len(post.drafts) - 1 else None
            })
            
        return versions    