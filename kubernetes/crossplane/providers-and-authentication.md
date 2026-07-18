# Crossplane providers and authentication

## Purpose

Use this page to understand Crossplane provider packages, provider configs, authentication choices, package health, and schema validation.

Providers extend Crossplane with external APIs. Installing a provider creates Kubernetes API types for managed resources and starts controller pods that reconcile those resources.

## Provider package model

Crossplane packages are OCI images. The main package types are:

| Package type | Contains | Example use |
| --- | --- | --- |
| Provider | Managed-resource APIs and controllers. | Add AWS S3, EC2, RDS, Kubernetes, Helm, or GitHub APIs. |
| Function | Composition or operation logic. | Patch and transform, Go templating, KCL, CUE, Python, or custom functions. |
| Configuration | Platform APIs and package dependencies. | Bundle XRDs, compositions, providers, and functions into a versioned platform release. |

### Install a provider

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

What it does: installs a pinned AWS S3 provider package. The exact package name and version should come from the provider's official package documentation or marketplace page.

### Check provider health

```bash
kubectl get providers.pkg.crossplane.io
kubectl get providerrevisions.pkg.crossplane.io
kubectl get pods -n crossplane-system
```

What it does: verifies package installation, active revisions, and provider controller pods.

Expected provider status resembles:

```text
NAME              INSTALLED   HEALTHY   PACKAGE
provider-aws-s3   True        True      xpkg.upbound.io/upbound/provider-aws-s3:v2.6.1
```

## ProviderConfig and ClusterProviderConfig

A provider config tells the provider how to authenticate and connect to the external system.

| Type | Scope | Use it when |
| --- | --- | --- |
| `ProviderConfig` | Namespaced. | A tenant, team, or namespace should own its provider credentials. |
| `ClusterProviderConfig` | Cluster-wide. | Shared platform credentials are intentionally exposed across namespaces. |

### Namespaced provider config

```yaml
apiVersion: aws.m.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
  namespace: payments
spec:
  credentials:
    source: Secret
    secretRef:
      namespace: payments
      name: aws-secret
      key: creds
```

What it does: defines AWS credentials for managed resources in the `payments` namespace.

### Cluster-wide provider config

```yaml
apiVersion: aws.m.upbound.io/v1beta1
kind: ClusterProviderConfig
metadata:
  name: default
spec:
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: aws-secret
      key: creds
```

What it does: defines AWS credentials that managed resources can reference across namespaces.

> [!IMPORTANT]
> Some providers fall back to a provider config named `default` when `providerConfigRef` is omitted. Production manifests should reference the intended provider config explicitly.

## Authentication choices

| Environment | Common model | Notes |
| --- | --- | --- |
| Temporary local lab | Short-lived access keys in a Kubernetes Secret. | Use only in a sandbox account; never commit secrets. |
| EKS production | EKS Pod Identity when supported by the provider image and AWS SDK path. | Simpler EKS-native association model. |
| EKS with IRSA requirements | IAM Roles for Service Accounts. | Useful when IRSA-specific trust controls are required. |
| Multi-account AWS | Base provider role plus `AssumeRole` to target accounts. | Separate provider configs by environment or account. |
| Hosted control plane | Provider-specific OIDC or workload identity flow. | Follow the hosted platform documentation. |

### Static credentials secret for a lab

```bash
kubectl create secret generic aws-secret \
  --namespace=crossplane-system \
  --from-file=creds=./aws-credentials.ini
```

What it does: creates a Kubernetes Secret from a local AWS credentials file without printing the credential values.

> [!WARNING]
> Static access keys are suitable only for short-lived isolated labs. Rotate or delete the keys after the lab and keep credential files out of Git.

### EKS Pod Identity fit

For EKS, Pod Identity maps an IAM role to a Kubernetes ServiceAccount through an EKS association. It provides temporary credentials through the EKS Pod Identity Agent and supported AWS SDK credential chains.

Before using it for provider pods, verify:

- The EKS Pod Identity Agent is installed or EKS Auto Mode handles it.
- The provider Deployment uses the expected ServiceAccount.
- The provider image uses an AWS SDK credential chain compatible with Pod Identity.
- CloudTrail shows the expected role sessions.
- Cross-account access is handled through role delegation where needed.

### IRSA fit

IRSA uses the EKS OIDC issuer, an IAM OIDC provider, a service-account annotation, and STS `AssumeRoleWithWebIdentity`.

Use it when:

- Your organization already standardizes on IRSA.
- You need IRSA-specific trust-policy controls.
- Provider compatibility with Pod Identity has not been proven.

## Least privilege

Provider credentials need more than create permissions. Reconciliation usually needs read, list, tag, update, and delete permissions depending on lifecycle policy.

Prefer:

```text
provider-aws-s3 ServiceAccount
  -> S3 platform role

provider-aws-ec2 ServiceAccount
  -> Network platform role

provider-aws-rds ServiceAccount
  -> Database platform role
```

instead of:

```text
one provider role
  -> AdministratorAccess
```

Use permission boundaries, service control policies, CloudTrail, Access Analyzer, and explicit deny guardrails for high-risk environments.

## Managed resource activation policies

Large providers can install many managed-resource APIs. Crossplane v2 includes Managed Resource Activation Policies to activate only selected ManagedResourceDefinitions.

Use activation policies when:

- A provider ships many APIs but the platform needs only a few.
- API-server memory and discovery load matter.
- You want to reduce accidental access to unused resource kinds.
- Provider package installation should stay scoped to approved services.

## Validate installed APIs

### List provider APIs

```bash
kubectl api-resources | grep -E 'aws|upbound|crossplane'
```

What it does: shows which API groups and resource kinds are actually installed.

### Explain a provider schema

```bash
kubectl explain bucket.s3.aws.m.upbound.io.spec.forProvider
```

What it does: shows fields supported by the installed provider version.

### Dry-run a manifest

```bash
kubectl apply --dry-run=server -f bucket.yaml
```

What it does: asks the Kubernetes API server to validate the manifest against installed schemas without creating or updating the resource.

## Related links

- [Crossplane](README.md)
- [Managed resources and lifecycle](managed-resources-and-lifecycle.md)
- [Crossplane on AWS](../../cross-topic-guides/crossplane-on-aws.md)
- [Crossplane references](references.md)
- [Crossplane providers documentation](https://docs.crossplane.io/latest/packages/providers/)
- [Managed resource activation policies](https://docs.crossplane.io/latest/managed-resources/managed-resource-activation-policies/)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
