"""Verification subsystem helper utilities."""


def normalize_key(text: str) -> str:
    """Normalizes keys for robust string matching (lowercase alphanumeric)."""
    return "".join(c for c in text.lower() if c.isalnum())


def _clean_numeric_value(val: str) -> str:
    """Removes common currency symbols, commas, and currency codes, leaving alphanumeric/numeric chars."""
    val = val.upper()
    for clean_target in [
        "JPY",
        "INR",
        "USD",
        "KRW",
        "EUR",
        "GBP",
        "YEN",
        "RUPEES",
        "¥",
        "₹",
        "$",
        "€",
        "£",
        ",",
    ]:
        val = val.replace(clean_target, "")
    return val.strip()


def values_are_equivalent(expected: str, actual: str) -> bool:
    """Checks if two values are equivalent, handling numeric/currency normalizations."""
    # 1. Direct normalized string check
    norm_expected = expected.strip().lower()
    norm_actual = actual.strip().lower()
    if norm_expected == norm_actual:
        return True

    # 2. Try cleaning numeric values (e.g., "3000 JPY" vs "¥3,000")
    clean_exp = _clean_numeric_value(expected)
    clean_act = _clean_numeric_value(actual)

    if clean_exp == clean_act:
        return True

    # 3. Try parsing as float if they are numeric
    try:
        if float(clean_exp) == float(clean_act):
            return True
    except ValueError:
        pass

    return False
