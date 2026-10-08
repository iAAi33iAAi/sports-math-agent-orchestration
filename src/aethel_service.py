"""AETHEL Interop v1 service for the deterministic sports/math engine.

Run:
    python -m src.aethel_service --host 127.0.0.1 --port 8101

This service is intentionally dry-run only. It returns mathematical results;
the AETHEL Colony remains responsible for safety and execution authorization.
"""
from __future__ import annotations
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .formulas import compute_dynamic_weight
from .optimizer import dp_knapsack, greedy_knapsack
from .orchestrator import AgentOrchestrator

PROTOCOL = "aethel-interop/1"
SERVICE = "sports-math"
VERSION = "0.2.0"


def _response(request_id: str, status: str, decision: str | None, reasons: list[str], result: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        "protocol": PROTOCOL,
        "service": SERVICE,
        "version": VERSION,
        "request_id": request_id,
        "status": status,
        "decision": decision,
        "reasons": reasons,
        "result": result,
        "evidence": evidence,
    }


def evaluate(request_id: str, operation: str, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        if operation == "optimize":
            agents = payload.get("agents", [])
            budget = payload.get("budget")
            method = payload.get("method", "exact")
            if not isinstance(agents, list) or budget is None:
                return _response(request_id, "FAIL", "INVALID_INPUT", ["agents and budget are required"], {}, {})
            if method == "greedy":
                selected, value, cost = greedy_knapsack(agents, float(budget))
            elif method == "exact":
                selected, value, cost = dp_knapsack(agents, int(budget))
            else:
                return _response(request_id, "FAIL", "INVALID_INPUT", [f"unknown optimization method: {method}"], {}, {})
            return _response(
                request_id, "PASS", "OPTIMIZED", [],
                {"selected": selected, "total_value": value, "total_cost": cost},
                {"method": method, "budget": budget},
            )

        if operation == "route":
            agents = payload.get("agents", [])
            mode = payload.get("routing_mode", "top-k")
            task_value = float(payload.get("task_value", 1.0))
            if not agents:
                return _response(request_id, "FAIL", "INVALID_INPUT", ["agents must not be empty"], {}, {})
            planner = AgentOrchestrator(
                agents=agents,
                budget=float(payload.get("budget", 100000.0)),
                routing_mode=mode,
                top_k=int(payload.get("top_k", 1)),
                threshold=float(payload.get("threshold", 0.2)),
            )
            result = planner.assign_task(task_value)
            return _response(
                request_id, "PASS", "ROUTED", [],
                {"selection": result, "weights": planner._weights()},
                {"routing_mode": mode},
            )

        if operation == "score":
            agent = payload.get("agent", {})
            weight = compute_dynamic_weight(
                agent,
                alpha=float(payload.get("alpha", 1.0)),
                beta=float(payload.get("beta", 0.5)),
                gamma=float(payload.get("gamma", 0.3)),
                delta=float(payload.get("delta", 0.2)),
            )
            return _response(request_id, "PASS", "SCORED", [], {"weight": weight}, {})

        return _response(request_id, "FAIL", "INVALID_OPERATION", [f"unsupported operation: {operation}"], {}, {})
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        return _response(request_id, "FAIL", "INVALID_INPUT", [str(exc)], {}, {})


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: dict[str, Any]) -> None:
        encoded = json.dumps(body, sort_keys=True).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:
        if self.path == "/aethel/health":
            self._send(200, _response("health", "PASS", "HEALTHY", [], {}, {"service": SERVICE, "version": VERSION}))
            return
        if self.path == "/aethel/capabilities":
            self._send(200, {
                "protocol": PROTOCOL,
                "service": SERVICE,
                "version": VERSION,
                "operations": ["optimize", "route", "score"],
                "dry_run": True,
            })
            return
        self._send(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/aethel/evaluate":
            self._send(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            if body.get("protocol") != PROTOCOL:
                self._send(400, {"error": "unsupported protocol"})
                return
            self._send(200, evaluate(str(body["request_id"]), str(body["operation"]), dict(body.get("payload", {}))))
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            self._send(400, {"error": str(exc)})

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8101)
    args = parser.parse_args()
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
