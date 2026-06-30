"""Evaluator for constraint satisfaction using LLM judgment."""

from typing import List
from framework.models import AgentOutput, Benchmark
from framework.evaluation.evaluators.base_llm import BaseLLMEvaluator
from framework.evaluation.prompts import build_constraint_prompt
from framework.evaluation.dimensions import CONSTRAINT_SATISFACTION
from framework.llms import Message


class ConstraintEvaluator(BaseLLMEvaluator):
    """Evaluates the 'Constraint Satisfaction' dimension of an agent's output.

    Uses an LLM Judge to determine if all constraints defined in the benchmark
    scenario are successfully met.
    """

    @property
    def dimension(self) -> str:
        return CONSTRAINT_SATISFACTION

    def build_prompt(
        self,
        benchmark: Benchmark,
        output: AgentOutput,
    ) -> List[Message]:
        return build_constraint_prompt(benchmark, output)
