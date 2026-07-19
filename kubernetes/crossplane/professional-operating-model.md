# Crossplane professional operating model

## Purpose

Use this page to understand how professional platform teams actually work with Crossplane: what they give developers, what they keep private, how they review changes, and how Crossplane fits with GitOps, Terraform, AWS identity, policy, and observability.

Professional Crossplane use is rarely about letting every developer write raw cloud resources. The durable pattern is a platform team running Crossplane as a management control plane and exposing small internal APIs that represent approved infrastructure products.

## The professional split

| Concern | Platform team owns | Application team sees |
| --- | --- | --- |
| Bootstrap | Management cluster, Crossplane core, GitOps, policy, observability. | Usually hidden. |
| Provider installation | Provider package versions, runtime configs, activation policies. | Usually hidden. |
| Credentials | IAM roles, ProviderConfigs, account mapping, secret flow. | A safe namespace or platform API. |
| Cloud implementation | Managed resources, references, tagging, networking, encryption, deletion rules. | A small XR such as `SecureBucket` or `ApplicationEnvironment`. |
| Reviews | Composition changes, provider upgrades, IAM changes, destructive behavior. | Pull requests for resource requests. |
| Operations | Metrics, alerts, backups, incident response, upgrades, recovery. | Status, events, and platform support paths. |

## How the system really works

Crossplane extends the Kubernetes API. Providers add Kubernetes API endpoints for external systems and run controller pods that reconcile those objects. A managed resource is the Kubernetes-side object; the cloud service, such as an S3 bucket, is the external resource.

```text
Developer or GitOps commit
        |
        v
Kubernetes API object
        |
        v
Crossplane core selects composition or provider watches managed resource
        |
        v
Provider pod authenticates through ProviderConfig
        |
        v
AWS API create, read, update, delete, tag, or observe call
        |
        v
status.conditions, status.atProvider, external-name, events
```

The key operational detail is that `kubectl apply` does not call AWS. It changes Kubernetes desired state. The provider controller later calls AWS and writes status.

## Professional patterns

| Pattern | Why professionals use it |
| --- | --- |
| Management cluster | Keeps the infrastructure control plane separate from ordinary workloads. |
| GitOps first | Makes Git the review and audit point before Kubernetes desired state changes. |
| Platform APIs over raw resources | Hides provider complexity and prevents teams from bypassing standards. |
| Namespaced XRs and managed resources | Uses Kubernetes namespace and RBAC boundaries for tenant isolation. |
| Explicit ProviderConfigs | Prevents accidental use of the wrong credentials or account. |
| Provider package pinning | Avoids surprise schema, controller, or Terraform-provider behavior changes. |
| Managed Resource Activation Policies | Reduces API surface and cluster overhead for large providers. |
| Composition rendering in CI | Gives reviewers a view of generated resources before reconciliation. |
| Sandbox integration tests | Finds IAM, quota, eventual-consistency, and provider-schema issues before production. |
| Cloud guardrails outside Crossplane | IAM, SCPs, AWS Config, CloudTrail, and budgets catch mistakes Crossplane cannot know about. |

## Repository workflow

Professional teams usually separate platform implementation from user requests.

```text
platform/
  crossplane/
    core/
    providers/
    functions/
    provider-configs/
    xrd/
    compositions/
    policy/

environments/
  dev/
    requests/
  staging/
    requests/
  prod/
    requests/
```

Platform PRs change packages, credentials, XRDs, compositions, functions, and policy. Application PRs create or update small XRs.

## Change flow

1. Platform engineer changes an XRD, Composition, Function, provider version, or IAM role in Git.
2. CI runs YAML validation, policy checks, `kubectl apply --dry-run=server`, and `crossplane composition render`.
3. A sandbox control plane reconciles the change against a non-production AWS account.
4. Reviewers inspect generated resources, permissions, deletion behavior, and migration notes.
5. GitOps promotes the change to staging, then production.
6. Crossplane reconciles the approved desired state.
7. Observability confirms provider health, `Ready=True`, `Synced=True`, and expected AWS audit events.

## Developer request flow

Developers should usually create a platform resource, not raw cloud resources.

```yaml
apiVersion: platform.example.com/v1alpha1
kind: SecureBucket
metadata:
  name: payments-artifacts
  namespace: payments
spec:
  region: eu-west-1
  lifecycle:
    expireAfterDays: 90
  dataClassification: internal
```

What it does: asks for an approved S3-backed storage product. The platform owns bucket names, tags, public-access blocking, encryption, logging, versioning, lifecycle policy, and AWS account placement.

## Platform implementation flow

The platform team defines the API contract with an XRD, then implements it with a Composition.

```yaml
apiVersion: apiextensions.crossplane.io/v2
kind: CompositeResourceDefinition
metadata:
  name: securebuckets.platform.example.com
spec:
  scope: Namespaced
  group: platform.example.com
  names:
    kind: SecureBucket
    plural: securebuckets
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                region:
                  type: string
                  enum:
                    - eu-west-1
                    - eu-central-1
                dataClassification:
                  type: string
                  enum:
                    - internal
                    - confidential
                lifecycle:
                  type: object
                  properties:
                    expireAfterDays:
                      type: integer
                      minimum: 30
                      maximum: 365
              required:
                - region
                - dataClassification
```

What it does: defines a small namespaced platform API and prevents unsupported regions or classifications at the Kubernetes API layer.

## Review checklist for real teams

- [ ] Does the XRD expose intent instead of cloud-provider internals?
- [ ] Are destructive fields omitted, locked down, or separately approved?
- [ ] Does the Composition generate required tags, encryption, public-access blocks, logging, and deletion behavior?
- [ ] Does CI render the Composition and show generated resources?
- [ ] Are provider package versions pinned?
- [ ] Are provider roles least-privilege and account-scoped?
- [ ] Are ProviderConfigs selected by platform logic rather than arbitrary user input?
- [ ] Are AWS SCPs, Config, CloudTrail, budgets, and IAM guardrails in place?
- [ ] Does the recovery plan preserve external-name mappings?
- [ ] Are Terraform and Crossplane ownership boundaries documented?

## What professionals avoid

- Letting every team create arbitrary raw managed resources in production.
- Using `AdministratorAccess` for all provider pods.
- Letting Crossplane and Terraform update the same resource fields.
- Upgrading providers directly in production without rendering and sandbox reconciliation.
- Relying on Crossplane alone for compliance.
- Deleting the management cluster before external resources are cleanly deleted or intentionally orphaned.
- Removing finalizers without an external-resource recovery decision.

## Related links

- [Crossplane](README.md)
- [Deployment patterns and references](deployment-patterns-and-references.md)
- [AWS resource workflow](aws-resource-workflow.md)
- [Crossplane compositions](compositions.md)
- [Providers and authentication](providers-and-authentication.md)
- [Production, GitOps, and operations](production-gitops-and-operations.md)
- [Crossplane references](references.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
