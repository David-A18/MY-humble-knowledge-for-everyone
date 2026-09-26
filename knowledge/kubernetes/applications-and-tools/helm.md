---
type: "Explanation"
title: "Helm for Kubernetes and Crossplane"
description: "Use this page to understand Helm's chart and release model, safely inspect and"
tags: [kubernetes, applications-and-tools, helm]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# Helm for Kubernetes and Crossplane

## Purpose

Use this page to understand Helm's chart and release model, safely inspect and
operate Helm deployments, and install or upgrade Crossplane in Kubernetes.
It also explains where Helm ends and Crossplane package management begins.

## Key ideas

| Concept | Meaning | Why it matters |
| --- | --- | --- |
| Chart | Versioned package of Kubernetes resource templates and defaults. | Reuses an application or platform installation definition. |
| Release | One installed instance of a chart in a Kubernetes namespace. | Helm tracks its revision and values for upgrade and rollback. |
| Repository | Chart distribution location. | Traditional HTTP indexes and OCI registries are both supported paths. |
| Values | Inputs merged into chart templates. | Keep environment-specific configuration reviewable and separate from chart source. |
| Render | Turn a chart plus values into Kubernetes YAML. | Review the generated objects before changing a cluster. |
| Helm | Installs Crossplane core and optionally initial packages. | It does not replace Crossplane's provider/package lifecycle after installation. |

## Safe Helm workflow

| Task | Command | When to use it |
| --- | --- | --- |
| Inspect chart defaults | `helm show values` | Before writing a values file. |
| Render locally | `helm template` | Before changing a cluster. |
| Preview server interaction | `helm upgrade --install --dry-run --debug` | Before an install or upgrade. |
| Install or upgrade | `helm upgrade --install` | Idempotent release management. |
| Inspect release | `helm status` and `helm get values` | Before troubleshooting or changing it. |
| Review revision history | `helm history` | Before rollback. |
| Roll back | `helm rollback` | After a tested prior revision is known good. |

### Add and inspect a chart repository

```bash
helm repo add <repository-alias> <chart-repository-url>
helm repo update
helm search repo <repository-alias>/<chart-name> --versions
helm show values <repository-alias>/<chart-name> --version <reviewed-version>
```

What it does: adds a repository to the local Helm client, refreshes the chart
index, lists available versions, and prints values for the exact chart version
being considered. Pin a reviewed chart version in automation rather than
silently adopting a later release.

### Render a chart before installation

```bash
helm template <release-name> <repository-alias>/<chart-name> \
  --namespace <namespace> \
  --version <reviewed-version> \
  --values values.yaml > rendered.yaml

kubectl apply --dry-run=server -f rendered.yaml
```

What it does: renders the chart locally and asks the Kubernetes API to validate
the generated resources without storing them. Review `rendered.yaml` carefully;
some charts use hooks or resources that a static render cannot fully model.

### Install or upgrade a release

```bash
helm upgrade --install <release-name> <repository-alias>/<chart-name> \
  --namespace <namespace> \
  --create-namespace \
  --version <reviewed-version> \
  --values values.yaml \
  --dry-run --debug
```

What it does: previews the same idempotent command used for an installation or
upgrade. Remove `--dry-run --debug` only after reviewing the rendered output,
the selected values, and the scope of resources it can change.

### Inspect, roll back, and uninstall

```bash
helm status <release-name> --namespace <namespace>
helm get values <release-name> --namespace <namespace> --all
helm history <release-name> --namespace <namespace>
helm rollback <release-name> <revision> --namespace <namespace>
```

What it does: reads release state and values, lists known revisions, then rolls
back to a selected revision. Test rollback behavior in a non-production cluster:
some resource changes, CRD changes, hooks, and external side effects are not
reversed merely because Helm restores an earlier release manifest.

> [!WARNING]
> `helm uninstall` deletes the release's tracked Kubernetes resources. Before
> uninstalling a platform chart, identify CRDs, controllers, custom resources,
> persistent data, and external resources that may outlive or be orphaned by the
> removal. Do not use an uninstall as a generic repair action.

## Install Crossplane with Helm

Crossplane installs into an existing Kubernetes cluster through its official
Helm chart. The chart installs Crossplane core, which then enables `Provider`,
`Function`, and `Configuration` package objects.

### Discover the chart and its values

```bash
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update
helm search repo crossplane-stable/crossplane --versions
helm show values crossplane-stable/crossplane --version <reviewed-version>
```

