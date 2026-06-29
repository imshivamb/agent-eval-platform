"""Module for transforming raw markdown content into python structures."""

from typing import Any, Dict, List
import yaml
# pyrefly: ignore [missing-import]
from markdown_it import MarkdownIt
from framework.exceptions import TransformerError

# Single shared parser instance at the module level to avoid repeated construction
_MD = MarkdownIt()


def parse_list(content: str) -> List[str]:
    """Parses all bulleted or numbered list items in markdown content.

    Args:
        content: The raw markdown content of the list section.

    Returns:
        A list of strings representing the text of each list item.
    """
    tokens = _MD.parse(content)
    items: List[str] = []
    current_item: List[str] = []
    in_item = False

    for token in tokens:
        if token.type == "list_item_open":
            in_item = True
            current_item = []
        elif token.type == "inline" and in_item:
            current_item.append(token.content)
        elif token.type == "list_item_close" and in_item:
            items.append("".join(current_item).strip())
            in_item = False

    return items


def parse_nested_lists(content: str) -> Dict[str, List[str]]:
    """Parses subheadings and the list items directly beneath them.

    Args:
        content: The raw markdown containing headings and list items.

    Returns:
        A dictionary mapping each subheading's text to its list items.
    """
    tokens = _MD.parse(content)
    result: Dict[str, List[str]] = {}

    active_heading: List[str] = []
    in_heading = False
    active_item: List[str] = []
    in_item = False
    current_list: List[str] = []

    for token in tokens:
        if token.type == "heading_open":
            # Save the previous heading and its list items if we had one
            if active_heading:
                result["".join(active_heading).strip()] = current_list
            active_heading = []
            in_heading = True
            current_list = []
        elif token.type == "inline" and in_heading:
            active_heading.append(token.content)
        elif token.type == "heading_close":
            in_heading = False
        elif token.type == "list_item_open" and active_heading:
            in_item = True
            active_item = []
        elif token.type == "inline" and in_item:
            active_item.append(token.content)
        elif token.type == "list_item_close" and in_item:
            current_list.append("".join(active_item).strip())
            in_item = False

    # Save the trailing heading
    if active_heading:
        result["".join(active_heading).strip()] = current_list

    return result


def parse_yaml_block(content: str) -> Dict[str, Any]:
    """Finds and parses the first YAML code fence block in the markdown content.

    Args:
        content: The raw markdown content.

    Returns:
        A dictionary representation of the parsed YAML content.

    Raises:
        TransformerError: If YAML parsing fails.
    """
    tokens = _MD.parse(content)

    for token in tokens:
        if token.type == "fence" and token.info == "yaml":
            try:
                result = yaml.safe_load(token.content)
                if result is None:
                    return {}
                if not isinstance(result, dict):
                    raise TransformerError("YAML block content must represent a dictionary")
                return result
            except Exception as e:
                raise TransformerError(f"Failed to parse YAML block: {e}") from e

    return {}
