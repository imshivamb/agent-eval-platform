"""Module for parsing YAML frontmatter from markdown documents."""

from typing import Any, Dict, Tuple
import frontmatter


class FrontmatterParseError(ValueError):
    """Raised when frontmatter is malformed or invalid."""
    pass


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Parses YAML frontmatter from a markdown string.

    Args:
        content: The raw markdown content, which may contain YAML frontmatter.

    Returns:
        A tuple of (metadata, remaining_content) where:
            - metadata is a dictionary containing the parsed frontmatter fields.
            - remaining_content is the markdown body without the frontmatter block.

    Raises:
        FrontmatterParseError: If frontmatter parsing fails due to malformed YAML.
    """
    try:
        post = frontmatter.loads(content)
        return post.metadata, post.content
    except Exception as e:
        raise FrontmatterParseError(
            f"Failed to parse YAML frontmatter: {e}"
        ) from e
