import pytest
from core.quantity import normalize_quantity


def test_quantity_normalizer_is_not_implemented_in_stage_one():
    with pytest.raises(NotImplementedError):
        normalize_quantity("aadha kilo")
