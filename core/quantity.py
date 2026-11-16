"""Quantity parsing and light normalization for English, Hindi and Hinglish."""

import re

from core.vocabulary import NUMBER_WORDS, UNIT_ALIASES

_NUMBER_PATTERN = (
    r"(?:\d+(?:\.\d+)?|\d+\s*/\s*\d+|half|quarter|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"a|an|aadha|pauna|sawa|dedh|ek|do|teen|char|paanch|chhe|saat|aath|nau|das|"
    r"आधा|आधे|पौना|सवा|डेढ़|ढाई|एक|दो|तीन|चार|पांच|पाँच|छह|सात|आठ|नौ|दस)"
)
_UNIT_PATTERN = (
    r"(?:kilograms?|kgs?|kilos?|kg|किलोग्राम|किलो|pao|पाव|grams?|gms?|gm|g|ग्राम|"
    r"litres?|liters?|litre|liter|ltr|lt|l|लीटर|millilitres?|milliliters?|ml|मिलीलीटर|"
    r"pieces?|pcs?|pc|पिस|नग|dozen|दर्जन|packs?|packets?|pack|पैकेट)"
)
# Permit compact forms such as 500gm and 1kg, but require a word boundary after the unit.
_QUANTITY_RE = re.compile(rf"(?<!\w)({_NUMBER_PATTERN})\s*({_UNIT_PATTERN})(?!\w)", re.IGNORECASE)
_PREFIX_RE = re.compile(rf"^\s*({_NUMBER_PATTERN})\s*({_UNIT_PATTERN})\s+(.+?)\s*$", re.IGNORECASE)
_PREFIX_COUNT_RE = re.compile(rf"^\s*({_NUMBER_PATTERN})\s+(.+?)\s*$", re.IGNORECASE)
_SUFFIX_RE = re.compile(rf"\s+({_NUMBER_PATTERN})\s*({_UNIT_PATTERN})\s*$", re.IGNORECASE)
_SUFFIX_COUNT_RE = re.compile(
    r"\s+(\d+(?:\.\d+)?|\d+\s*/\s*\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"ek|do|teen|char|paanch|chhe|saat|aath|nau|das|एक|दो|तीन|चार|पांच|पाँच|छह|सात|आठ|नौ|दस)\s*$",
    re.IGNORECASE,
)


def _number(value: str) -> str:
    clean = value.strip().lower()
    if clean in NUMBER_WORDS:
        return NUMBER_WORDS[clean]
    return re.sub(r"\s*/\s*", "/", clean)


def _clean_item(value: str) -> str:
    value = value.strip(" ,.-")
    value = re.sub(r"^(?:of|का|की|के)\s+", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+(?:of|का|की|के)$", "", value, flags=re.IGNORECASE)
    return value.strip()


def normalize_quantity(value: str) -> str:
    text = " ".join(str(value or "").strip().split())
    if not text:
        return ""
    match = _QUANTITY_RE.fullmatch(text)
    if match:
        amount, unit = match.groups()
        return f"{_number(amount)} {UNIT_ALIASES.get(unit.lower(), unit)}"
    return _number(text) if text.lower() in NUMBER_WORDS else text


def extract_quantity(text: str) -> tuple[str, str]:
    """Return (item text, normalized quantity), accepting prefix and suffix forms."""
    value = " ".join(text.strip().split())
    if not value:
        return "", ""

    match = _PREFIX_RE.match(value)
    if match:
        amount, unit, item = match.groups()
        return _clean_item(item), normalize_quantity(f"{amount} {unit}")

    match = _PREFIX_COUNT_RE.match(value)
    if match:
        amount, item = match.groups()
        # Only treat a leading bare number as a quantity when there is a clear item after it.
        return _clean_item(item), normalize_quantity(amount)

    match = _SUFFIX_RE.search(value)
    if match:
        amount, unit = match.groups()
        item = _clean_item(value[:match.start()])
        return item, normalize_quantity(f"{amount} {unit}")

    match = _SUFFIX_COUNT_RE.search(value)
    if match:
        return _clean_item(value[:match.start()]), normalize_quantity(match.group(1))

    return _clean_item(value), ""
