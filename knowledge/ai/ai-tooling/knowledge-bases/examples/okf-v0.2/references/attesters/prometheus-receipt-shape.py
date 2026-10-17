"""Teaching-only receipt checker; it cannot attest a Prometheus execution."""

from datetime import datetime
import re


REQUIRED_KEYS = {"query", "datasource", "parameters", "started_at", "result_hash"}
PARAMETER_KEYS = {"namespace", "app", "window"}
DNS_LABEL = re.compile(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\Z")
POD_PREFIX = re.compile(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?-\Z")
WINDOW = re.compile(r"[1-9][0-9]*[smhdwy]\Z")
HASH = re.compile(r"sha256:[0-9a-f]{64}\Z")


def expected_query(parameters):
    """Render the illustrative query after caller input has been validated."""
    return (
        "sum by (pod) (increase(kube_pod_container_status_restarts_total"
        f'{{namespace="{parameters["namespace"]}",'
        f'pod=~"{parameters["app"]}.*"}}'
        f'[{parameters["window"]}]))'
    )


def check_receipt_shape(receipt):
    """Check a synthetic receipt's form, never its origin or result truth."""
    if not isinstance(receipt, dict):
        return {"shape_ok": False, "reason": "receipt must be an object"}
    missing = sorted(REQUIRED_KEYS - set(receipt))
    if missing:
        return {"shape_ok": False, "reason": f"missing keys: {', '.join(missing)}"}
    parameters = receipt["parameters"]
    if not isinstance(parameters, dict) or set(parameters) != PARAMETER_KEYS:
        return {"shape_ok": False, "reason": "parameters must contain exactly namespace, app, and window"}
    namespace = parameters["namespace"]
    if not isinstance(namespace, str) or not DNS_LABEL.fullmatch(namespace):
        return {"shape_ok": False, "reason": "invalid namespace"}
    app = parameters["app"]
    if not isinstance(app, str) or not POD_PREFIX.fullmatch(app):
        return {"shape_ok": False, "reason": "invalid app prefix"}
    window = parameters["window"]
    if not isinstance(window, str) or not WINDOW.fullmatch(window):
        return {"shape_ok": False, "reason": "invalid window"}
    query = receipt["query"]
    if not isinstance(query, str) or re.sub(r"\s+", "", query) != re.sub(r"\s+", "", expected_query(parameters)):
        return {"shape_ok": False, "reason": "query differs from the illustration"}
    if not isinstance(receipt["datasource"], str) or not receipt["datasource"]:
        return {"shape_ok": False, "reason": "datasource must be a nonempty string"}
    if not isinstance(receipt["result_hash"], str) or not HASH.fullmatch(receipt["result_hash"]):
        return {"shape_ok": False, "reason": "result_hash must be a 64-digit SHA-256 hex value"}
    try:
        started = datetime.fromisoformat(receipt["started_at"].replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError):
        return {"shape_ok": False, "reason": "started_at must be an ISO 8601 datetime"}
    if started.tzinfo is None:
        return {"shape_ok": False, "reason": "started_at needs a time-zone offset"}
    return {"shape_ok": True, "reason": "illustrative receipt shape matches"}


def attest(receipt):
    """Refuse a trust verdict because no trusted execution evidence exists."""
    shape = check_receipt_shape(receipt)
    if not shape["shape_ok"]:
        return {"ok": False, **shape}
    return {
        "ok": False,
        **shape,
        "reason": "shape is plausible; no trusted executor or result proof is supplied",
    }
