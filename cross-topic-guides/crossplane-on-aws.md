# Crossplane on AWS

## Purpose

Use this guide to run Crossplane in Kubernetes while managing AWS resources with clear bootstrap, authentication, account, GitOps, and ownership boundaries.

Core Crossplane concepts belong in [Crossplane](../kubernetes/crossplane/README.md). This page focuses on AWS-specific decisions.

For the install-to-resource-management procedure, use [Crossplane AWS resource workflow](../kubernetes/crossplane/aws-resource-workflow.md).

## Architecture

| Component | Responsibility |
| --- | --- |
| Management Kubernetes cluster | Hosts Crossplane, AWS providers, functions, GitOps, policy, and observability. |
| AWS provider packages | Add AWS managed-resource APIs and controller pods. |
| ProviderConfig or ClusterProviderConfig | Defines AWS authentication and account targeting. |
| Platform APIs and compositions | Expose standardized AWS capabilities to teams. |
| AWS accounts | Hold external resources reconciled by provider controllers. |
| GitOps controller | Applies provider packages, platform APIs, and resource requests from Git. |

Common flow:

```text
Terraform, eksctl, CDK, or CloudFormation
        |
Management EKS cluster
        |
Crossplane and AWS providers
        |
Development, staging, production, network, or security AWS accounts
```

Crossplane requires Kubernetes first. Use a bootstrap tool to create the first management cluster, then let Crossplane reconcile the platform resources it is designed to own.

## AWS provider packages

AWS support is usually split into a provider family plus service-specific providers. For example, an S3 provider package installs S3 managed-resource APIs, while the provider family supplies common AWS authentication types.

### Install an AWS provider

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws-s3
spec:
  package: xpkg.upbound.io/upbound/provider-aws-s3:v2.6.1
  packagePullPolicy: IfNotPresent
  revisionActivationPolicy: Automatic
  revisionHistoryLimit: 1
```

What it does: installs a pinned S3 provider package. Verify the latest package and schema in the provider marketplace before using it in production.

### Check package health

```bash
kubectl get providers.pkg.crossplane.io
kubectl get providerrevisions.pkg.crossplane.io
kubectl get pods -n crossplane-system
```

What it does: confirms package installation, active revisions, and provider pod health.

## AWS authentication options

| Environment | Recommended pattern | Notes |
| --- | --- | --- |
| Local `kind` lab | Temporary access keys in a Kubernetes Secret. | Keep it short-lived and sandbox-only. |
| EKS production | EKS Pod Identity when the provider image and AWS SDK path support it. | EKS-native role association, temporary credentials, and clean separation from OIDC provider setup. |
| EKS with IRSA requirements | IAM Roles for Service Accounts. | Use when existing controls or compatibility require `AssumeRoleWithWebIdentity`. |
| Multi-account platform | Provider role assumes target account roles. | Separate provider configs by account, environment, or capability. |
| Hosted or Upbound control plane | Follow hosted provider authentication docs. | Usually OIDC or provider-specific workload identity. |

### Static credentials for a temporary lab

```bash
kubectl create secret generic aws-secret \
  --namespace=crossplane-system \
  --from-file=creds=./aws-credentials.ini
```

What it does: creates a Secret for a temporary local lab.

> [!WARNING]
> Do not use long-lived static access keys for production Crossplane providers. Prefer temporary workload identity and least privilege.

### Cluster-wide provider config

```yaml
apiVersion: aws.m.upbound.io/v1beta1
kind: ClusterProviderConfig
metadata:
  name: production-s3
spec:
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: aws-secret
      key: creds
```

What it does: defines a cluster-wide AWS credential source. Use namespaced `ProviderConfig` when team or namespace isolation is required.

## EKS Pod Identity checks

Before running AWS provider pods with EKS Pod Identity, verify:

- The EKS Pod Identity Agent is installed, unless EKS Auto Mode handles it.
- The provider controller uses the intended ServiceAccount.
- The Pod Identity association maps that ServiceAccount to the intended IAM role.
- The provider image uses an AWS SDK credential provider chain that can consume Pod Identity credentials.
- CloudTrail shows sessions for the expected IAM role.
- Cross-account access uses delegated roles from the pod identity role.

## IRSA checks

Before using IRSA, verify:

- The EKS cluster has an IAM OIDC provider in the AWS account.
- The provider ServiceAccount has the correct role annotation.
- The IAM role trust policy matches issuer, audience, namespace, and ServiceAccount.
- Provider pods mount projected service account tokens.
- CloudTrail shows `AssumeRoleWithWebIdentity` for the intended role.

## Multi-account model

```text
Management EKS cluster in platform account
        |
        +-- development account role
        +-- staging account role
        +-- production account role
        +-- shared network account role
        +-- security account role
