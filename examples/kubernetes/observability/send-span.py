"""Send one synthetic span. Does not retry or claim durable delivery."""
import json
import sys
import time
import urllib.error
import urllib.request
import uuid

def payload():
    now = time.time_ns()
    return {"resourceSpans": [{"resource": {"attributes": [
        {"key": "service.name", "value": {"stringValue": "kb-lab"}}]},
        "scopeSpans": [{"scope": {"name": "kb-lab"}, "spans": [{
            "traceId": uuid.uuid4().hex, "spanId": uuid.uuid4().hex[:16],
            "name": "kb-lab-request", "kind": 2,
            "startTimeUnixNano": str(now), "endTimeUnixNano": str(now + 1000000),
            "status": {"code": 1}}]}]}]}

def send(endpoint="http://127.0.0.1:4318/v1/traces"):
    request = urllib.request.Request(endpoint, data=json.dumps(payload()).encode(),
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=10) as response:
        result = json.load(response)
        if result.get("partialSuccess", {}).get("rejectedSpans", 0) not in (0, "0"):
            raise RuntimeError("Receiver rejected spans: " + json.dumps(result))
        print("Receiver accepted synthetic span; verify downstream export separately.")

if __name__ == "__main__":
    try:
        send(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4318/v1/traces")
    except (urllib.error.URLError, TimeoutError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
