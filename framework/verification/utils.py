"""Verification subsystem helper utilities."""


def normalize_key(text: str) -> str:
    """Normalizes keys for robust string matching (lowercase alphanumeric)."""
    return "".join(c for c in text.lower() if c.isalnum())
