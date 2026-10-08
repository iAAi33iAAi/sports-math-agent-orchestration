from src.aethel_service import evaluate


def test_health_contract_fields():
    result = evaluate("r1", "score", {
        "agent": {"efficiency": 1.0, "ev": 0.5, "risk": 0.0, "load": 0.1}
    })
    assert result["protocol"] == "aethel-interop/1"
    assert result["service"] == "sports-math"
    assert result["status"] == "PASS"
    assert "weight" in result["result"]


def test_exact_optimizer_contract():
    result = evaluate(
        "r2", "optimize",
        {"agents": [{"name": "A", "value": 10, "cost": 5}], "budget": 5, "method": "exact"},
    )
    assert result["status"] == "PASS"
    assert result["result"]["total_cost"] == 5.0


def test_bad_operation_fails_closed():
    result = evaluate("r3", "unknown", {})
    assert result["status"] == "FAIL"
    assert result["decision"] == "INVALID_OPERATION"
