"""Prompt builder for Adaptability dimension."""

from typing import List
from framework.models import AgentOutput, Benchmark
from framework.evaluation.prompts.base import build_llm_judge_prompt
from framework.llms import Message

# Detailed evaluation rubric for Adaptability
ADAPTABILITY_RUBRIC = (
    "Main Question: When circumstances change, how well does the agent revise "
    "the plan while preserving the overall experience?\n\n"
    "Note on scope: Evaluate only how well the agent adapts the itinerary to changes, "
    "disruptions, or new constraints introduced mid-travel. Do not evaluate baseline "
    "planning quality, factual correctness of attractions, or static user interests, "
    "as those are evaluated separately in other dimensions.\n\n"
    "Evaluate the adaptability quality of the travel itinerary across these three core aspects:\n\n"
    "1. Constraint Adaptation:\n"
    "   Assess how effectively the agent revises the itinerary to accommodate modified or new constraints.\n"
    "   Favor revisions that make the smallest necessary changes while preserving the overall itinerary whenever practical.\n"
    "   Consider factors such as: adapting to budget reductions, timeline shifts, or transit cancellations.\n\n"
    "2. Experience Preservation:\n"
    "   Assess how well the revised plan preserves the original travel goals, style, and interests of the traveler.\n"
    "   Consider factors such as: finding alternative activities of similar theme/vibe rather than replacing them with generic tourist options.\n\n"
    "3. Impact Mitigation:\n"
    "   Assess whether the revisions minimize cascading disruptions to the rest of the itinerary.\n"
    "   Consider factors such as: avoiding unnecessary cancellations of existing bookings and keeping alterations localized where possible.\n\n"
    "### Scoring Guidance:\n"
    "- 90–100: Excellent adaptability, smoothly resolving changes with zero friction and high experience preservation.\n"
    "- 75–89: Good adaptability resolving disruptions with minor inefficiencies or pacing compromises.\n"
    "- 50–74: Moderate adaptability; recovers from changes but sacrifices multiple travel goals or introduces excessive pacing stress.\n"
    "- 25–49: Poor adaptability; fails to meet new constraints or completely loses the traveler's preferences during revision.\n"
    "- 0–24: Not adaptable; fails to address changed circumstances entirely.\n\n"
    "Assign the score holistically across all three aspects. "
    "Do not average the aspects mechanically unless the evidence clearly supports doing so."
)


def build_adaptability_prompt(
    benchmark: Benchmark, output: AgentOutput
) -> List[Message]:
    """Generates LLM judge messages for adaptability quality assessment.

    Args:
        benchmark: The scenario benchmark details.
        output: The agent response output.

    Returns:
        List of prompt Message structures.
    """
    system_objective = (
        "You are an objective AI evaluator checking the adaptability quality "
        "of an agent's output itinerary against a benchmark scenario."
    )

    return build_llm_judge_prompt(
        system_objective, ADAPTABILITY_RUBRIC, benchmark, output
    )
