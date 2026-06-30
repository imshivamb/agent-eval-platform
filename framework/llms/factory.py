"""Factory module for creating LLM client wrappers."""

from typing import Any, Dict, Type
from framework.llms.base import BaseLLM
from framework.llms.mock import MockLLM
from framework.llms.openai import OpenAILLM
from framework.llms.gemini import GeminiLLM

# Registry of supported providers mapping provider name to class wrapper
_PROVIDERS: Dict[str, Type[BaseLLM]] = {
    "openai": OpenAILLM,
    "gemini": GeminiLLM,
    "mock": MockLLM,
}


def create_llm(provider: str, **kwargs: Any) -> BaseLLM:
    """Factory function to instantiate an LLM wrapper by provider name.

    Args:
        provider: Name of the LLM provider ('openai', 'gemini', 'mock').
        **kwargs: Arguments passed to the provider class constructor.

    Returns:
        An instance of BaseLLM.

    Raises:
        ValueError: If an unknown provider name is supplied.
    """
    try:
        provider_cls = _PROVIDERS[provider.lower()]
    except KeyError:
        supported = ", ".join(sorted(_PROVIDERS.keys()))
        raise ValueError(
            f"Unknown LLM provider '{provider}'. Supported providers: {supported}"
        )

    return provider_cls(**kwargs)
