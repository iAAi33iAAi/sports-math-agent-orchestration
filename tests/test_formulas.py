import pytest

from src.formulas import dynamic_weight, efficiency_score, expected_value, load_index, weight_update


def test_efficiency():
    assert efficiency_score(100, 50) == 2.0
    with pytest.raises(ValueError):
        efficiency_score(1, 0)


def test_expected_value():
    assert expected_value([0.5, 0.5], [100, 50]) == pytest.approx(75.0)


def test_load_index():
    assert load_index([0.3, 0.7], [0.8, 0.4]) == pytest.approx(0.52)


def test_dynamic_weight():
    w = dynamic_weight(0.9, 100, 0.1, 0.5)
    assert isinstance(w, float)
    assert w > 0


def test_weight_update():
    w = weight_update(2.0, [2.0, 1.0, 0.5], 0.6, 0.8)
    assert isinstance(w, float)
