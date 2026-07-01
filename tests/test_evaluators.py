import unittest
import tempfile
import os
import json
from framework.models import AgentOutput, Benchmark
from framework.evaluation.evaluators import (
    ConstraintEvaluator,
    PlanningQualityEvaluator,
    PersonalizationEvaluator,
    AdaptabilityEvaluator,
    InformationAccuracyEvaluator,
)
from framework.verification.local import LocalKnowledgeBaseVerifier
from framework.verification.extractor import ClaimExtractor
from framework.verification.pipeline import VerificationPipeline
from framework.llms import MockLLM


class TestEvaluators(unittest.TestCase):
    """Tests concrete evaluation dimension strategies."""

    def setUp(self):
        # Sample benchmark for test judges
        self.benchmark = Benchmark(
            benchmark_id="test-id",
            name="Test Scenario",
            description="Test description",
            prompt="Test prompt",
            constraints={"Budget": "1000 USD"},
            expected_behavior=["do good"],
            evaluation_criteria={"Constraint Satisfaction": ["do good"]},
            pass_criteria=["scored"],
            failure_conditions=["fail"],
            notes=[],
        )
        self.output = AgentOutput(content="Mock itinerary content.")

        # Create temporary ground truth file
        self.kb_data = {"attraction": {"exists": "true"}}
        self.temp_kb = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(self.kb_data, self.temp_kb)
        self.temp_kb.close()

    def tearDown(self):
        os.unlink(self.temp_kb.name)

    def test_constraint_evaluator(self):
        mock_response = """
        ```json
        {
          "score": 90,
          "reason": "Satisfied budget constraints."
        }
        ```
        """
        llm = MockLLM(responses=[mock_response])
        evaluator = ConstraintEvaluator(llm)
        score = evaluator.evaluate(self.benchmark, self.output)
        self.assertEqual(score.dimension, "Constraint Satisfaction")
        self.assertEqual(score.score, 90.0)
        self.assertEqual(score.reason, "Satisfied budget constraints.")

    def test_planning_quality_evaluator(self):
        mock_response = """
        ```json
        {
          "score": 85,
          "reason": "Good pacing."
        }
        ```
        """
        llm = MockLLM(responses=[mock_response])
        evaluator = PlanningQualityEvaluator(llm)
        score = evaluator.evaluate(self.benchmark, self.output)
        self.assertEqual(score.dimension, "Planning Quality")
        self.assertEqual(score.score, 85.0)

    def test_personalization_evaluator(self):
        mock_response = """
        ```json
        {
          "score": 95,
          "reason": "Matches interest."
        }
        ```
        """
        llm = MockLLM(responses=[mock_response])
        evaluator = PersonalizationEvaluator(llm)
        score = evaluator.evaluate(self.benchmark, self.output)
        self.assertEqual(score.dimension, "Personalization")
        self.assertEqual(score.score, 95.0)

    def test_adaptability_evaluator(self):
        mock_response = """
        ```json
        {
          "score": 80,
          "reason": "Adapts budget."
        }
        ```
        """
        llm = MockLLM(responses=[mock_response])
        evaluator = AdaptabilityEvaluator(llm)
        score = evaluator.evaluate(self.benchmark, self.output)
        self.assertEqual(score.dimension, "Adaptability")
        self.assertEqual(score.score, 80.0)

    def test_information_accuracy_evaluator(self):
        # 1. Mock responses: claim extraction JSON + final evidence judge JSON
        mock_extractor_response = """
        ```json
        [
          {
            "subject": "attraction",
            "predicate": "exists",
            "value": "true",
            "claim_type": "existence"
          }
        ]
        ```
        """
        mock_judge_response = """
        ```json
        {
          "score": 100,
          "reason": "All facts verified."
        }
        ```
        """
        # Sequential responses for first and second calls
        llm = MockLLM(responses=[mock_extractor_response, mock_judge_response])
        extractor = ClaimExtractor(llm)
        verifier = LocalKnowledgeBaseVerifier(self.temp_kb.name)
        pipeline = VerificationPipeline(extractor, verifier)

        evaluator = InformationAccuracyEvaluator(llm, pipeline)
        score = evaluator.evaluate(self.benchmark, self.output)
        self.assertEqual(score.dimension, "Information Accuracy")
        self.assertEqual(score.score, 100.0)
        self.assertEqual(score.reason, "All facts verified.")


if __name__ == "__main__":
    unittest.main()
