"""Agent lineup optimization using greedy and exact 0/1 knapsack methods."""
from typing import Dict, List, Tuple

Agent = Dict[str, float]


def _validate_agents(agents: List[Agent]) -> None:
    for agent in agents:
        if agent["cost"] < 0:
            raise ValueError("Agent cost must be non-negative.")
        if agent["value"] < 0:
            raise ValueError("Agent value must be non-negative.")
        if agent["cost"] == 0 and agent["value"] > 0:
            raise ValueError("Positive-value zero-cost agents are not supported.")


def greedy_knapsack(agents: List[Agent], budget: float) -> Tuple[List[Agent], float, float]:
    """Greedy 0/1 knapsack heuristic: select by value/cost while staying within budget."""
    if budget < 0:
        raise ValueError("Budget must be non-negative.")
    _validate_agents(agents)

    zero_cost = [a for a in agents if a["cost"] == 0]
    ranked = sorted(
        (a for a in agents if a["cost"] > 0),
        key=lambda a: a["value"] / a["cost"],
        reverse=True,
    )

    selected: List[Agent] = list(zero_cost)
    total_cost = float(sum(a["cost"] for a in selected))
    total_value = float(sum(a["value"] for a in selected))

    for agent in ranked:
        cost = float(agent["cost"])
        if total_cost + cost <= budget:
            selected.append(agent)
            total_cost += cost
            total_value += float(agent["value"])

    return selected, total_value, total_cost


def dp_knapsack(agents: List[Agent], budget: int) -> Tuple[List[Agent], float, float]:
    """Exact 0/1 knapsack via dynamic programming for integer costs."""
    if budget < 0:
        raise ValueError("Budget must be non-negative.")
    if not isinstance(budget, int):
        raise TypeError("Budget must be an integer for dp_knapsack.")
    _validate_agents(agents)

    n = len(agents)
    costs = [int(a["cost"]) for a in agents]
    vals = [float(a["value"]) for a in agents]

    for c in costs:
        if c != int(c):
            raise ValueError("Agent costs must be integers for dp_knapsack.")

    dp = [[0.0] * (budget + 1) for _ in range(n + 1)]
    keep = [[False] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = costs[i - 1]
        value = vals[i - 1]
        for capacity in range(budget + 1):
            dp[i][capacity] = dp[i - 1][capacity]
            if cost <= capacity:
                candidate = dp[i - 1][capacity - cost] + value
                if candidate > dp[i][capacity]:
                    dp[i][capacity] = candidate
                    keep[i][capacity] = True

    selected: List[Agent] = []
    capacity = budget
    for i in range(n, 0, -1):
        if keep[i][capacity]:
            selected.append(agents[i - 1])
            capacity -= costs[i - 1]

    selected.reverse()
    total_value = float(sum(a["value"] for a in selected))
    total_cost = float(sum(a["cost"] for a in selected))
    return selected, total_value, total_cost
