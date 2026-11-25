# Kubernetes removed API rehearsal

Run with Python 3, Docker and kind from the repository root. The runner uses
the kubectl bundled in each digest-pinned kind node image.

```bash
python examples/kubernetes/minor-upgrade-rehearsal/run.py
```

What it does: starts one disposable cluster per version, with separate
temporary kubeconfig from your normal setup. On Kubernetes 1.31, the legacy
and current client URLs return the same FlowSchema. On 1.32, the legacy URL
fails with NotFound and the current URL succeeds. The runner checks that it
removed each cluster before moving on.

A FlowSchema is a rule the API server uses to classify requests. This
exercise reads a built-in FlowSchema and writes no application resources.
The two clusters model the source and target versions of a compatibility
test. An in-place control plane upgrade and state migration need their own
rehearsal.

- [Plan a Kubernetes minor upgrade](../../../knowledge/kubernetes/plan-a-minor-upgrade.md)
- [Kubernetes examples](../README.md)
