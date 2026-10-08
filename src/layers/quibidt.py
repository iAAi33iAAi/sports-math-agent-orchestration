"""QUIBIDT Safety Kernel."""
from typing import Dict, List

import numpy as np


class QUIBIDTKernel:
    INVARIANTS = ["identity", "permissions", "state", "safety", "finance", "data_integrity"]

    def __init__(self, strict: bool = True) -> None:
        self.strict = strict
        self.violation_log: List[str] = []

    def enforce_invariants(self, agents: List[Dict]) -> bool:
        self.violation_log.clear()
        for agent in agents:
            if "name" not in agent:
                self.violation_log.append("identity: missing 'name'")
            for field in ("efficiency", "ev", "risk", "load"):
                if field not in agent:
                    self.violation_log.append(f"state: missing '{field}' in {agent.get('name', '?')}")
            if agent.get("load", 0) > 1.0:
                self.violation_log.append(f"safety: load > 1.0 for {agent.get('name')}")
            if agent.get("risk", 0) > 0:
                self.violation_log.append(f"safety: risk > 0 for {agent.get('name')}")

        if self.violation_log and self.strict:
            raise RuntimeError(f"QUIBIDT violations: {self.violation_log}")
        return not self.violation_log

    def equilibrium_score(self, weights: List[float]) -> float:
        """Return normalized Shannon entropy; 1.0 is perfectly balanced."""
        if not weights:
            return 0.0
        total = sum(weights)
        if total <= 0:
            raise ValueError("Weights must sum to a positive value.")
        probabilities = np.asarray(weights, dtype=float) / total
        entropy = -float(sum(p * np.log(p + 1e-12) for p in probabilities))
        max_entropy = float(np.log(len(weights)))
        return entropy / max_entropy if max_entropy > 0 else 1.0
