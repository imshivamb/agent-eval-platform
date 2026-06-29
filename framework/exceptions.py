"""Common exceptions for the evaluation framework."""


class BenchmarkError(Exception):
    """Base class for all benchmark-related exceptions."""

    pass


class FrontmatterParseError(BenchmarkError):
    """Raised when parsing YAML frontmatter from content fails."""

    pass


class MarkdownParseError(BenchmarkError):
    """Raised when parsing markdown body into sections fails."""

    pass


class TransformerError(BenchmarkError):
    """Raised when transforming raw markdown sections into Python structures fails."""

    pass


class MapperError(BenchmarkError):
    """Raised when mapping parsed content to a Benchmark dataclass fails."""

    pass


class EvaluationError(Exception):
    """Raised when evaluation orchestration or execution fails."""

    pass

