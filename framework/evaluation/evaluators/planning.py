"""Evaluator for planning quality using LLM judgment."""

from typing import List
from framework.models import AgentOutput, Benchmark
from framework.evaluation.evaluators.base_llm import BaseLLMEvaluator
from framework.evaluation.prompts import build_planning_prompt
from framework.evaluation.dimensions import PLANNING_QUALITY
from framework.llms import Message


class PlanningQualityEvaluator(BaseLLMEvaluator):
    """Evaluates the 'Planning Quality' dimension of an agent's output.

    Uses an LLM Judge to determine if the itinerary follows a logical,
    efficient route, minimizes accommodation changes, and balances pacing.
    """

    @property
    def dimension(self) -> str:
        return PLANNING_QUALITY

    def build_prompt(
        self,
        benchmark: Benchmark,
        output: AgentOutput,
    ) -> List[Message]:
        return build_planning_prompt(benchmark, output)
