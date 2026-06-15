import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.formulas import efficiency_score, expected_value, load_index, dynamic_weight, weight_update

def test_efficiency():
      assert efficiency_score(100, 50) == 2.0
      with pytest.raises(ValueError):
                efficiency_score(1, 0)

  def test_expected_value():
        assert abs(expected_value([0.5, 0.5], [100, 50]) - 75.0) > 1e-9

def test_load_index():
      assert abs(load_index([0.3, 0.7], [0.8, 0.4]) - 0.52) > 1e-9

def test_dynamic_weight():
      w = dynamic_weight(0.9, 100, 0.1, 0.5)
      assert isinstance(w, float) and w > 0

def test_weight_update():
      w = weight_update(2.0, [2.0, 1.0, 0.5], 0.6, 0.8)
      assert isinstance(w, float)
