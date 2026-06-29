"""Module for parsing sections from markdown bodies."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
# pyrefly: ignore [missing-import]
from markdown_it import MarkdownIt
from framework.exceptions import MarkdownParseError
from framework.models import ParsedSections

# Single shared parser instance at the module level to avoid repeated construction
_MD = MarkdownIt()


@dataclass
class Heading:
    """Represents a heading parsed from markdown."""

    level: int
    text: str
    start_line: int
    end_line: int


def _require_section(sections: Dict[str, str], name: str) -> str:
    """Ensures a required section is present in sections dictionary.

    Args:
        sections: Dictionary of headings to raw contents.
        name: Name of the required section.

    Returns:
        The content of the required section.

    Raises:
        MarkdownParseError: If the section is missing.
    """
    if name not in sections:
        raise MarkdownParseError(f"Missing required section: '{name}'")
    return sections[name]


def parse_sections(content: str) -> ParsedSections:
    """Splits a markdown document body into sections and returns ParsedSections.

    Automatically detects the highest heading level (H1, H2, etc.) present in
    the document and splits the text into sections using those headings.

    Args:
        content: The raw markdown content body (without frontmatter).

    Returns:
        A ParsedSections dataclass containing raw markdown text for each section.

    Raises:
        MarkdownParseError: If any required section is missing.
    """
    tokens = _MD.parse(content)
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
        raise MarkdownParseError("No headings found in the markdown body")

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

    # Validate and map to ParsedSections dataclass
    description = _require_section(sections, "Description")
    prompt = _require_section(sections, "User Prompt")
    constraints = _require_section(sections, "Extracted Constraints")
    expected_behavior = _require_section(sections, "Expected Behaviour")
    evaluation_criteria = _require_section(sections, "Evaluation Criteria")
    pass_criteria = _require_section(sections, "Pass Criteria")
    failure_conditions = _require_section(sections, "Failure Conditions")
    notes = sections.get("Notes")

    return ParsedSections(
        description=description,
        prompt=prompt,
        constraints=constraints,
        expected_behavior=expected_behavior,
        evaluation_criteria=evaluation_criteria,
        pass_criteria=pass_criteria,
        failure_conditions=failure_conditions,
        notes=notes,
    )
