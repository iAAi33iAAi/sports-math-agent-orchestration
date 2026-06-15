"""
orchestrator.py  AgentOrchestrator: full three-layer engine.
"""
from typing import List, Dict, Literal
from .formulas import compute_dynamic_weight, weight_update
from .routing import probabilistic_route, top_k_route, threshold_route
from .layers.quibidt import QUIBIDTKernel
from .layers.stratega import STRATEGAPlanner
from .layers.manna import MANNABudgetLayer

class AgentOrchestrator:
      def __init__(self, agents: List[Dict], budget: float = 100_000.0,
                                    routing_mode: Literal["probabilistic","top-k","threshold"] = "probabilistic",
                                    alpha=1.0, beta=0.5, gamma=0.3, delta=0.2, eta=0.1,
                                    top_k=1, threshold=0.2):
                                              self.agents = agents
                                              self.routing_mode = routing_mode
                                              self.alpha, self.beta, self.gamma, self.delta, self.eta = alpha, beta, gamma, delta, eta
                                              self.top_k, self.threshold = top_k, threshold
                                              self.quibidt  = QUIBIDTKernel()
                                              self.stratega = STRATEGAPlanner()
                                              self.manna    = MANNABudgetLayer(total_budget=budget)

      def _weights(self) -> List[float]:
                return [compute_dynamic_weight(a, alpha=self.alpha, beta=self.beta,
                                                                                      gamma=self.gamma, delta=self.delta) for a in self.agents]

      def assign_task(self, task_value: float = 1.0):
                self.quibidt.enforce_invariants(self.agents)
                weights = self._weights()
                self.stratega.optimize(self.agents, weights, task_value)
                self.manna.allocate(task_value)
                if self.routing_mode == "probabilistic":
                              return probabilistic_route(self.agents, weights)
elif self.routing_mode == "top-k":
            return top_k_route(self.agents, weights, k=self.top_k)
        return threshold_route(self.agents, weights, threshold=self.threshold)

    def update_loads(self, load_avg: float):
              weights = self._weights()
              for a in self.agents:
                            w = compute_dynamic_weight(a, alpha=self.alpha, beta=self.beta,
                                                                                              gamma=self.gamma, delta=self.delta)
                            a["_updated_weight"] = weight_update(w, weights, load_avg, a["load"], eta=self.eta)
                        return self.agents
