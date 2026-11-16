import pytest

from core.parser import parse_grocery_text


def test_parses_english_items_with_prefix_quantities():
    assert parse_grocery_text("2 litres milk, 1 kg potatoes and 500 g onions") == [
        {"name": "Milk", "quantity": "2 L"},
        {"name": "Potatoes", "quantity": "1 kg"},
        {"name": "Onions", "quantity": "500 g"},
    ]


def test_parses_hinglish_items_and_half_quantity():
    assert parse_grocery_text("aadha kilo aloo aur 1 litre doodh") == [
        {"name": "Potatoes", "quantity": "1/2 kg"},
        {"name": "Milk", "quantity": "1 L"},
    ]


def test_parses_common_hindi_words():
    assert parse_grocery_text("दो किलो आलू, आधा किलो प्याज और एक लीटर दूध") == [
        {"name": "Potatoes", "quantity": "2 kg"},
        {"name": "Onions", "quantity": "1/2 kg"},
        {"name": "Milk", "quantity": "1 L"},
    ]


def test_supports_quantity_after_item_name():
    assert parse_grocery_text("milk 2 litres, potatoes 1 kg") == [
        {"name": "Milk", "quantity": "2 L"},
        {"name": "Potatoes", "quantity": "1 kg"},
    ]


def test_preserves_unknown_item_names():
    assert parse_grocery_text("2 packets cornflakes") == [
        {"name": "cornflakes", "quantity": "2 packs"}
    ]


def test_empty_text_returns_empty_list():
    assert parse_grocery_text("  ") == []


def test_rejects_non_string_and_oversized_input():
    with pytest.raises(TypeError):
        parse_grocery_text(None)
    with pytest.raises(ValueError):
        parse_grocery_text("x" * 2001)


def test_parses_compact_quantities_without_spaces():
    assert parse_grocery_text("500gm tomato, 1kg onion") == [
        {"name": "Tomatoes", "quantity": "500 g"},
        {"name": "Onions", "quantity": "1 kg"},
    ]


def test_parses_quantity_phrases_with_of():
    assert parse_grocery_text("1 litre of milk and 2 kg of potatoes") == [
        {"name": "Milk", "quantity": "1 L"},
        {"name": "Potatoes", "quantity": "2 kg"},
    ]
