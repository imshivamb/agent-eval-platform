"""Generic evaluation framework for AI agents."""

from framework.models import (
    Benchmark,
    AgentOutput,
    DimensionScore,
    EvaluationResult,
    EvaluationProfile,
    ParsedSections,
    ParsedBenchmark,
)
from framework.parser import parse_benchmark, parse_benchmark_content
