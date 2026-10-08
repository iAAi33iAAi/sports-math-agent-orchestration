"""Normalization strategies for agent weight routing."""
from typing import List

import numpy as np


def softmax(weights: List[float]) -> np.ndarray:
    """Stable softmax probabilities."""
    if not weights:
        return np.array([], dtype=float)
    w = np.asarray(weights, dtype=float)
    e = np.exp(w - np.max(w))
    return e / e.sum()


def temperature_softmax(weights: List[float], temperature: float = 1.0) -> np.ndarray:
    """Stable temperature-scaled softmax; temperature must be positive."""
    if temperature <= 0:
        raise ValueError("Temperature must be positive.")
    if not weights:
        return np.array([], dtype=float)
    w = np.asarray(weights, dtype=float) / temperature
    e = np.exp(w - np.max(w))
    return e / e.sum()


def min_max_normalize(weights: List[float]) -> np.ndarray:
    """Linear [0, 1] scaling."""
    if not weights:
        return np.array([], dtype=float)
    w = np.asarray(weights, dtype=float)
    lo, hi = w.min(), w.max()
    return np.ones_like(w) / len(w) if hi == lo else (w - lo) / (hi - lo)


def z_score_normalize(weights: List[float]) -> np.ndarray:
    """Zero-centred, unit-variance normalization."""
    if not weights:
        return np.array([], dtype=float)
    w = np.asarray(weights, dtype=float)
    mu, sigma = w.mean(), w.std()
    return np.zeros_like(w) if sigma == 0 else (w - mu) / sigma
