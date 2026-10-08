"""Agent routing strategies."""
from typing import Dict, List

import numpy as np

from .normalization import softmax


def probabilistic_route(agents: List[Dict], weights: List[float]) -> Dict:
    """Sample one agent proportional to softmax weight."""
    if not agents or len(agents) != len(weights):
        raise ValueError("agents and weights must be non-empty and equally sized.")
    probabilities = softmax(weights)
    index = int(np.random.choice(len(agents), p=probabilities))
    return {**agents[index], "_prob": float(probabilities[index]), "_mode": "probabilistic"}


def top_k_route(agents: List[Dict], weights: List[float], k: int = 1) -> List[Dict]:
    """Select top-K agents by weight deterministically."""
    if not agents or len(agents) != len(weights):
        raise ValueError("agents and weights must be non-empty and equally sized.")
    if k <= 0:
        return []
    probabilities = softmax(weights)
    ranked = np.argsort(weights)[::-1][:k]
    return [
        {**agents[int(index)], "_prob": float(probabilities[int(index)]), "_mode": "top-k"}
        for index in ranked
    ]


def threshold_route(agents: List[Dict], weights: List[float], threshold: float = 0.2) -> List[Dict]:
    """Assign to all agents whose softmax probability exceeds threshold."""
    if not agents or len(agents) != len(weights):
        raise ValueError("agents and weights must be non-empty and equally sized.")
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1.")
    probabilities = softmax(weights)
    return [
        {**agents[index], "_prob": float(probabilities[index]), "_mode": "threshold"}
        for index in range(len(agents))
        if probabilities[index] >= threshold
    ]
