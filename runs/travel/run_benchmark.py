"""Orchestration script to run a travel agent evaluation experiment.

To run this experiment:
    PYTHONPATH=. python3 runs/travel/run_benchmark.py
"""

import sys
from framework import (
    parse_benchmark,
    EvaluationEngine,
    MockLLM,
    ConstraintEvaluator,
    PlanningQualityEvaluator,
    PersonalizationEvaluator,
    AdaptabilityEvaluator,
    InformationAccuracyEvaluator,
    LocalKnowledgeBaseVerifier,
    ClaimExtractor,
    VerificationPipeline,
    VerificationStatus,
    TRAVEL_PROFILE,
    CONSTRAINT_SATISFACTION,
    PLANNING_QUALITY,
    INFORMATION_ACCURACY,
    PERSONALIZATION,
    ADAPTABILITY,
)
from agents.travel import TravelPlanningAgent


def print_report(result, report):
    """Prints a structured visual console evaluation report."""
    print("\n==================== EVALUATION REPORT ====================")
    print(f"Benchmark Scenario: {result.benchmark_name} ({result.benchmark_id})")
    print(f"Applied Profile:    {TRAVEL_PROFILE.name}")
    print(f"Overall Score:      {result.overall_score:.2f} / 100")
    print(
        f"Pass Status:        {'PASS' if result.passed else 'FAIL'} (Threshold: {TRAVEL_PROFILE.pass_threshold})"
    )

    print("\nExtracted Claims & Verifications")
    print("-----------------------------------------------------------")
    for ev in report.evidence:
        status_symbol = "✓" if ev.status == VerificationStatus.VERIFIED else "✗"
        print(
            f"{status_symbol} {ev.claim.subject} -> {ev.claim.predicate}: "
            f"claimed '{ev.claim.value}' (Expected: '{ev.expected_value or 'N/A'}')"
        )
    print("-----------------------------------------------------------")
    print("Verification Summary")
    print(f"- Verified:  {report.verified_count}")
    print(f"- Refuted:   {report.refuted_count}")
    print(f"- Unknown:   {report.unknown_count}")
    print(f"- Not Found: {report.not_found_count}")
    print("-----------------------------------------------------------")

    print("\nDimension Breakdown:")
    for ds in result.dimension_scores:
        weight = TRAVEL_PROFILE.weights[ds.dimension]
        print(f"\n- {ds.dimension} (Weight: {weight}%)")
        print(f"  Score:  {ds.score}")
        print(f"  Reason: {ds.reason}")
    print("===========================================================")


def main():
    # 1. Ingest Travel Agent Benchmark Scenario
    filepath = "evals/scenarios/travel-agent/budget-constrained-itinerary.md"
    try:
        benchmark = parse_benchmark(filepath)
    except Exception as e:
        print(f"Error parsing scenario: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Setup Mock Responses for Agent Generation and Evaluators
    mock_responses = [
        # Call 0: TravelAgent generating the itinerary output
        "29-Day Backpacking Itinerary for Japan and South Korea.\n"
        "Budget: ₹240,000 (INR) overall.\n"
        "Route: Seoul (7 days) -> Tokyo (14 days) -> Kyoto (8 days).\n"
        "Accommodation: Guesthouses and budget hostels throughout.",
        # Call 1: Constraint Satisfaction JSON response
        """
        ```json
        {
          "score": 95,
          "reason": "The agent perfectly stayed within the 250,000 INR budget (using 240,000 INR) and matched the 29-day length and backpacking style."
        }
        ```
        """,
        # Call 2: Planning Quality JSON response
        """
        ```json
        {
          "score": 88,
          "reason": "Geographically sensible route (Seoul to Tokyo to Kyoto). Pacing is realistic, though Kyoto could be trimmed slightly."
        }
        ```
        """,
        # Call 3: Information Accuracy - Claim Extraction LLM Output
        """
        ```json
        [
          {
            "subject": "gyeongbokgung",
            "predicate": "closed_days",
            "value": "Tuesday",
            "claim_type": "timing"
          },
          {
            "subject": "teamlab_planets",
            "predicate": "exists",
            "value": "true",
            "claim_type": "existence"
          }
        ]
        ```
        """,
        # Call 4: Information Accuracy - Final Evidence Grading LLM Output
        """
        ```json
        {
          "score": 98,
          "reason": "All extracted factual claims (Gyeongbokgung closing days, TeamLab Planets existence) were verified against ground-truth authoritative records."
        }
        ```
        """,
        # Call 5: Personalization JSON response
        """
        ```json
        {
          "score": 92,
          "reason": "Excellent tailoring. Directly scheduled around the traveler's 4-hour remote work slots, recommended thrift shops in Harajuku, and aligned with walking preferences."
        }
        ```
        """,
        # Call 6: Adaptability JSON response
        """
        ```json
        {
          "score": 80,
          "reason": "Successfully handled intermediate flight delays and budget reduction of 10,000 INR by shifting from express rail to standard transit, keeping primary sightseeing intact."
        }
        ```
        """,
    ]
    llm = MockLLM(responses=mock_responses)

    # 3. Create Travel Planning Agent
    agent = TravelPlanningAgent(llm)

    # 4. Generate the itinerary from benchmark user prompt
    agent_output = agent.run(benchmark.prompt)

    # 5. Initialize the verification pipeline using Dependency Injection
    verifier = LocalKnowledgeBaseVerifier("ground_truth/japan_demo.json")
    extractor = ClaimExtractor(llm)
    pipeline = VerificationPipeline(extractor, verifier)

    # 6. Setup the evaluation engine with evaluators
    evaluators = {
        CONSTRAINT_SATISFACTION: ConstraintEvaluator(llm),
        PLANNING_QUALITY: PlanningQualityEvaluator(llm),
        INFORMATION_ACCURACY: InformationAccuracyEvaluator(llm, pipeline),
        PERSONALIZATION: PersonalizationEvaluator(llm),
        ADAPTABILITY: AdaptabilityEvaluator(llm),
    }
    engine = EvaluationEngine(evaluators=evaluators)

    # 7. Evaluate the itinerary
    try:
        result = engine.evaluate(benchmark, agent_output, TRAVEL_PROFILE)
    except Exception as e:
        print(f"Evaluation failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 8. Extract verifier report for print presentation layout
    pipeline_llm = MockLLM(responses=[mock_responses[3]])
    demo_pipeline = VerificationPipeline(ClaimExtractor(pipeline_llm), verifier)
    report = demo_pipeline.run(agent_output)

    # 9. Print final report
    print_report(result, report)


if __name__ == "__main__":
    main()
