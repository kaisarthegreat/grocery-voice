"""Rule-based first-pass parser for short English, Hindi and Hinglish lists."""

import re

from core.quantity import extract_quantity
from core.vocabulary import GROCERY_ALIASES

_SEPARATOR_RE = re.compile(r"\s*(?:,|;|\n|\b(?:and|aur)\b|और|तथा)\s*", re.IGNORECASE)


def _canonical_name(value: str) -> str:
    clean = " ".join(value.strip(" \t\r\n,.;:-").split())
    if not clean:
        return ""
    return GROCERY_ALIASES.get(clean.casefold(), clean)


def parse_grocery_text(text: str) -> list[dict[str, str]]:
    """Parse a spoken/typed list into item and quantity pairs.

    This is deterministic rule-based parsing, not an LLM. Unknown item names
    remain in the result so the user can correct them rather than lose data.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    source = text.strip()
    if not source:
        return []
    if len(source) > 2000:
        raise ValueError("text must be 2000 characters or fewer")

    results: list[dict[str, str]] = []
    for segment in _SEPARATOR_RE.split(source):
        segment = segment.strip()
        if not segment:
            continue
        item_text, quantity = extract_quantity(segment)
        name = _canonical_name(item_text)
        if name:
            results.append({"name": name, "quantity": quantity})
    return results
