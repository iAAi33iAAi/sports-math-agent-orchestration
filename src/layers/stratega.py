"""
stratega.py  STRATEGA Planning Layer
Mission alignment, plan optimization, constraint enforcement.
"""
from typing import List, Dict, Callable
import numpy as np

class STRATEGAPlanner:
      def __init__(self):
                self.last_plan: Dict = {}

      def optimize(self, agents: List[Dict], weights: List[float], task_value: float) -> Dict:
                ranked = np.argsort(weights)[::-1]
                self.last_plan = {
                    "task_value": task_value,
                    "ranked_agents": [agents[i]["name"] for i in ranked],
                    "top_weight": weights[int(ranked[0])],
                }
                return self.last_plan

      def enforce_constraints(self, plan: Dict, hard: List[Callable], soft: List) -> Dict:
                """hard = list of bool callables; soft = list of (lambda, penalty) tuples."""
                plan["soft_penalty"] = sum(lam * p for lam, p in soft)
                plan["feasible"] = all(c(plan) for c in hard)
                return plan
