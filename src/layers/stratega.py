"""STRATEGA planning and constraint layer."""
from typing import Callable, Dict, List

import numpy as np


class STRATEGAPlanner:
    def __init__(self) -> None:
        self.last_plan: Dict = {}

    def optimize(self, agents: List[Dict], weights: List[float], task_value: float) -> Dict:
        if len(agents) != len(weights):
            raise ValueError("agents and weights must have the same length.")
        if not agents:
            self.last_plan = {"task_value": task_value, "ranked_agents": [], "top_weight": 0.0}
            return self.last_plan

        ranked = np.argsort(weights)[::-1]
        self.last_plan = {
            "task_value": task_value,
            "ranked_agents": [agents[int(i)]["name"] for i in ranked],
            "top_weight": float(weights[int(ranked[0])]),
        }
        return self.last_plan

    def enforce_constraints(self, plan: Dict, hard: List[Callable], soft: List) -> Dict:
        """hard = bool callables; soft = (penalty_callable_or_value, penalty) tuples."""
        plan["soft_penalty"] = sum(lam * penalty for lam, penalty in soft)
        plan["feasible"] = all(constraint(plan) for constraint in hard)
        return plan
