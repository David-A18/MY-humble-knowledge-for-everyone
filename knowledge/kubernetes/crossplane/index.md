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

For the focused decision guide, read [When to use Terraform or Crossplane](terraform-vs-crossplane.md).

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
| [How to request a Crossplane platform API](xrd-composition-and-xr-calls.md) | See what the platform team defines, what one XR asks for, and which checks establish delivery. |
| [How Crossplane's components turn a request into a resource](component-model.md) | Follow an invented bucket request from XRD and XR through Composition, managed resource, provider, and external API; then place advanced components around that path. |
| [How a Crossplane managed resource changes over time](managed-resources-and-lifecycle.md) | Follow desired state, provider observation, drift, import, pause, and deletion for one invented bucket. |
| [How a Crossplane provider reaches an external API](providers-and-authentication.md) | Separate provider package health, provider configuration, Pod credentials, and external authorization for one invented bucket. |
| [When to use a managed resource or a Crossplane platform API](providers-compositions-and-managed-resources.md) | Compare direct provider-specific requests with a small XR and Composition backed by the same provider. |
| [How a Crossplane Composition fulfills one application request](compositions.md) | Follow an invented WebApplication from XRD validation through function output, composed Deployment and Service, revision choice, and user-path check. |
| [How one platform request reaches a running application](application-delivery-platform-api.md) | Follow repository creation, image publication, Kubernetes rollout, and application checks as separate handoffs. |
| [Choose how Crossplane repeats and connects resources](deployment-patterns-and-references.md) | Choose explicit objects, fixed templates, or a function loop, then connect dependent resources by provider reference. |
| [When to use Terraform or Crossplane](terraform-vs-crossplane.md) | Use one invented network request to choose a reviewed plan/apply workflow, a continuously reconciled platform API, or both with clear ownership. |
| [How one Crossplane request becomes an AWS network](aws-vpc-platform-api.md) | Follow a `PlatformNetwork` XR through VPC, subnet, routing, optional endpoint, and deletion decisions. |
| [How a team operates a Crossplane platform API](professional-operating-model.md) | Follow an invented storage request through team ownership, change review, access boundaries, and outcome checks. |
| [How an AWS resource request moves through Crossplane](aws-resource-workflow.md) | Follow one invented bucket request from API acceptance through provider reconciliation, AWS state, application use, and deletion. |
| [Create and remove one S3 bucket with Crossplane](local-aws-s3-lab.md) | Practice one authorized sandbox request, confirm provider and AWS state, and verify deletion before removing the cluster. |
| [Record evidence from a Crossplane S3 sandbox lab](aws-s3-lab-validation-template.md) | Capture actual identity, version, condition, AWS, and cleanup evidence from an authorized lab run. |
| [How GitOps and Crossplane keep a platform request running](production-gitops-and-operations.md) | Follow an invented storage change through GitOps and Crossplane reconciliation, promotion, monitoring, and recovery. |
| [Find the first failing Crossplane handoff](troubleshooting.md) | Follow one stuck deletion, distinguish conditions, and locate the first failed controller boundary. |
| [Find the right Crossplane source for your question](references.md) | Choose an official source for API design, provider schemas, identity, or troubleshooting. |

## Related links

- [How to request a Crossplane platform API](xrd-composition-and-xr-calls.md)
- [How Crossplane's components turn a request into a resource](component-model.md)
- [How a Crossplane managed resource changes over time](managed-resources-and-lifecycle.md)
- [How a Crossplane provider reaches an external API](providers-and-authentication.md)
- [When to use a managed resource or a Crossplane platform API](providers-compositions-and-managed-resources.md)
- [How a Crossplane Composition fulfills one application request](compositions.md)
- [How one platform request reaches a running application](application-delivery-platform-api.md)
- [Choose how Crossplane repeats and connects resources](deployment-patterns-and-references.md)
- [When to use Terraform or Crossplane](terraform-vs-crossplane.md)
- [How one Crossplane request becomes an AWS network](aws-vpc-platform-api.md)
- [How a team operates a Crossplane platform API](professional-operating-model.md)
- [How an AWS resource request moves through Crossplane](aws-resource-workflow.md)
- [Create and remove one S3 bucket with Crossplane](local-aws-s3-lab.md)
- [Record evidence from a Crossplane S3 sandbox lab](aws-s3-lab-validation-template.md)
- [How GitOps and Crossplane keep a platform request running](production-gitops-and-operations.md)
- [Crossplane on AWS](../../cross-topic-guides/crossplane-on-aws.md)
- [Find the first failing Crossplane handoff](troubleshooting.md)
- [Find the right Crossplane source for your question](references.md)
- [Crossplane v2 overview](https://docs.crossplane.io/latest/whats-new/)
- [Crossplane documentation](https://docs.crossplane.io/latest/)
- [Back to Kubernetes index](../index.md)
- [Back to knowledge index](../../index.md)
