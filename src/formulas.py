"""formulas.py - Core sports mathematics formulas mapped to agent orchestration."""
import numpy as np
from typing import List, Dict

def efficiency_score(value: float, cost: float) -> float:
    """Eff_a = Value_a / Cost_a"""
    if cost == 0:
        raise ValueError("Cost must be non-zero.")
    return value / cost

def expected_value(probabilities: List[float], outcomes: List[float]) -> float:
    """EV_a = Sum P(a,j) * V(a,j)"""
    return float(np.dot(probabilities, outcomes))

def load_index(task_weights: List[float], load_values: List[float]) -> float:
    """Load_a = Sum w_t * l(a,t)"""
    return float(np.dot(task_weights, load_values))

def dynamic_weight(efficiency, ev, risk, load, alpha=1.0, beta=0.5, gamma=0.3, delta=0.2) -> float:
    """w_a = alpha*Eff + beta*EV - gamma*Risk - delta*Load"""
    return alpha * efficiency + beta * ev - gamma * risk - delta * load

def weight_update(current_weight, all_weights, load_avg, load_agent, eta=0.1) -> float:
    """w_a(t+1) = w_a(t) + eta*(w_a/Sum_w)*(L_avg - L_a)"""
    total = sum(all_weights)
    if total == 0:
        raise ValueError("Sum of weights must be non-zero.")
    return current_weight + eta * (current_weight / total) * (load_avg - load_agent)

def compute_dynamic_weight(agent: Dict, **kwargs) -> float:
    return dynamic_weight(agent["efficiency"], agent["ev"], agent["risk"], agent["load"], **kwargs)
