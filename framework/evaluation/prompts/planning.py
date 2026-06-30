"""Prompt builder for Planning Quality dimension."""

from typing import List
from framework.models import AgentOutput, Benchmark
from framework.evaluation.prompts.base import build_llm_judge_prompt
from framework.llms import Message


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

    criteria_rubric = (
        "Assess the planning quality of the itinerary across these key aspects:\n"
        "1. Route Logic & Geographic Efficiency: Does the route flow logically, or does it backtrack?\n"
        "2. Accommodation Stability: Are unnecessary changes/check-ins minimized?\n"
        "3. Pacing & Balance: Is there a realistic balance between travel, work, and sightseeing?"
    )

    return build_llm_judge_prompt(
        system_objective, criteria_rubric, benchmark, output
    )
