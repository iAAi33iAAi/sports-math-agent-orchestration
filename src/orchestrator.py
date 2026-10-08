"""AgentOrchestrator: three-layer routing, optimization, and budget allocation."""
from typing import Dict, List, Literal

from .formulas import compute_dynamic_weight, weight_update
from .layers.manna import MANNABudgetLayer
from .layers.quibidt import QUIBIDTKernel
from .layers.stratega import STRATEGAPlanner
from .routing import probabilistic_route, threshold_route, top_k_route


class AgentOrchestrator:
    def __init__(
        self,
        agents: List[Dict],
        budget: float = 100_000.0,
        routing_mode: Literal["probabilistic", "top-k", "threshold"] = "probabilistic",
        alpha: float = 1.0,
        beta: float = 0.5,
        gamma: float = 0.3,
        delta: float = 0.2,
        eta: float = 0.1,
        top_k: int = 1,
        threshold: float = 0.2,
    ) -> None:
        self.agents = agents
        self.routing_mode = routing_mode
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.eta = eta
        self.top_k = top_k
        self.threshold = threshold
        self.quibidt = QUIBIDTKernel()
        self.stratega = STRATEGAPlanner()
        self.manna = MANNABudgetLayer(total_budget=budget)

    def _weights(self) -> List[float]:
        return [
            compute_dynamic_weight(
                agent,
                alpha=self.alpha,
                beta=self.beta,
                gamma=self.gamma,
                delta=self.delta,
            )
            for agent in self.agents
        ]

    def assign_task(self, task_value: float = 1.0):
        self.quibidt.enforce_invariants(self.agents)
        weights = self._weights()
        self.stratega.optimize(self.agents, weights, task_value)
        self.manna.allocate(task_value)

        if self.routing_mode == "probabilistic":
            return probabilistic_route(self.agents, weights)
        if self.routing_mode == "top-k":
            return top_k_route(self.agents, weights, k=self.top_k)
        if self.routing_mode == "threshold":
            return threshold_route(self.agents, weights, threshold=self.threshold)
        raise ValueError(f"Unsupported routing_mode: {self.routing_mode}")

    def update_loads(self, load_avg: float):
        weights = self._weights()
        for agent, weight in zip(self.agents, weights):
            agent["_updated_weight"] = weight_update(
                weight,
                weights,
                load_avg,
                agent["load"],
                eta=self.eta,
            )
        return self.agents
