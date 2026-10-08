import numpy as np
import pytest

from src.normalization import min_max_normalize, softmax, temperature_softmax, z_score_normalize


W = [2.0, 1.0, 0.5, 3.0]


def test_softmax_sums_to_one():
    assert softmax(W).sum() == pytest.approx(1.0)


def test_softmax_order():
    p = softmax(W)
    assert p[3] > p[0] > p[1] > p[2]


def test_temperature_high_is_flatter():
    hot = temperature_softmax(W, temperature=100)
    cold = temperature_softmax(W, temperature=0.01)
    assert hot.std() < cold.std()


def test_minmax_range():
    n = min_max_normalize(W)
    assert n.min() == pytest.approx(0.0)
    assert n.max() == pytest.approx(1.0)


def test_zscore_mean_zero():
    z = z_score_normalize(W)
    assert z.mean() == pytest.approx(0.0)
    assert np.std(z) == pytest.approx(1.0)
