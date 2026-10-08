"""Core sports mathematics formulas."""
from typing import Dict, List

import numpy as np


def efficiency_score(value: float, cost: float) -> float:
    """Eff_a = Value_a / Cost_a."""
    if cost == 0:
        raise ValueError("Cost must be non-zero.")
    return value / cost


def expected_value(probabilities: List[float], outcomes: List[float]) -> float:
    """EV = sum(P_j * V_j)."""
    if len(probabilities) != len(outcomes):
        raise ValueError("probabilities and outcomes must have equal length.")
    return float(np.dot(probabilities, outcomes))


def load_index(task_weights: List[float], load_values: List[float]) -> float:
    """Load = sum(w_t * l_t)."""
    if len(task_weights) != len(load_values):
        raise ValueError("task_weights and load_values must have equal length.")
    return float(np.dot(task_weights, load_values))


def dynamic_weight(
    efficiency: float,
    ev: float,
    risk: float,
    load: float,
    alpha: float = 1.0,
    beta: float = 0.5,
    gamma: float = 0.3,
    delta: float = 0.2,
) -> float:
    """w = alpha*Eff + beta*EV - gamma*Risk - delta*Load."""
    return alpha * efficiency + beta * ev - gamma * risk - delta * load


def weight_update(current_weight, all_weights, load_avg, load_agent, eta=0.1) -> float:
    """w(t+1) = w(t) + eta*(w/Sum_w)*(L_avg - L)."""
    total = sum(all_weights)
    if total == 0:
        raise ValueError("Sum of weights must be non-zero.")
    return current_weight + eta * (current_weight / total) * (load_avg - load_agent)


def compute_dynamic_weight(agent: Dict, **kwargs) -> float:
    return dynamic_weight(
        agent["efficiency"],
        agent["ev"],
        agent["risk"],
        agent["load"],
        **kwargs,
    )
