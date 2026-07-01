"""Travel planning agent implementation for generating itineraries."""

from framework.llms import BaseLLM, Message
from framework.models import AgentOutput
from agents.base import BaseAgent
from .prompts import TRAVEL_PLANNING_SYSTEM_PROMPT


class TravelPlanningAgent(BaseAgent):
    """A travel planning assistant agent powered by an LLM.

    Accepts user prompts/scenarios and plans itineraries accordingly.
    """

    def __init__(self, llm: BaseLLM):
        """Initializes the TravelPlanningAgent.

        Args:
            llm: The LLM client wrapper to generate itineraries.
        """
        self.llm = llm

    def run(self, prompt: str) -> AgentOutput:
        """Generates a travel itinerary based on user preferences.

        Args:
            prompt: The user prompt describing constraints and preferences.

        Returns:
            An AgentOutput containing the planned travel itinerary.
        """
        messages = [
            Message(role="system", content=TRAVEL_PLANNING_SYSTEM_PROMPT),
            Message(role="user", content=prompt),
        ]

        # Let any generation exceptions propagate to caller/framework handlers
        response = self.llm.generate(messages)

        return AgentOutput(
            content=response.text,
            metadata={
                "agent": self.__class__.__name__,
                "llm": type(self.llm).__name__,
            },
        )
