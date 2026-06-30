"""Prompt builder for Constraint Satisfaction dimension."""

from typing import List
import yaml
from framework.models import AgentOutput, Benchmark
from framework.evaluation.prompts.base import build_llm_judge_prompt
from framework.llms import Message


def build_constraint_prompt(
    benchmark: Benchmark, output: AgentOutput
) -> List[Message]:
    """Generates LLM judge messages for constraint satisfaction checking.

    Args:
        benchmark: The scenario benchmark details.
        output: The agent response output.

    Returns:
        List of prompt Message structures.
    """
    system_objective = (
        "You are an objective AI evaluator checking if an agent's output satisfies "
        "the explicit constraints of a benchmark scenario."
    )

    constraints_str = (
        yaml.dump(benchmark.constraints, default_flow_style=False)
        if benchmark.constraints
        else "No explicit constraints defined."
    )

    criteria_rubric = (
        "Analyze the agent output and determine if every constraint listed "
        "below is satisfied.\n"
        f"Explicit constraints to verify:\n{constraints_str}"
    )

    return build_llm_judge_prompt(
        system_objective, criteria_rubric, benchmark, output
    )
