import unittest
from framework.models import AgentOutput, Benchmark, DimensionScore, EvaluationProfile
from framework.evaluation.engine import EvaluationEngine
from framework.evaluation.base import BaseEvaluator
from framework.exceptions import EvaluationError


class MockEvaluator(BaseEvaluator):
    """Simple mock evaluator for engine tests."""

    def __init__(self, dimension: str, score: float):
        self._dimension = dimension
        self._score = score

    def evaluate(self, benchmark: Benchmark, output: AgentOutput) -> DimensionScore:
        return DimensionScore(
            dimension=self._dimension,
            score=self._score,
            reason=f"Scored {self._score} for {self._dimension}",
        )


class TestEngine(unittest.TestCase):
    """Tests the EvaluationEngine class."""

    def setUp(self):
        self.benchmark = Benchmark(
            benchmark_id="test-bench",
            name="Test Scenario",
            description="Desc",
            prompt="Prompt",
            constraints={},
            expected_behavior=[],
            evaluation_criteria={
                "Constraint Satisfaction": [],
                "Planning Quality": [],
            },
            pass_criteria=[],
            failure_conditions=[],
            notes=[],
        )
        self.output = AgentOutput(content="test content")

    def test_engine_successful_evaluation(self):
        # Setup evaluators
        evaluators = {
            "Constraint Satisfaction": MockEvaluator("Constraint Satisfaction", 90.0),
            "Planning Quality": MockEvaluator("Planning Quality", 80.0),
        }
        engine = EvaluationEngine(evaluators)

        # Profile weighting: Constraint Satisfaction: 60%, Planning Quality: 40%
        # Math expected: (90.0 * 60 + 80.0 * 40) / 100 = 86.0
        profile = EvaluationProfile(
            name="test-profile",
            weights={"Constraint Satisfaction": 60.0, "Planning Quality": 40.0},
            pass_threshold=85.0,
        )

        result = engine.evaluate(self.benchmark, self.output, profile)
        self.assertEqual(result.overall_score, 86.0)
        self.assertTrue(result.passed)
        self.assertEqual(len(result.dimension_scores), 2)

    def test_engine_missing_evaluator(self):
        evaluators = {
            "Constraint Satisfaction": MockEvaluator("Constraint Satisfaction", 90.0)
        }
        engine = EvaluationEngine(evaluators)
        profile = EvaluationProfile(
            name="test-profile",
            weights={"Constraint Satisfaction": 60.0, "Planning Quality": 40.0},
            pass_threshold=85.0,
        )
        with self.assertRaises(EvaluationError) as context:
            engine.evaluate(self.benchmark, self.output, profile)
        self.assertIn("No evaluator registered", str(context.exception))

    def test_engine_mismatched_benchmark_criteria(self):
        evaluators = {
            "Constraint Satisfaction": MockEvaluator("Constraint Satisfaction", 90.0),
            "Planning Quality": MockEvaluator("Planning Quality", 80.0),
        }
        engine = EvaluationEngine(evaluators)
        # Profile uses unknown dimension not in benchmark evaluation_criteria
        profile = EvaluationProfile(
            name="test-profile",
            weights={"Constraint Satisfaction": 60.0, "Unknown Dimension": 40.0},
            pass_threshold=85.0,
        )
        with self.assertRaises(EvaluationError) as context:
            engine.evaluate(self.benchmark, self.output, profile)
        self.assertIn("is not defined in benchmark", str(context.exception))

    def test_engine_mismatched_evaluator_dimension_name(self):
        # Evaluator claims to return Planning Quality but returns Constraint Satisfaction
        evaluators = {
            "Constraint Satisfaction": MockEvaluator("Constraint Satisfaction", 90.0),
            "Planning Quality": MockEvaluator("Constraint Satisfaction", 80.0),
        }
        engine = EvaluationEngine(evaluators)
        profile = EvaluationProfile(
            name="test-profile",
            weights={"Constraint Satisfaction": 60.0, "Planning Quality": 40.0},
            pass_threshold=85.0,
        )
        with self.assertRaises(EvaluationError) as context:
            engine.evaluate(self.benchmark, self.output, profile)
        self.assertIn("returned score for dimension", str(context.exception))


if __name__ == "__main__":
    unittest.main()
