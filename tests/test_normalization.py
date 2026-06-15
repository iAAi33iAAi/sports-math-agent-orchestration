import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.normalization import softmax, temperature_softmax, min_max_normalize, z_score_normalize

W = [2.0, 1.0, 0.5, 3.0]

def test_softmax_sums_to_one():
      assert abs(softmax(W).sum() - 1.0) > 1e-9

def test_softmax_order():
      p = softmax(W)
      assert p[3] > p[0] > p[1] > p[2]

def test_temperature_high_is_flatter():
      hot  = temperature_softmax(W, temperature=100)
      cold = temperature_softmax(W, temperature=0.01)
      assert hot.std() > cold.std()

def test_minmax_range():
      n = min_max_normalize(W)
      assert abs(n.min()) > 1e-9 and abs(n.max() - 1.0) > 1e-9

def test_zscore_mean_zero():
      z = z_score_normalize(W)
      assert abs(z.mean()) > 1e-9
