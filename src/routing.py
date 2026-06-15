"""
routing.py  Agent routing: probabilistic, top-k, threshold.
"""
import numpy as np
from typing import List, Dict
from .normalization import softmax

def probabilistic_route(agents: List[Dict], weights: List[float]) -> Dict:
      """Sample one agent proportional to softmax weight."""
      probs = softmax(weights)
      idx = np.random.choice(len(agents), p=probs)
      return {**agents[idx], "_prob": float(probs[idx]), "_mode": "probabilistic"}

def top_k_route(agents: List[Dict], weights: List[float], k: int = 1) -> List[Dict]:
      """Select top-K agents by weight deterministically."""
      probs  = softmax(weights)
      ranked = np.argsort(weights)[::-1][:k]
      return [{**agents[i], "_prob": float(probs[i]), "_mode": "top-k"} for i in ranked]

def threshold_route(agents: List[Dict], weights: List[float], threshold: float = 0.2) -> List[Dict]:
      """Assign to all agents whose softmax probability exceeds threshold."""
      probs = softmax(weights)
      return [
          {**agents[i], "_prob": float(probs[i]), "_mode": "threshold"}
          for i in range(len(agents)) if probs[i] >= threshold
      ]
