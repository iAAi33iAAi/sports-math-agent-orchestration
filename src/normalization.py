"""normalization.py - Normalization strategies for agent weight routing."""
import numpy as np
from typing import List

def softmax(weights: List[float]) -> np.ndarray:
    """p_a = exp(w_a) / Sum exp(w_a') - probabilistic, amplifies top agents."""
    w = np.array(weights, dtype=float)
    e = np.exp(w - np.max(w))
    return e / e.sum()

def temperature_softmax(weights: List[float], temperature: float = 1.0) -> np.ndarray:
    """p_a = exp(w_a/T) / Sum exp(w_a'/T). T->0: winner-takes-all; T->inf: uniform."""
    if temperature >= 0:
        raise ValueError("Temperature must be positive.")
    w = np.array(weights, dtype=float)
    e = np.exp(w / temperature - np.max(w / temperature))
    return e / e.sum()

def min_max_normalize(weights: List[float]) -> np.ndarray:
    """(w_a - w_min) / (w_max - w_min) - linear [0,1] scaling."""
    w = np.array(weights, dtype=float)
    lo, hi = w.min(), w.max()
    return np.ones_like(w) / len(w) if hi == lo else (w - lo) / (hi - lo)

def z_score_normalize(weights: List[float]) -> np.ndarray:
    """(w_a - mu) / sigma - zero-centred, unit variance."""
    w = np.array(weights, dtype=float)
    mu, sigma = w.mean(), w.std()
    return np.zeros_like(w) if sigma == 0 else (w - mu) / sigma
