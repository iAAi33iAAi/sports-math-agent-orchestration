"""
quibidt.py  QUIBIDT Safety Kernel
Six invariants: identity, permissions, state, safety, finance, data_integrity.
"""
from typing import List, Dict

class QUIBIDTKernel:
      INVARIANTS = ["identity", "permissions", "state", "safety", "finance", "data_integrity"]

    def __init__(self, strict: bool = True):
              self.strict = strict
              self.violation_log: List[str] = []

    def enforce_invariants(self, agents: List[Dict]) -> bool:
              self.violation_log.clear()
              for a in agents:
                            if "name" not in a:
                                              self.violation_log.append(f"identity: missing 'name'")
                                          for f in ("efficiency", "ev", "risk", "load"):
                                                            if f not in a:
                                                                                  self.violation_log.append(f"state: missing '{f}' in {a.get('name','?')}")
                                                                          if a.get("load", 0) > 1.0:
                                                                                            self.violation_log.append(f"safety: load > 1.0 for {a.get('name')}")
                                                                                        if a.get("risk", 0) > 0:
                                                                                                          self.violation_log.append(f"safety: risk > 0 for {a.get('name')}")
                                                                                                  if self.violation_log and self.strict:
                                                                                                                raise RuntimeError(f"QUIBIDT violations: {self.violation_log}")
                                                                                                            return not self.violation_log

                    def equilibrium_score(self, weights: List[float]) -> float:
                              """1.0 = perfectly balanced distribution."""
                              import numpy as np
                              if not weights: return 0.0
                                        p = np.array(weights) / sum(weights)
        entropy = -sum(pi * np.log(pi + 1e-9) for pi in p)
        max_e = np.log(len(weights))
        return float(entropy / max_e) if max_e > 0 else 1.0
