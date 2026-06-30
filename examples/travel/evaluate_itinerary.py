"""End-to-end travel agent evaluation demo.

To run this demo:
    PYTHONPATH=. python3 examples/travel/evaluate_itinerary.py
"""

import sys
from framework import (
    parse_benchmark,
    AgentOutput,
    EvaluationEngine,
    MockLLM,
    ConstraintEvaluator,
    PlanningQualityEvaluator,
    DummyEvaluator,
    TRAVEL_PROFILE,
    CONSTRAINT_SATISFACTION,
    PLANNING_QUALITY,
    INFORMATION_ACCURACY,
    PERSONALIZATION,
    ADAPTABILITY,
)


def main():
    print("=== Step 1: Ingesting Travel Agent Benchmark Scenario ===")
    filepath = "evals/scenarios/travel-agent/budget-constrained-itinerary.md"
    try:
        benchmark = parse_benchmark(filepath)
        print(f"Successfully loaded and parsed benchmark: '{benchmark.name}'")
    except Exception as e:
        print(f"Error parsing scenario: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n=== Step 2: Preparing Mock Agent Output ===")
    # A travel agent's output that we want to evaluate
    agent_output = AgentOutput(
        content=(
            "29-Day Backpacking Itinerary for Japan and South Korea.\n"
            "Budget: ₹240,000 (INR) overall.\n"
            "Route: Seoul (7 days) -> Tokyo (14 days) -> Kyoto (8 days).\n"
            "Accommodation: Guesthouses and budget hostels throughout."
        ),
        metadata={},
    )
    print("Agent Output loaded successfully.")

    print("\n=== Step 3: Setting Up Mock LLM Responses for Judges ===")
    # Simulate LLM Judge responses. The MockLLM will return these structured JSON strings.
    mock_responses = [
        # Constraint Satisfaction JSON response
        """
        ```json
        {
          "score": 95,
          "reason": "The agent perfectly stayed within the 250,000 INR budget (using 240,000 INR) and matched the 29-day length and backpacking style."
        }
        ```
        """,
        # Planning Quality JSON response
        """
        ```json
        {
          "score": 88,
          "reason": "Geographically sensible route (Seoul to Tokyo to Kyoto). Pacing is realistic, though Kyoto could be trimmed slightly."
        }
        ```
        """,
    ]
    llm = MockLLM(responses=mock_responses)
    print("Mock LLM client configured.")

    print("\n=== Step 4: Registering Evaluators & Profiles ===")
    # Registering evaluators corresponding to the TRAVEL_PROFILE dimensions using standard constants
    evaluators = {
        CONSTRAINT_SATISFACTION: ConstraintEvaluator(llm),
        PLANNING_QUALITY: PlanningQualityEvaluator(llm),
        # Using DummyEvaluator from testing package for features not yet backed by real LLM judges
        INFORMATION_ACCURACY: DummyEvaluator(
            INFORMATION_ACCURACY, 85.0, "All attraction facts verified."
        ),
        PERSONALIZATION: DummyEvaluator(
            PERSONALIZATION,
            90.0,
            "Thrift shopping recommendations fit the backpacker vibe.",
        ),
        ADAPTABILITY: DummyEvaluator(
            ADAPTABILITY, 75.0, "Baseline adaptability checks passed."
        ),
    }

    engine = EvaluationEngine(evaluators=evaluators)
    print(f"EvaluationEngine initialized with {len(evaluators)} evaluators.")

    print("\n=== Step 5: Executing Evaluation Engine ===")
    try:
        result = engine.evaluate(benchmark, agent_output, TRAVEL_PROFILE)
    except Exception as e:
        print(f"Evaluation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n==================== EVALUATION REPORT ====================")
    print(f"Benchmark Scenario: {result.benchmark_name} ({result.benchmark_id})")
    print(f"Applied Profile:    {TRAVEL_PROFILE.name}")
    print(f"Overall Score:      {result.overall_score:.2f} / 100")
    print(
        f"Pass Status:        {'PASS' if result.passed else 'FAIL'} (Threshold: {TRAVEL_PROFILE.pass_threshold})"
    )
    print("\nDimension Breakdown:")
    for ds in result.dimension_scores:
        weight = TRAVEL_PROFILE.weights[ds.dimension]
        print(f"\n- {ds.dimension} (Weight: {weight}%)")
        print(f"  Score:  {ds.score}")
        print(f"  Reason: {ds.reason}")
    print("===========================================================")


if __name__ == "__main__":
    main()
