"""Evaluator for adaptability quality using LLM judgment."""

from typing import List
from framework.models import AgentOutput, Benchmark
from framework.evaluation.evaluators.base_llm import BaseLLMEvaluator
from framework.evaluation.prompts import build_adaptability_prompt
from framework.evaluation.dimensions import ADAPTABILITY
from framework.llms import Message


class AdaptabilityEvaluator(BaseLLMEvaluator):
    """Evaluates the 'Adaptability' dimension of an agent's output.

    Uses an LLM Judge to check how well the itinerary is modified to respond to changing
    circumstances while keeping traveler preferences intact.
    """

    @property
    def dimension(self) -> str:
        return ADAPTABILITY

    def build_prompt(
        self,
        benchmark: Benchmark,
        output: AgentOutput,
    ) -> List[Message]:
        return build_adaptability_prompt(benchmark, output)
