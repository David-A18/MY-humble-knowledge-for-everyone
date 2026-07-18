# Crossplane production, GitOps, and operations

## Purpose

Use this page to run Crossplane as a critical control plane with GitOps, package promotion, observability, backup, upgrade, and operational workflow practices.

If Crossplane can create, change, or delete production infrastructure, treat the management cluster as privileged infrastructure.

## Production architecture

| Component | Production responsibility |
| --- | --- |
| Management cluster | Hosts Crossplane, providers, functions, GitOps, policy, observability, and platform APIs. |
| Provider controllers | Reconcile external infrastructure through scoped credentials. |
| GitOps controller | Applies Crossplane packages, provider configs, XRDs, compositions, and resource requests from Git. |
| Policy layer | Enforces allowed API shapes, packages, namespaces, and destructive behaviors. |
| Cloud guardrails | Limit blast radius with IAM, SCPs, Config, CloudTrail, and deletion protection. |
| Observability stack | Tracks health, readiness, reconcile failures, package state, and cloud API errors. |

Avoid running ordinary application workloads on the same cluster that owns broad production infrastructure unless that is a deliberate design.

## GitOps responsibility split

Crossplane and GitOps controllers reconcile different systems:

```text
GitOps controller:
  Git repository -> Kubernetes desired objects

Crossplane:
  Kubernetes desired objects -> external resources
```

Together:

```text
Git repository
      |
Argo CD or Flux
      |
Kubernetes API
      |
Crossplane providers and functions
      |
External infrastructure
```

## Suggested repository layers

```text
clusters/
  management/
    crossplane-core/
    providers/
    functions/
    provider-configs/
    platform-apis/
    platform-compositions/

infrastructure/
  development/
  staging/
  production/
```

Keep Crossplane core installation, providers, functions, provider authentication, XRDs, compositions, and user-facing resources in separate layers so dependency order is clear.

## Apply order

1. Crossplane core.
2. Providers and functions.
3. Provider configs and runtime configuration.
4. XRDs.
5. Compositions.
6. XRs or direct managed resources.

GitOps health checks should wait for:

- Provider `HEALTHY=True`.
- Function `HEALTHY=True`.
- XRD `ESTABLISHED=True`.
- Critical XR and managed-resource `Ready=True`.

## Argo CD and Flux considerations

Crossplane creates generated resources such as provider revisions, provider config usages, composed resources, and status updates. Configure tracking, diff behavior, exclusions, and health checks so GitOps does not fight Crossplane-owned runtime objects.

> [!IMPORTANT]
> Do not configure GitOps pruning so broadly that it deletes dynamically generated composed resources or Crossplane runtime objects unintentionally.

## Package versioning and promotion

Pin:

- Crossplane Helm chart version.
- Provider package versions.
- Function package versions.
- Configuration package versions.
- Kubernetes version compatibility.
- Provider schemas used by examples and CI.

Promotion should move packages through development, staging, and production control planes. Test provider upgrades for schema changes, deprecations, defaults, permissions, controller behavior, and underlying provider runtime changes.

## Limit installed APIs

Large providers can install many APIs and increase API discovery load, memory use, and accidental exposure.

Use:

- Service-specific providers when practical.
- Managed Resource Activation Policies where supported.
- Admission policy to block unapproved resource groups or packages.
- Namespace and RBAC boundaries for tenant access.

## Observability

Enable metrics according to the installed Helm chart version:

```yaml
metrics:
  enabled: true
```

What it does: exposes Crossplane metrics for Prometheus-style scraping when supported by the chart configuration.

Monitor:

- Provider and function package health.
- Sustained `Synced=False` or `Ready=False`.
- Reconciliation error rate.
- Function request latency and errors.
- Provider workqueue depth.
- Cloud API throttling.
- Package pull and revision failures.
- Stuck deletions and finalizer age.
- Management cluster CPU, memory, and API-server pressure.

## Alert examples

| Signal | Why it matters |
| --- | --- |
| Provider unhealthy for more than a few minutes. | External infrastructure changes may be stalled. |
| Critical XR `Ready=False`. | Platform API users are affected. |
| Managed resource stuck deleting. | External resources may remain attached or billable. |
| Reconcile error rate spike. | Auth, quota, schema, or API availability may have changed. |
| Package revision inactive or unhealthy. | Upgrade or dependency resolution failed. |
| AWS throttling messages in provider logs. | Provider concurrency or polling may be too aggressive. |

## Backup and recovery

Back up:

- XRDs.
- Compositions and composition revisions.
- Provider, Function, and Configuration objects.
- ProviderConfigs, excluding or securely handling secrets.
- Managed resources and XRs.
- Connection Secrets.
- Namespace, RBAC, and admission policy objects.
- Git repositories and package version metadata.
- Management cluster state through supported cluster backup tooling.

Recovery plans must preserve or reconstruct `crossplane.io/external-name` mappings. Without them, Crossplane may not know which external resource belongs to which Kubernetes object.

## Deletion protection

For critical resources:

- Use management policies deliberately.
- Use cloud-native deletion protection where available.
- Add admission controls for destructive changes.
- Require pull-request review for production deletions.
- Keep provider delete permissions narrow.
- Document break-glass finalizer handling.

## Operations

Crossplane v2 Operations are alpha and intended for tasks that do not fit permanent reconciliation, such as backup workflows, maintenance, validation, scheduled tasks, and reactive tasks.

Use Operations when:

- The task is naturally run-to-completion.
- A function pipeline can express the workflow.
- The workflow should live near the Crossplane control plane.

Use another workflow engine when:

- Human approvals, branching, retries, or long-running orchestration dominate.
- Existing CI/CD or automation already handles the job more simply.
- The task should not have Crossplane control-plane privileges.

## Production readiness checklist

- [ ] Crossplane, providers, functions, and configurations are pinned.
- [ ] Provider credentials are least-privilege and separated by capability.
- [ ] Namespaced APIs and RBAC define tenant boundaries.
- [ ] XRDs validate allowed values and prevent invalid regions, tiers, and sizes.
- [ ] GitOps apply order and health checks are defined.
- [ ] CI renders compositions and runs server-side dry runs.
- [ ] Metrics, alerts, logs, and cloud audit trails are connected.
- [ ] Backups include external-name mappings and recovery procedures.
- [ ] Destructive actions have review, deletion protection, and rollback notes.
- [ ] Terraform and Crossplane ownership boundaries are documented.

## Related links

- [Crossplane](README.md)
- [Crossplane compositions](compositions.md)
- [Providers and authentication](providers-and-authentication.md)
- [Crossplane troubleshooting](troubleshooting.md)
- [Crossplane with Argo CD](https://docs.crossplane.io/latest/guides/crossplane-with-argo-cd/)
- [Crossplane metrics](https://docs.crossplane.io/latest/guides/metrics/)
- [Crossplane operations](https://docs.crossplane.io/latest/operations/operation/)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
