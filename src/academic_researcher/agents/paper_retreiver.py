from typing import Any
import arxiv

from loguru import logger
from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import UsageLimits
from pydantic_ai.tools import Tool

from academic_researcher.agents.base_agent import BaseAgent 
from academic_researcher.models.schemas import PaperMetadata, GatherPapers

class PaperRetreiverAgent(BaseAgent):
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
            "You are a research assistant that fetches research papers from arXiv."
            "Return a list of paper metadata relevant to the refined query."
        )

        super().__init__(
            system_prompt=system_prompt, 
            host=host,
            model_name=model_name,
            usage_limits=usage_limits,
            rtx_type=GatherPapers
            )
    def _register_tools(self): 
        @self.agent.tool(retries=3)
        async def fetch_papers(query) -> GatherPapers:
            refined_query = query.prompt  # The refined query from the prompt processor
            logger.info(f"Fetching papers for query: {refined_query}")
            search = arxiv.Search(
                query=refined_query,
                max_results=5,  # Adjust the number of results as needed.
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            results = list(search.results())
            papers = []
            for result in results:
                published_str = (
                    result.published.strftime("%Y-%m-%d")
                    if hasattr(result, "published") and result.published is not None
                    else "Unknown"
                )
                papers.append(
                    PaperMetadata(
                        title=result.title,
                        abstract=result.summary,
                        authors=[author.name for author in result.authors],
                        publication_date=published_str
                    )
                )
            logger.info(f"Fetched {len(papers)} papers.")
            return  GatherPapers(papers=papers)
        logger.info(f"Initialized tool in {self.__class__.__name__} as fetch_papers")