import pytest
from core.parser import parse_grocery_text


def test_parser_is_not_implemented_in_stage_one():
    with pytest.raises(NotImplementedError):
        parse_grocery_text("2 litres milk")
