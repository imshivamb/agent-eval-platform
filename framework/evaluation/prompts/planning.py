"""Prompt builder for Planning Quality dimension."""

from typing import List
from framework.models import AgentOutput, Benchmark
from framework.evaluation.prompts.base import build_llm_judge_prompt
from framework.llms import Message

# Detailed evaluation rubric for Planning Quality
PLANNING_RUBRIC = (
    "Main Question: Considering only planning quality, is this itinerary organized in the best possible way for the traveler?\n\n"
    "Note on scope: Evaluate only the organization and structure of the itinerary. "
    "Do not consider factual accuracy, personalization, or whether explicit user constraints were satisfied, "
    "as those are evaluated separately in other dimensions.\n\n"
    "Evaluate the planning quality of the travel itinerary across these six core aspects:\n\n"
    "1. Route Logic & Geographic Efficiency:\n"
    "   Assess whether the itinerary minimizes unnecessary travel while maintaining a logical progression.\n"
    "   Consider factors such as: unnecessary backtracking, revisiting cities, or inefficient long-distance jumps.\n\n"
    "2. Accommodation Stability:\n"
    "   Assess whether stays are grouped effectively to avoid unnecessary overhead.\n"
    "   Consider factors such as: changing hotels/guesthouses every night, daily packing/unpacking, or not grouping activities around the active lodging node.\n\n"
    "3. Daily Pacing & Balance:\n"
    "   Assess whether the activities are realistic and pacing feels balanced.\n"
    "   Consider factors such as: overloading single days with 5+ major sites, not leaving transit buffers, or conflicting with remote work hours.\n\n"
    "4. Time & Transit Utilization:\n"
    "   Assess whether transit schedules are optimized for convenience and cost.\n"
    "   Consider factors such as: losing full days to slow daylight transits, choosing complex routes with tight/unrealistic transfer connections.\n\n"
    "5. Trip Flow & Cohesion:\n"
    "   Assess whether the sequence of cities, theme, and travel flow feel natural and coherent rather than disjointed, scattered, or random.\n\n"
    "6. Trade-off Optimization:\n"
    "   Assess whether the plan demonstrates balanced decisions between travel convenience, fatigue, cost, and traveler experience.\n\n"
    "### Scoring Guidance:\n"
    "- 90–100: Excellent planning with only minor improvements possible.\n"
    "- 75–89: Good planning with some inefficiencies.\n"
    "- 50–74: Noticeable planning problems that reduce the overall experience.\n"
    "- 25–49: Major inefficiencies or unrealistic daily pacing.\n"
    "- 0–24: Poorly organized itinerary.\n\n"
    "Assign the score holistically across all six aspects. "
    "Do not average the aspects mechanically unless the evidence clearly supports doing so."
)


def build_planning_prompt(
    benchmark: Benchmark, output: AgentOutput
) -> List[Message]:
    """Generates LLM judge messages for planning quality assessment.

    Args:
        benchmark: The scenario benchmark details.
        output: The agent response output.

    Returns:
        List of prompt Message structures.
    """
    system_objective = (
        "You are an objective AI evaluator checking the planning quality "
        "of an agent's output itinerary against a benchmark scenario."
    )

    return build_llm_judge_prompt(
        system_objective, PLANNING_RUBRIC, benchmark, output
    )
