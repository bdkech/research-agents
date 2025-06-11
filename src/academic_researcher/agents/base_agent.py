"""Base agent class for the academic researcher package."""
from abc import ABC 
from typing import Callable, List

from loguru import logger
from pydantic_ai import Agent
from pydantic_ai.usage import UsageLimits
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

from academic_researcher.models.schemas import ResearchContext

class BaseAgent(ABC):
    """Base class for all agents in the academic researcher package."""

    def __init__(
        self,
        model_name: str = "llama3.2",
        system_prompt: str = "",
        usage_limits: UsageLimits | None = None,
        host: str = "http://localhost:11434/v1",
        ctx =  ResearchContext,
        rtx_type = None,
    ) -> None:
        """Initialize the base agent.

        Args:
            model_name: Name of the model to use
            system_prompt: System prompt for the agent
            usage_limits: Optional usage limits for the agent
            host: Host URL for the model
        """
        logger.info(f"Initializing {self.__class__.__name__} with model {model_name}")
        provider = OpenAIProvider(
            base_url=host
        )
        model = OpenAIModel(
            model_name=model_name,
            provider=provider,
        )
        self.agent = Agent(
            model,
            deps_type=ctx,
            result_type=rtx_type,  
            system_prompt=system_prompt,
        )
        self.usage_limits = usage_limits or UsageLimits(request_limit=100)
        self._registered_tools: List[Callable] = []

        self._register_tools()
        logger.info(f"Initialized {self.__class__.__name__} with model {model_name}")

    def _register_tools(self):
        """
        This method is designed to be overridden by subclasses.
        Subclasses should define their tools as methods within the subclass
        and decorate them using `@self.internal_agent.tool` or
        `@self.internal_agent.tool_plain` to register them with the agent.
        """
        pass # No-op in base class

    async def run(self, user_prompt: str, *args, **kwargs):
        """
        Runs the agent asynchronously with a user prompt.
        All additional *args and **kwargs are passed directly to the underlying
        pydantic_ai.Agent's `run` method (e.g., `deps`, `message_history`).
        """
        return await self.agent.run(user_prompt, *args, **kwargs)

    def run_sync(self, user_prompt: str, *args, **kwargs):
        """
        Runs the agent synchronously with a user prompt.
        All additional *args and **kwargs are passed directly to the underlying
        pydantic_ai.Agent's `run_sync` method (e.g., `deps`, `message_history`).
        """
        return self.agent.run_sync(user_prompt, *args, **kwargs)