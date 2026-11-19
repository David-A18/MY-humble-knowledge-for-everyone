# Istio security fixtures

- [Version pins](lab-versions.json) fix the Linux tool releases, checksums and kind node image.
- [Workloads](workloads.yaml) define the server and two client service accounts.
- [JWT fixture generator](jwt-lab.py) creates a synthetic token and matching policies for the disposable mesh.
- [Mesh runner](validate-mesh.py) performs baseline, STRICT mTLS, JWT and authorization checks in sequence and verifies cleanup.

- [Recorded CI results](runtime-evidence.json) show the observed versions, request outcomes and cleanup on the tested revision.

[Back to the lab](../../../../knowledge/kubernetes/applications-and-tools/istio/security-lab.md) | [Back to Istio](../../../../knowledge/kubernetes/applications-and-tools/istio/index.md)
