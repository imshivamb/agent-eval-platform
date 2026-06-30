"""OpenAI client wrapper implementation."""

from typing import List, Optional
from framework.llms.base import BaseLLM, LLMResponse, Message


class OpenAILLM(BaseLLM):
    """OpenAI API client wrapper."""

    def __init__(self, model_name: str = "gpt-4o", api_key: Optional[str] = None):
        """Initializes the OpenAILLM.

        Validates that the 'openai' library is installed immediately.

        Args:
            model_name: The target model ID.
            api_key: The OpenAI API key. Reads from environment if None.

        Raises:
            ImportError: If the 'openai' library is not installed.
        """
        try:
            # pyrefly: ignore [missing-import]
            import openai
        except ImportError:
            raise ImportError(
                "The 'openai' library is required to use OpenAILLM. "
                "Please install it using 'pip install openai'."
            )

        self._client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name

    def generate(self, messages: List[Message]) -> LLMResponse:
        formatted_messages = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]
        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,
        )
        response_text = response.choices[0].message.content or ""
        return LLMResponse(text=response_text)
