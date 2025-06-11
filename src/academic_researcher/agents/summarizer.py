from typing import Any

from loguru import logger

from academic_researcher.agents.base_agent import BaseAgent 
from academic_researcher.models.schemas import PaperSummary

class SummarizerAgent(BaseAgent):
    def __init__(
        self,
        host: str = "",
        model_name: str = "",
        usage_limits: Any = None,
    ) -> None:
        """Initialize the prompt processor agent.

        Args:
            host: Host URL for the model
            model_name: Name of the model to use
            usage_limits: Optional usage limits for the agent
        """
        system_prompt = (
            "You are an expert summarizer. Provide a concise summary of the given paper abstract."
            "Your summary should be completely derived from the abstract and should not include any additional information."
            "It should not be longer than 150 characters."
        )
        super().__init__(
            system_prompt=system_prompt, 
            host=host,
            model_name=model_name,
            usage_limits=usage_limits,
            rtx_type=PaperSummary
            )
    def _register_tools(self): 
        @self.agent.tool(retries=3)
        async def summarize(abstract) -> PaperSummary:
            """Summarize the given paper abstract."""
            logger.info(f"Summarizing papers...")
            if not abstract:
                return PaperSummary(summary="No abstract available.")
            summary_text = abstract[:150] + "..." if len(abstract) > 150 else abstract
            return PaperSummary(summary=summary_text)
        logger.info(f"Initialized tool in {self.__class__.__name__} as summarize")