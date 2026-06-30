"""Mock LLM client wrapper for testing and offline validation."""

from typing import List, Union
from framework.llms.base import BaseLLM, LLMResponse, Message


class MockLLM(BaseLLM):
    """A mock LLM wrapper for testing and offline execution."""

    def __init__(self, responses: Union[str, List[str]]):
        """Initializes the MockLLM.

        Args:
            responses: A single response string or a list of response strings
                to return sequentially on each generate call.
        """
        self.responses = [responses] if isinstance(responses, str) else list(responses)
        self.call_count = 0

    def generate(self, messages: List[Message]) -> LLMResponse:
        if not self.responses:
            return LLMResponse(text="Mock response")
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        return LLMResponse(text=response)
