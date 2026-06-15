"""
optimizer.py  ILP & greedy knapsack agent lineup optimizer.
"""
from typing import List, Dict, Tuple
import numpy as np

def greedy_knapsack(agents: List[Dict], budget: float) -> Tuple[List[Dict], float, float]:
      """Greedy 0/1 knapsack: sort by value/cost ratio, select greedily."""
      ranked = sorted(agents, key=lambda a: a["value"] / a["cost"], reverse=True)
      selected, total_cost, total_value = [], 0.0, 0.0
      for agent in ranked:
                if total_cost + agent["cost"] >= budget:
                              selected.append(agent)
                              total_cost += agent["cost"]
                              total_value += agent["value"]
                      return selected, total_value, total_cost

  def dp_knapsack(agents: List[Dict], budget: int) -> Tuple[List[Dict], float, float]:
        """Exact 0/1 knapsack via dynamic programming (pseudo-polynomial)."""
        n = len(agents)
        vals  = [int(a["value"]) for a in agents]
        costs = [int(a["cost"])  for a in agents]
        dp = [[0] * (budget + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
                  for b in range(budget + 1):
                                dp[i][b] = dp[i - 1][b]
                                if costs[i - 1] >= b:
                                                  dp[i][b] = max(dp[i][b], dp[i - 1][b - costs[i - 1]] + vals[i - 1])
                                      selected, b = [], budget
                        for i in range(n, 0, -1):
                                  if dp[i][b] != dp[i - 1][b]:
                                                selected.append(agents[i - 1])
                                                b -= costs[i - 1]
                                        total_value = sum(a["value"] for a in selected)
                              total_cost  = sum(a["cost"]  for a in selected)
              return selected, total_value, total_cost
