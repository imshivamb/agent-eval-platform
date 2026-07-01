"""Evaluator for factual information accuracy using hybrid verifiers."""

from typing import List
from framework.evaluation.evaluators.base_llm import BaseLLMEvaluator
from framework.evaluation.prompts.information_accuracy import build_information_accuracy_prompt
from framework.evaluation.dimensions import INFORMATION_ACCURACY
from framework.llms import BaseLLM, Message
from framework.models import AgentOutput, Benchmark
from framework.verification.pipeline import VerificationPipeline


class InformationAccuracyEvaluator(BaseLLMEvaluator):
    """Evaluates the 'Information Accuracy' dimension of an agent's output.

    Uses an injected VerificationPipeline to check factual claims,
    and formats them to get graded by the LLM Judge.
    """

    def __init__(self, llm: BaseLLM, pipeline: VerificationPipeline):
        """Initializes the InformationAccuracyEvaluator.

        Args:
            llm: The LLM client for final evidence grading.
            pipeline: The VerificationPipeline instance to verify claims.
        """
        super().__init__(llm)
        self.pipeline = pipeline

    @property
    def dimension(self) -> str:
        return INFORMATION_ACCURACY

    def build_prompt(
        self,
        benchmark: Benchmark,
        output: AgentOutput,
    ) -> List[Message]:
        # 1. Run the injected pipeline to extract and verify factual claims
        report = self.pipeline.run(output)
        # 2. Format findings context and return prompts list
        return build_information_accuracy_prompt(benchmark, output, report)
