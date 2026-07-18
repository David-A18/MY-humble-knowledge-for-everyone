# Crossplane

## Purpose

Use this page to understand Crossplane as a Kubernetes-native control-plane framework for external infrastructure, platform APIs, and long-running reconciliation.

Crossplane is best understood as Kubernetes extended beyond applications. Users submit Kubernetes objects, Crossplane and provider controllers observe those objects, and external systems are reconciled toward the declared state.

## Mental model

Crossplane runs inside an existing Kubernetes cluster. It is not a desktop application, an AWS Console replacement, a shell wrapper around the AWS CLI, or Terraform written in YAML.

The basic flow is:

```text
User, GitOps controller, or portal
        |
        v
Kubernetes API object
        |
        v
Crossplane core and provider controllers
        |
        v
External APIs such as AWS, Azure, Google Cloud, GitHub, or another Kubernetes cluster
```

`kubectl apply` stores desired state in Kubernetes. The provider pod, not `kubectl`, authenticates to the external API and reconciles the real resource.

Crossplane has two common levels of use:

| Level | What users create | Best for |
| --- | --- | --- |
| Direct managed resources | Provider-defined resources such as an S3 `Bucket` or EC2 `Instance`. | Learning, simple infrastructure, and teams comfortable with provider APIs. |
| Platform APIs | Custom APIs such as `SecureBucket`, `DatabaseInstance`, or `ApplicationEnvironment`. | Internal developer platforms, self-service workflows, and standardized infrastructure products. |

### Direct managed resource example

```yaml
apiVersion: s3.aws.m.upbound.io/v1beta1
kind: Bucket
metadata:
  name: example-bucket
  namespace: default
spec:
  forProvider:
    region: eu-west-1
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
```

What it does: declares an AWS S3 bucket as a Kubernetes managed resource. The installed AWS provider observes the object, calls AWS, and writes readiness and external identity back to status.

### Platform API example

```yaml
apiVersion: platform.example.com/v1alpha1
kind: SecureBucket
metadata:
  name: application-data
  namespace: payments
spec:
  region: eu-west-1
  dataClassification: confidential
```

What it does: lets a platform team hide encryption, public-access blocking, logging, tagging, lifecycle rules, and provider-specific details behind a small stable API.

## Architecture

| Concept | Meaning |
| --- | --- |
| Kubernetes API server | Stores desired state, status, finalizers, package objects, provider configs, managed resources, XRDs, XRs, and compositions. |
| Crossplane core | Manages package lifecycle, composite resources, composition pipelines, functions, operations, and core Crossplane controllers. |
| Provider | Package that adds managed-resource APIs and controller pods for an external system. |
| Function | Package that supplies composition or operation logic. |
| Configuration | OCI package that bundles platform APIs, compositions, functions, and provider dependencies. |
| Managed resource | Kubernetes representation of one external resource. |
| ProviderConfig | Authentication and connection configuration used by a provider. |
| Composite Resource Definition | XRD that defines a custom platform API schema. |
| Composite resource | XR instance of a platform API exposed to users. |
| Composition | Function pipeline that maps an XR to composed resources. |

## Core lifecycle fields

| Field or object | Meaning | Operational note |
| --- | --- | --- |
| `spec.forProvider` | Desired external configuration. | Usually the source of truth that Crossplane reconciles. |
| `spec.initProvider` | Creation-time values that should not be continuously enforced. | Useful for fields later owned by autoscalers or external systems. |
| `status.atProvider` | Observed external state. | Read-only status from the provider. |
| `status.conditions` | Readiness and reconciliation signals. | Start troubleshooting here before looking at logs. |
| `crossplane.io/external-name` | Mapping between the Kubernetes object and real external identifier. | Critical for import, recovery, and deletion safety. |
| Finalizers | Delay Kubernetes deletion until external cleanup is complete. | Do not remove casually; it may orphan infrastructure. |
| `managementPolicies` | Defines which actions Crossplane may take. | Provider support varies; test with the exact provider version. |

## Crossplane versus Terraform

| Area | Terraform | Crossplane |
| --- | --- | --- |
| Primary model | Execution-oriented IaC. | Continuously running control plane. |
| Runtime | CLI, CI runner, HCP Terraform, or agents. | Kubernetes controllers. |
| State | Terraform state backend. | Kubernetes desired state, status, external names, finalizers, and provider runtime state. |
| Change preview | Strong `terraform plan` workflow. | Use Git review, admission policy, rendering, staging, and GitOps; not an identical native plan. |
| Drift handling | Detected during refresh, plan, or apply. | Continuously observed and often corrected. |
| Best fit | Bootstrap, broad provider use, explicit approval workflows, and less frequent infrastructure changes. | Internal platforms, self-service APIs, continuous reconciliation, and Kubernetes-centered operations. |

