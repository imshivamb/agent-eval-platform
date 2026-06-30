"""Prompt builder for Personalization dimension."""

from typing import List
from framework.models import AgentOutput, Benchmark
from framework.evaluation.prompts.base import build_llm_judge_prompt
from framework.llms import Message

# Detailed evaluation rubric for Personalization
PERSONALIZATION_RUBRIC = (
    "Main Question: Considering only personalization, does the itinerary feel "
    "specifically tailored to this traveler's stated preferences, interests, and profile?\n\n"
    "Note on scope: Evaluate only how well the itinerary aligns with the traveler's stated preferences, "
    "goals, interests, and style. Do not evaluate route efficiency, daily pacing, factual correctness "
    "of attractions, or strict duration constraints, as those are evaluated separately in other dimensions.\n\n"
    "Evaluate the personalization quality of the travel itinerary across these three core aspects:\n\n"
    "1. Preference Alignment:\n"
    "   Assess whether the activities, sightseeing spots, and recommendations match the traveler's listed interests.\n"
    "   Consider both explicit preferences stated by the traveler and reasonable implications of those preferences "
    "   (e.g., backpacking implies budget lodging and public transit), but do not invent unsupported interests.\n"
    "   Consider factors such as: incorporating stated hobbies (e.g., photography, thrift shopping, café culture) and aligning with the backpacking travel style.\n\n"
    "2. Context & Constraints Integration:\n"
    "   Assess whether lodging selection and pacing integrate cleanly with the traveler's daily constraints.\n"
    "   Consider factors such as: scheduling around remote work windows and respecting walking preferences or physical limits.\n\n"
    "3. Recommendation Relevance:\n"
    "   Assess whether the recommendations are highly relevant to this specific traveler's profile rather than boilerplate tourist stops.\n"
    "   Consider factors such as: localized recommendations that directly serve the traveler's stated and implied interests.\n\n"
    "### Scoring Guidance:\n"
    "- 90–100: Excellent personalization, highly tailored to the traveler's profile with deep alignment.\n"
    "- 75–89: Good personalization matching major interests, with minor generic elements.\n"
    "- 50–74: Moderate personalization; feels somewhat generic or overlooks multiple stated preferences.\n"
    "- 25–49: Poor personalization; ignores key interests or remote work requirements.\n"
    "- 0–24: Not personalized at all; entirely boilerplate itinerary.\n\n"
    "Assign the score holistically across all three aspects. "
    "Do not average the aspects mechanically unless the evidence clearly supports doing so."
)


def build_personalization_prompt(
    benchmark: Benchmark, output: AgentOutput
) -> List[Message]:
    """Generates LLM judge messages for personalization quality assessment.

    Args:
        benchmark: The scenario benchmark details.
        output: The agent response output.

    Returns:
        List of prompt Message structures.
    """
    system_objective = (
        "You are an objective AI evaluator checking the personalization quality "
        "of an agent's output itinerary against a benchmark scenario."
    )

    return build_llm_judge_prompt(
        system_objective, PERSONALIZATION_RUBRIC, benchmark, output
    )
