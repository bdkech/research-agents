from typing import Any

from loguru import logger
from pydantic_ai import RunContext
from pydantic_ai.tools import Tool

from academic_researcher.agents.base_agent import BaseAgent
from academic_researcher.models.schemas import RefinedQueryResult, WorkflowState

class PromptProcessorAgent(BaseAgent):
    """Agent for processing and refining research queries."""

    def __init__(
        self,
        host: str = "",
        model_name: str = "",
        usage_limits: Any = None,
        topic: str = ""
    ) -> None:
        """Initialize the prompt processor agent.

        Args:
            host: Host URL for the model
            model_name: Name of the model to use
            usage_limits: Optional usage limits for the agent
        """
        system_prompt = (
            "You are an expert prompt processor for academic research. "
            "Given a research topic, generate a refined arXiv search query string "
            "that enhances search relevance. Consider using arXiv's advanced search "
            "syntax and appropriate filters. Return a structured query that will "
            "yield the most relevant academic papers based on the provided input. "
            "Do not add date filters." 
        )
        self.topic = topic
        super().__init__(
            system_prompt=system_prompt, 
            host=host,
            model_name=model_name,
            usage_limits=usage_limits,
            rtx_type=RefinedQueryResult
            )
    def _register_tools(self):
        @self.agent.tool(retries=3)
        async def process_prompt(query) -> RefinedQueryResult:
            topic = query.strip().lower()

            # Basic heuristic refinement
            if ' in ' in topic:
                # Split the topic into key parts if it contains 'in', to form precise queries.
                subtopics = topic.split(' in ')
                main_topic = subtopics[0].strip()
                context = subtopics[1].strip()
                refined_query = f"all:{main_topic} AND cat:{context.replace(' ', '_')}"
            else:
                # Fallback: Assume it's a broader topic
                refined_query = f"ti:\"{topic}\" OR abs:\"{topic}\""
        
            logger.info(f"Refined query generated: {refined_query}")
            return RefinedQueryResult(query=refined_query) 
        logger.info(f"Initialized tool in {self.__class__.__name__} as process_prompt)")