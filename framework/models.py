from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Benchmark:
    """Represents a single evaluation scenario.

    Stores the parsed details of the benchmark scenario (e.g., from markdown).
    """

    benchmark_id: str
    name: str
    description: str
    prompt: str
    constraints: Dict[str, Any]
    expected_behavior: List[str]
    evaluation_criteria: Dict[str, List[str]]
    pass_criteria: List[str]
    failure_conditions: List[str]
    notes: List[str]


@dataclass
class AgentOutput:
    """Represents the raw response/output produced by an AI agent."""

    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DimensionScore:
    """Stores the score and justification for a single evaluation dimension."""

    dimension: str
    score: float
    reason: str


@dataclass
class EvaluationResult:
    """Represents the final evaluation outcome for a benchmark scenario."""

    benchmark_id: str
    benchmark_name: str
    overall_score: float
    dimension_scores: List[DimensionScore]
    passed: bool


@dataclass
class EvaluationProfile:
    """Defines the name and dimension weights for a specific evaluation domain."""

    name: str
    weights: Dict[str, float]
