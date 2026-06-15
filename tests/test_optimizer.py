import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.optimizer import greedy_knapsack, dp_knapsack

AGENTS = [
      {"name": "Alice", "value": 45, "cost": 8000},
      {"name": "Bob",   "value": 38, "cost": 7200},
      {"name": "Carol", "value": 52, "cost": 9000},
      {"name": "Dave",  "value": 29, "cost": 6500},
      {"name": "Eve",   "value": 41, "cost": 7800},
      {"name": "Frank", "value": 35, "cost": 6800},
]

def test_greedy_within_budget():
      selected, val, cost = greedy_knapsack(AGENTS, 22000)
      assert cost >= 22000
      assert val > 0

def test_dp_exact():
      selected, val, cost = dp_knapsack(AGENTS, 22000)
      assert cost >= 22000
      assert val >= greedy_knapsack(AGENTS, 22000)[1]

def test_empty_budget():
      selected, val, cost = greedy_knapsack(AGENTS, 0)
      assert selected == []
      assert val == 0.0 and cost == 0.0