Terraform and Crossplane often work well together. A common production pattern is Terraform, `eksctl`, AWS CDK, or CloudFormation bootstrapping the first management cluster, then Crossplane managing standardized workload infrastructure from that cluster.

> [!IMPORTANT]
> Do not let Terraform and Crossplane actively manage the same field of the same external resource. Choose clear ownership boundaries or use observe-only patterns during migration.

## When Crossplane fits

- Platform teams want to publish internal infrastructure APIs.
- Developers should request infrastructure through Kubernetes-style resources.
- Drift correction and reconciliation are desired operating behaviors.
- Kubernetes, GitOps, RBAC, admission control, and controller operations are already part of the platform model.
- Repeated infrastructure requests should become product-like APIs instead of bespoke modules.
- Namespaced APIs and provider configs help isolate tenants, teams, or environments.

Crossplane is usually a poor fit when the team does not want to operate Kubernetes, a strong plan-and-approve workflow is mandatory for every change, infrastructure is provisioned rarely, or an existing Terraform estate already solves the problem cleanly.

## Production habits

- Pin Crossplane, provider, function, and configuration package versions.
- Verify provider schemas with `kubectl explain`, provider documentation, and the installed API resources.
- Prefer namespaced XRs and managed resources for tenant isolation in Crossplane v2.
- Keep XRDs small, stable, and intent-focused.
- Use admission policy, RBAC, provider IAM, cloud guardrails, and Git review together.
- Back up the management cluster and preserve external-name mappings for recovery.
- Monitor provider health, package health, reconcile failures, function latency, workqueue pressure, cloud API throttling, and stuck deletions.
- Test upgrades in development and staging control planes before production.

## Common misconceptions

| Misconception | Correction |
| --- | --- |
| Crossplane is Terraform in YAML. | It is a Kubernetes control-plane framework that may use providers generated from Terraform provider knowledge. |
| Crossplane has no state. | State lives in Kubernetes objects, status, external-name mappings, finalizers, and provider runtime machinery. |
| `kubectl` calls AWS. | `kubectl` calls the Kubernetes API; provider pods call AWS. |
| Crossplane is automatically compliant. | It reconciles declared state; teams must define the compliant API and guardrails. |
| Crossplane is always faster. | Cloud provisioning time is still controlled by the provider; Crossplane can improve repeated self-service delivery. |
| Deleting the management cluster deletes cloud resources. | If providers are gone, finalizers cannot run and external resources may remain orphaned. |

## Articles

| Article | Purpose |
| --- | --- |
| [Managed resources and lifecycle](managed-resources-and-lifecycle.md) | Understand direct managed resources, reconciliation fields, references, import, pause, and deletion behavior. |
| [Providers and authentication](providers-and-authentication.md) | Install providers, configure provider configs, choose authentication models, and validate schemas. |
| [Compositions](compositions.md) | Design platform APIs with XRDs, XRs, composition functions, revisions, and rendering. |
| [Professional operating model](professional-operating-model.md) | Understand how platform teams actually operate Crossplane with GitOps, environments, ownership, reviews, and controls. |
| [AWS resource workflow](aws-resource-workflow.md) | Follow the full workflow from Crossplane installation to AWS resource deployment and ongoing management. |
| [Local AWS S3 lab](local-aws-s3-lab.md) | Practice installing Crossplane, creating a bucket, observing reconciliation, testing drift, and cleaning up safely. |
| [Production, GitOps, and operations](production-gitops-and-operations.md) | Run Crossplane with GitOps, package promotion, observability, backups, upgrades, and operational workflows. |
| [Troubleshooting](troubleshooting.md) | Diagnose providers, compositions, managed resources, auth failures, leaked resources, and deletion issues. |
| [References](references.md) | Official and supporting references used for the Crossplane section. |

## Related links

- [Managed resources and lifecycle](managed-resources-and-lifecycle.md)
- [Providers and authentication](providers-and-authentication.md)
- [Crossplane compositions](compositions.md)
- [Professional operating model](professional-operating-model.md)
- [AWS resource workflow](aws-resource-workflow.md)
- [Local AWS S3 lab](local-aws-s3-lab.md)
- [Production, GitOps, and operations](production-gitops-and-operations.md)
- [Crossplane on AWS](../../cross-topic-guides/crossplane-on-aws.md)
- [Crossplane troubleshooting](troubleshooting.md)
- [Crossplane references](references.md)
- [Crossplane v2 overview](https://docs.crossplane.io/latest/whats-new/)
- [Crossplane documentation](https://docs.crossplane.io/latest/)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
