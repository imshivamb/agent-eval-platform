"""Evaluator for personalization quality using LLM judgment."""

from typing import List
from framework.models import AgentOutput, Benchmark
from framework.evaluation.evaluators.base_llm import BaseLLMEvaluator
from framework.evaluation.prompts import build_personalization_prompt
from framework.evaluation.dimensions import PERSONALIZATION
from framework.llms import Message


class PersonalizationEvaluator(BaseLLMEvaluator):
    """Evaluates the 'Personalization' dimension of an agent's output.

    Uses an LLM Judge to check if the itinerary is tailored to the traveler's stated
    interests, hobbies, remote working requirements, and pacing preferences.
    """

    @property
    def dimension(self) -> str:
        return PERSONALIZATION

    def build_prompt(
        self,
        benchmark: Benchmark,
        output: AgentOutput,
    ) -> List[Message]:
        return build_personalization_prompt(benchmark, output)
