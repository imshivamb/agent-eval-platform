"""Public API for parsing benchmark scenarios."""

from framework.models import Benchmark, ParsedBenchmark
from framework.parsers import parse_frontmatter, parse_sections, map_to_benchmark


def parse_benchmark_content(content: str) -> Benchmark:
    """Parses a raw markdown string and maps it to a Benchmark dataclass.

    Args:
        content: The raw markdown content with YAML frontmatter.

    Returns:
        A Benchmark dataclass instance.

    Raises:
        FrontmatterParseError: If YAML frontmatter parsing fails.
        MarkdownParseError: If markdown section parsing fails.
        MapperError: If mapping parsed content to Benchmark fails.
    """
    metadata, body = parse_frontmatter(content)
    parsed_sections = parse_sections(body)
    parsed_benchmark = ParsedBenchmark(metadata=metadata, sections=parsed_sections)
    return map_to_benchmark(parsed_benchmark)


def parse_benchmark(filepath: str) -> Benchmark:
    """Parses a markdown benchmark file on disk and maps it to a Benchmark dataclass.

    Args:
        filepath: Path to the markdown file.

    Returns:
        A Benchmark dataclass instance.

    Raises:
        FileNotFoundError: If the file does not exist.
        FrontmatterParseError: If YAML frontmatter parsing fails.
        MarkdownParseError: If markdown section parsing fails.
        MapperError: If mapping parsed content to Benchmark fails.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return parse_benchmark_content(content)
