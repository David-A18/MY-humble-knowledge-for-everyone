# Manifest-validation fixtures

Run commands from the parent series directory. JSON manifests are also valid YAML.

- `app.yaml`: labeled Deployment listening on port 80.
- `service.json`: correct selector and target port.
- `service-reordered.json`: identical data in a different key order.
- `service-broken.json`: intentionally wrong target port.
- `chainsaw-test.yaml`: apply, readiness, and connectivity test.
- `ci-workflow.yaml`: educational offline/cluster CI sequence; copy and review before enabling.
- `test-fixtures.py`: offline structural regression checks (requires PyYAML).
- [Policy example](policy/index.md): ownership-label enforcement.

[Back to series](../index.md) | [Back to root](../../../../../README.md)
