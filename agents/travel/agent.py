"""Real travel agent implementation for generating itineraries."""

from framework.llms import BaseLLM, Message
from framework.models import AgentOutput


class TravelAgent:
    """A travel planning assistant agent powered by an LLM.

    Accepts user prompts/scenarios and plans itineraries accordingly.
    """

    def __init__(self, llm: BaseLLM):
        """Initializes the TravelAgent.

        Args:
            llm: The LLM client wrapper to generate itineraries.
        """
        self.llm = llm

    def plan_trip(self, prompt: str) -> AgentOutput:
        """Generates a travel itinerary based on user preferences.

        Args:
            prompt: The user prompt describing constraints and preferences.

        Returns:
            An AgentOutput containing the planned travel itinerary.
        """
        system_instruction = (
            "You are a professional travel agent assistant.\n"
            "Your task is to plan a detailed, well-structured travel itinerary "
            "based on the user's preferences, budget limits, duration, backpacking style, "
            "and other specified constraints.\n"
            "Be precise, geographically efficient, and mention exact travel logistics, closed days, and pricing "
            "where appropriate."
        )

        messages = [
            Message(role="system", content=system_instruction),
            Message(role="user", content=prompt),
        ]

        try:
            response = self.llm.generate(messages)
            content = response.text
        except Exception as e:
            content = f"Failed to generate travel itinerary: {e}"

        return AgentOutput(content=content, metadata={"model": type(self.llm).__name__})
