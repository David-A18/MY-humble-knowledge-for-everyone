# Manifest-validation fixtures and runners

Run the documented commands from the repository root unless a chapter explicitly selects the series directory. JSON manifests are valid YAML. All inputs are synthetic.

| File | Purpose |
| --- | --- |
| [Version manifest](lab-versions.json) | Fixed tool releases, official release SHA256 values, node digest and immutable schema revision. |
| [Linux installer](install-tools.py) | Downloads checksum-pinned Linux amd64 tools into an explicitly empty directory. |
| [Source-tool runner](validate-offline.py) | Eight real Git/dyff/kubeconform/Conftest assertions, no cluster calls. |
| [Cluster runner](validate-cluster.py) | Private kind cluster, Kustomize, live diff, wrong-port HTTP failure/recovery, Chainsaw and cleanup. |
| [Fixture contract](test-fixtures.py) | Declared labels/ports only; does not prove a process listens. |
| [Deployment](app.yaml) | One pinned NGINX workload listening on port 80. |
| [Working Service](service.json) | Correct selector and target port. |
| [Reordered Service](service-reordered.json) | Equal parsed object, different text. |
| [Broken Service](service-broken.json) | Schema-valid target port 81, intentionally wrong for the application. |
| [Kustomization](kustomization.yaml) | Renders the working Deployment and Service. |
| [Chainsaw test](chainsaw-test.yaml) | Declarative apply/readiness/actual Service request; runner substitutes a broken Service in a temporary negative copy. |
| [Workflow reference](ci-workflow.yaml) | Reference copy; the [enabled workflow](../../../../../.github/workflows/manifest-validation-lab.yml) is authoritative. |
| [Policy example](policy/index.md) | Small ownership-label Rego rule. |

Follow the [lab](../regression-lab-and-ci.md) for prerequisites, expected results, execution evidence and cleanup. Do not run mutations in a shared cluster.

[Back to series](../index.md) | [Back to knowledge](../../../../index.md)
