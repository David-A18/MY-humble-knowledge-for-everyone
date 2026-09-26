"""Deterministic example attester for the OKF v0.2 sample bundle."""

REQUIRED_KEYS = {"query", "datasource", "parameters", "started_at", "result_hash"}
EXPECTED_METRIC = "kube_pod_container_status_restarts_total"


def attest(receipt):
    """Return a deterministic verdict for a synthetic Prometheus receipt."""
    missing = sorted(REQUIRED_KEYS - set(receipt))
    if missing:
        return {"ok": False, "reason": f"missing keys: {', '.join(missing)}"}

    if not isinstance(receipt["parameters"], dict):
        return {"ok": False, "reason": "parameters must be an object"}

    if not str(receipt["result_hash"]).startswith("sha256:"):
        return {"ok": False, "reason": "result_hash must start with sha256:"}

    if EXPECTED_METRIC not in str(receipt["query"]):
        return {"ok": False, "reason": "query does not use the expected restart metric"}

    return {"ok": True, "reason": "receipt shape matches the sanctioned computation"}
