"""Public API for parsing benchmark scenarios."""

from pathlib import Path
from typing import Union
from framework.models import Benchmark, ParsedBenchmark
from framework.parsers import parse_frontmatter, parse_sections, map_to_benchmark


def parse_benchmark_text(text: str) -> Benchmark:
    """Parses raw markdown text and maps it to a Benchmark dataclass.

    Args:
        text: The raw markdown text containing YAML frontmatter.

    Returns:
        A Benchmark dataclass instance.

    Raises:
        FrontmatterParseError: If YAML frontmatter parsing fails.
        MarkdownParseError: If markdown section parsing fails.
        MapperError: If mapping parsed content to Benchmark fails.
    """
    metadata, body = parse_frontmatter(text)
    parsed_sections = parse_sections(body)
    parsed_benchmark = ParsedBenchmark(metadata=metadata, sections=parsed_sections)
    return map_to_benchmark(parsed_benchmark)


def parse_benchmark(path: Union[str, Path]) -> Benchmark:
    """Parses a markdown benchmark file on disk and maps it to a Benchmark dataclass.

    Args:
        path: Path to the markdown file (string or pathlib.Path).

    Returns:
        A Benchmark dataclass instance.

    Raises:
        FileNotFoundError: If the file does not exist.
        FrontmatterParseError: If YAML frontmatter parsing fails.
        MarkdownParseError: If markdown section parsing fails.
        MapperError: If mapping parsed content to Benchmark fails.
    """
    text = Path(path).read_text(encoding="utf-8")
    return parse_benchmark_text(text)