What it does: uses the official stable repository, then lets the operator select
and inspect a tested chart version. Consult the current [Crossplane installation documentation](https://docs.crossplane.io/latest/get-started/install/) for supported Kubernetes and Helm versions.

### Use a reviewed values file

```bash
helm show values crossplane-stable/crossplane \
  --version <reviewed-version> > crossplane-values.defaults.yaml

cp crossplane-values.defaults.yaml crossplane-values.yaml
```

What it does: saves the defaults from the exact chart version under review and
creates the values file that will be changed and committed. Remove irrelevant
defaults and edit only keys that exist in that version. Keep reviewed non-secret
values in Git. Do not assume a key exists merely because it appeared in another
chart version, and keep cloud credentials out of Helm values; use an approved
workload-identity or secret-delivery method for provider controllers.

### Preview, install, and check Crossplane

```bash
helm upgrade --install crossplane crossplane-stable/crossplane \
  --namespace crossplane-system \
  --create-namespace \
  --version <reviewed-version> \
  --values crossplane-values.yaml \
  --dry-run --debug

helm upgrade --install crossplane crossplane-stable/crossplane \
  --namespace crossplane-system \
  --create-namespace \
  --version <reviewed-version> \
  --values crossplane-values.yaml

kubectl get pods -n crossplane-system
kubectl get crds | grep crossplane
```

What it does: previews and then installs the Crossplane chart, followed by a
basic health and API check. A running Crossplane pod only confirms core is
available; providers and their credentials still need separate installation and
validation.

## Helm-installed providers versus Provider objects

Crossplane's Helm chart can install provider packages during the initial
Crossplane installation through chart values. This is useful for a small,
fully-controlled bootstrap. A separate `Provider` manifest is generally easier
to review, promote, upgrade, and roll back independently from Crossplane core.

| Choice | Best fit | Trade-off |
| --- | --- | --- |
| Chart value `provider.packages` | Initial lab or tightly coupled bootstrap. | Provider lifecycle is coupled to Helm chart configuration. |
| Separate `Provider` manifests | Production GitOps and independent provider promotion. | Requires explicit ordering and package health checks. |
| Configuration package dependency | Reusable platform API distribution. | Requires dependency/version management discipline. |

### Declare a provider after Crossplane is healthy

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws-ecr
spec:
  package: xpkg.upbound.io/upbound/provider-aws-ecr:<reviewed-version-or-digest>
  revisionActivationPolicy: Manual
```

What it does: installs the ECR provider as an independently reviewed Crossplane
package. The placeholder is intentional: copy the package location and version
or digest from the [Upbound Marketplace](https://marketplace.upbound.io/providers/upbound/provider-aws-ecr) after checking compatibility.

```bash
kubectl apply --dry-run=server -f provider-aws-ecr.yaml
kubectl apply -f provider-aws-ecr.yaml
kubectl get providers.pkg.crossplane.io -w
kubectl get providerrevisions.pkg.crossplane.io
```

What it does: validates the manifest, installs the package, waits for its
health condition, and exposes package revision information. Do not create ECR
managed resources until the provider is installed, healthy, and its schema is
visible through Kubernetes discovery.

> [!WARNING]
> Do not remove a provider before the managed resources it controls have been
> deliberately retained or deleted. Removing the controller can leave external
> resources unmanaged and finalizers unable to complete.

## Upgrade Crossplane safely

1. Read the target chart release notes, Crossplane upgrade guidance, provider
   compatibility, and any CRD migration notes.
2. Render the exact upgrade with the production values file and review the
   generated objects.
3. Test core, provider, function, and Composition versions together in a
   non-production control plane.
4. Back up Crossplane objects and preserve external-name mappings.
5. Upgrade Crossplane core separately from major provider or Composition
   changes when that makes diagnosis and rollback clearer.
6. Confirm core pods, package health, provider APIs, representative MRs, and
   composition renders after the change.

Helm's revision history covers the release manifest. It does not replace
Crossplane `ProviderRevision`, `FunctionRevision`, or `CompositionRevision`.
Each layer needs its own tested promotion and rollback strategy.

## Troubleshooting

| Symptom | Likely cause | First check |
| --- | --- | --- |
| Helm preview differs from the cluster | Values, capabilities, hooks, or chart version differ. | Exact chart version, values, and `helm get manifest`. |
| Crossplane pods are not ready | Image pull, RBAC, resources, or cluster policy problem. | `kubectl describe pod` and namespace events. |
| Provider is installed but unhealthy | Dependency, compatibility, package pull, or runtime failure. | `kubectl describe providerrevision` and provider logs. |
| A Crossplane MR kind is unknown | Provider is not healthy or its APIs are not active. | `kubectl api-resources` and activation policy. |
| Rollback did not restore external infrastructure | Helm only rolled back its own rendered objects. | Provider/MR status, CompositionRevision, and AWS audit trail. |

## Related links

- [Amazon ECR and Helm OCI charts](../../cloud/aws/compute/amazon-ecr.md)
- [Providers, managed resources, and compositions](../crossplane/providers-compositions-and-managed-resources.md)
- [Application delivery platform API](../crossplane/application-delivery-platform-api.md)
- [Crossplane AWS resource workflow](../crossplane/aws-resource-workflow.md)
- [Helm documentation](https://helm.sh/docs/intro/using_helm/)
- [Crossplane installation documentation](https://docs.crossplane.io/latest/get-started/install/)
- [Crossplane providers documentation](https://docs.crossplane.io/latest/packages/providers/)
- [Back to Kubernetes applications and tools](index.md)
- [Back to Kubernetes index](../index.md)
- [Back to root index](../../../README.md)
