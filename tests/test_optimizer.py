from src.optimizer import dp_knapsack, greedy_knapsack


AGENTS = [
    {"name": "Alice", "value": 45, "cost": 8000},
    {"name": "Bob", "value": 38, "cost": 7200},
    {"name": "Carol", "value": 52, "cost": 9000},
    {"name": "Dave", "value": 29, "cost": 6500},
    {"name": "Eve", "value": 41, "cost": 7800},
    {"name": "Frank", "value": 35, "cost": 6800},
]


def test_greedy_within_budget():
    selected, val, cost = greedy_knapsack(AGENTS, 22000)
    assert cost <= 22000
    assert val > 0
    assert selected


def test_dp_exact_and_at_least_greedy():
    selected, val, cost = dp_knapsack(AGENTS, 22000)
    _, greedy_val, _ = greedy_knapsack(AGENTS, 22000)
    assert cost <= 22000
    assert val >= greedy_val


def test_empty_budget():
    selected, val, cost = greedy_knapsack(AGENTS, 0)
    assert selected == []
    assert val == 0.0
    assert cost == 0.0


def test_exact_fit():
    agents = [{"name": "A", "value": 10, "cost": 5}, {"name": "B", "value": 9, "cost": 4}]
    selected, val, cost = dp_knapsack(agents, 9)
    assert {a["name"] for a in selected} == {"A", "B"}
    assert val == 19.0
    assert cost == 9.0