```

Use:

- Separate ProviderConfigs for each target account or capability.
- Least-privilege IAM actions for each provider.
- Permission boundaries and SCPs.
- Session tags for attribution.
- Namespace and RBAC boundaries.
- Admission policy to restrict which teams can select production ProviderConfigs.

Do not let application teams choose arbitrary production credentials unless that is an explicit platform contract.

## Crossplane and Terraform ownership

Use Terraform or another bootstrap tool for:

- AWS Organizations and baseline accounts.
- The first management VPC or EKS cluster.
- Shared identity and security foundations.
- Initial GitOps installation.
- Policies that must exist before Crossplane can safely run.

Use Crossplane for:

- Repeated self-service resources.
- Platform APIs such as `SecureBucket`, `DatabaseInstance`, or `ApplicationEnvironment`.
- Long-running drift reconciliation.
- Namespaced developer-facing infrastructure requests.
- Workload clusters and shared services when ownership is clear.

> [!IMPORTANT]
> Avoid two active owners. Terraform can create a resource that Crossplane observes, or Crossplane can create a resource Terraform reads through data sources, but both tools should not update the same fields.

## Example secure bucket request

The user-facing XR can stay small:

```yaml
apiVersion: platform.example.com/v1alpha1
kind: SecureBucket
metadata:
  name: payments-data
  namespace: payments
spec:
  region: eu-west-1
  dataClassification: confidential
```

What it does: requests a standardized bucket. The AWS-specific composition can generate the bucket, public-access block, encryption, versioning, lifecycle, logging, tags, and policy resources.

## Operational controls

| Control | AWS-specific reason |
| --- | --- |
| Provider IAM least privilege | Provider credentials define maximum AWS blast radius. |
| SCPs and permission boundaries | Protect against provider or composition mistakes. |
| CloudTrail | Attribute create, update, delete, and assume-role events. |
| AWS Config and Security Hub | Detect drift or policy failures outside Crossplane. |
| Budgets and cost tags | Prevent self-service APIs from hiding spend. |
| Deletion protection | Protect critical RDS, EKS, and networking resources. |
| Access Analyzer | Review provider IAM role reach. |

## Troubleshooting AWS resources

Start in Kubernetes:

```bash
kubectl describe <aws-resource-kind> <name> -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
kubectl logs -n crossplane-system \
  -l pkg.crossplane.io/provider=<provider-name> \
  --tail=200
```

What it does: shows provider conditions, events, and controller errors.

Then verify AWS state:

```bash
aws sts get-caller-identity
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRole \
  --max-results 10
```

What it does: confirms identity and recent assume-role activity.

For stuck deletions, check AWS deletion protection, dependencies, non-empty buckets, attached network interfaces, security group references, provider delete permissions, and finalizers.

## Production checklist

- Prefer least-privilege AWS permissions for provider controllers.
- Separate platform API design from provider implementation details.
- Use GitOps for Crossplane packages and compositions.
- Monitor managed-resource conditions and provider logs.
- Define deletion policy and recovery behavior before exposing APIs.
- Pin provider and function versions.
- Verify provider schemas with `kubectl explain` and provider documentation.
- Use EKS Pod Identity or IRSA instead of long-lived credentials for production.
- Separate ProviderConfigs by account, environment, and capability.
- Protect the management cluster as privileged infrastructure.
- Keep AWS guardrails outside Crossplane as defense in depth.
- Back up XRs, managed resources, provider configs, and external-name mappings.

## Related links

- [Crossplane](../kubernetes/crossplane/README.md)
- [Crossplane AWS resource workflow](../kubernetes/crossplane/aws-resource-workflow.md)
- [Crossplane professional operating model](../kubernetes/crossplane/professional-operating-model.md)
- [Providers and authentication](../kubernetes/crossplane/providers-and-authentication.md)
- [Managed resources and lifecycle](../kubernetes/crossplane/managed-resources-and-lifecycle.md)
- [Crossplane compositions](../kubernetes/crossplane/compositions.md)
- [Production, GitOps, and operations](../kubernetes/crossplane/production-gitops-and-operations.md)
- [Crossplane troubleshooting](../kubernetes/crossplane/troubleshooting.md)
- [Crossplane references](../kubernetes/crossplane/references.md)
- [Crossplane providers documentation](https://docs.crossplane.io/latest/packages/providers/)
- [AWS EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)
- [AWS IAM Roles for Service Accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
