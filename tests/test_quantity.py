from core.quantity import normalize_quantity


def test_normalizes_units():
    assert normalize_quantity("2 litres") == "2 L"
    assert normalize_quantity("500 grams") == "500 g"
    assert normalize_quantity("1 kilogram") == "1 kg"
    assert normalize_quantity("1 pao") == "1 pao"


def test_normalizes_spoken_numbers():
    assert normalize_quantity("aadha kilo") == "1/2 kg"
    assert normalize_quantity("two") == "2"


def test_preserves_unknown_quantity_text():
    assert normalize_quantity("one large packet") == "one large packet"
    assert normalize_quantity("") == ""


def test_extracts_compact_prefix_quantities():
    from core.quantity import extract_quantity

    assert extract_quantity("500gm tomato") == ("tomato", "500 g")
    assert extract_quantity("1kg onion") == ("onion", "1 kg")


def test_extracts_quantity_with_of_between_unit_and_item():
    from core.quantity import extract_quantity

    assert extract_quantity("1 litre of milk") == ("milk", "1 L")
