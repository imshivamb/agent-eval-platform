"""Mock and testing utilities for evaluation pipelines."""

from framework.evaluation.base import BaseEvaluator
from framework.models import AgentOutput, Benchmark, DimensionScore


class DummyEvaluator(BaseEvaluator):
    """Simple evaluator returning a static score for profile verification."""

    def __init__(self, dimension: str, score: float, reason: str):
        """Initializes the DummyEvaluator.

        Args:
            dimension: Dimension name key this evaluator represents.
            score: Static numeric score to return.
            reason: Static reason explanation to return.
        """
        self._dimension = dimension
        self.score = score
        self.reason = reason

    def evaluate(self, benchmark: Benchmark, output: AgentOutput) -> DimensionScore:
        return DimensionScore(
            dimension=self._dimension, score=self.score, reason=self.reason
        )
