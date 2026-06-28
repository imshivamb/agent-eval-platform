"""Module for parsing sections from markdown bodies."""

from dataclasses import dataclass
from typing import Dict, List, Optional
# pyrefly: ignore [missing-import]
from markdown_it import MarkdownIt


@dataclass
class Heading:
    """Represents a heading parsed from markdown."""

    level: int
    text: str
    start_line: int
    end_line: int


def parse_sections(content: str) -> Dict[str, str]:
    """Splits a markdown document body into sections based on top-level headings.

    Automatically detects the highest heading level (H1, H2, etc.) present in
    the document and splits the text into sections using those headings.

    Args:
        content: The raw markdown content body (without frontmatter).

    Returns:
        A dictionary mapping each heading's text to its corresponding raw
        markdown content.
    """
    md = MarkdownIt()
    tokens = md.parse(content)
    lines = content.splitlines()

    # Gather all headings and their line offsets using a simple stateful pass
    headings: List[Heading] = []
    current_heading: Optional[Heading] = None

    for token in tokens:
        if token.type == "heading_open":
            if not token.map:
                continue
            current_heading = Heading(
                level=int(token.tag[1]),
                text="",
                start_line=token.map[0],
                end_line=token.map[1],
            )
        elif token.type == "inline" and current_heading is not None:
            current_heading.text += token.content
        elif token.type == "heading_close" and current_heading is not None:
            # We match the tag (e.g. h1, h2) to ensure correct nesting closure
            if token.tag == f"h{current_heading.level}":
                headings.append(current_heading)
                current_heading = None

    if not headings:
        return {}

    # Identify the primary (highest-level) headings to use as section splitters
    primary_level = min(h.level for h in headings)
    primary_headings = [h for h in headings if h.level == primary_level]

    sections: Dict[str, str] = {}
    for idx, heading in enumerate(primary_headings):
        # The section content starts immediately after the heading
        content_start = heading.end_line

        # The section content ends where the next primary heading begins
        if idx + 1 < len(primary_headings):
            content_end = primary_headings[idx + 1].start_line
        else:
            content_end = len(lines)

        section_content = "\n".join(lines[content_start:content_end]).strip()
        sections[heading.text] = section_content

    return sections
