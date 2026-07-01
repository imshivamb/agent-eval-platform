"""Abstract base agent class definition."""

from abc import ABC, abstractmethod
from framework.models import AgentOutput


class BaseAgent(ABC):
    """Abstract base class defining the standard interface for all agents."""

    @abstractmethod
    def run(self, prompt: str) -> AgentOutput:
        """Executes the agent's primary decision/generation task.

        Args:
            prompt: The user request/scenario prompt.

        Returns:
            An AgentOutput dataclass containing generated content and metadata.
        """
        pass
