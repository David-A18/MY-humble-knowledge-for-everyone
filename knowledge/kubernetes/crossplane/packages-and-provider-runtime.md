---
type: Explanation
title: Crossplane packages and provider runtime
description: Understand how Crossplane installs providers, functions, and configurations as packages, and how provider pods run and authenticate to cloud APIs.
tags: [kubernetes, crossplane, packages, providers]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# Crossplane packages and provider runtime

This page explains how Crossplane installs its building blocks as packages and how the provider processes that talk to cloud APIs run and authenticate. It is part of [Crossplane component model](component-model.md).

## Packages

Crossplane package objects live in the `pkg.crossplane.io` API group. The main package types are `Provider`, `Function`, and `Configuration`.

### Provider

A `Provider` installs managed-resource APIs and provider controllers. For AWS, a provider might install APIs for S3 buckets, EC2 VPCs, IAM roles, or RDS instances. The provider pod is the component that authenticates to AWS and calls AWS APIs.

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws-s3
spec:
  package: xpkg.crossplane.io/crossplane-contrib/provider-aws-s3:v2.0.0
  revisionActivationPolicy: Manual
  revisionHistoryLimit: 2
```

What it does: installs a pinned AWS S3 provider package and keeps package activation under manual control.

### ProviderRevision

A `ProviderRevision` is created by Crossplane when a provider package is installed or upgraded. It records the resolved image, revision number, dependency state, health, and whether the revision is active.

Use it when provider installation looks successful but the managed-resource APIs or controller pods are missing:

```bash
kubectl get providers.pkg.crossplane.io
kubectl get providerrevisions.pkg.crossplane.io
kubectl describe providerrevision
```

What it does: separates the user-facing provider package from the concrete package revision Crossplane actually installed.

### Function

A `Function` installs logic that a Composition or Operation can call. Common functions include Patch and Transform for declarative patching, Go templating for loops and conditional rendering, and KCL for programmable configuration.

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Function
metadata:
  name: function-go-templating
spec:
  package: xpkg.crossplane.io/crossplane-contrib/function-go-templating:v0.11.0
```

What it does: installs a function package that can render composed resources from Go templates.

### FunctionRevision

A `FunctionRevision` is the concrete installed version of a function package. Inspect it when a Composition references an installed Function but the function pod is unhealthy, signature verification fails, or an ImageConfig changes package runtime behavior.

```bash
kubectl get functions.pkg.crossplane.io
kubectl get functionrevisions.pkg.crossplane.io
kubectl describe functionrevision
```

What it does: shows whether the function package revision is active, healthy, verified, and running with the expected runtime configuration.

### Configuration

A `Configuration` is a portable OCI package for a platform API release. It usually contains XRDs, Compositions, provider dependencies, function dependencies, and package metadata.

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Configuration
metadata:
  name: platform-networking
spec:
  package: xpkg.example.com/platform/networking:v1.4.0
  revisionActivationPolicy: Manual
  revisionHistoryLimit: 3
```

What it does: installs a versioned platform networking API bundle and allows a platform team to activate the new revision deliberately.

### ConfigurationRevision

A `ConfigurationRevision` is the installed version of a Configuration package. It is useful for confirming dependency resolution, active revision selection, and package health after a platform API release.

```bash
kubectl get configurations.pkg.crossplane.io
kubectl get configurationrevisions.pkg.crossplane.io
kubectl describe configurationrevision
```

What it does: shows whether the platform package is installed, healthy, and active.

### ImageConfig

`ImageConfig` centralizes package-image behavior. Use it for private registry pull secrets, signature verification, package runtime configuration, or image path rewrites.

This matters in enterprises where providers, functions, and configurations must come from an internal registry or must be verified before running.

## Provider runtime and authentication

Provider authentication is not part of an XR or Composition. Managed resources reference a `ProviderConfig` or `ClusterProviderConfig`, and the provider controller uses that configuration to authenticate to the external API.

```yaml
apiVersion: aws.upbound.io/v1beta1
kind: ClusterProviderConfig
metadata:
  name: default
spec:
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: aws-creds
      key: creds
```

What it does: gives AWS provider controllers credential material from a Kubernetes Secret. For production on EKS, prefer workload identity over long-lived static keys when the provider supports it.

Use `DeploymentRuntimeConfig` when the provider pod needs a specific Kubernetes service account, scheduling rule, resource request, or runtime metadata.

```yaml
apiVersion: pkg.crossplane.io/v1beta1
kind: DeploymentRuntimeConfig
metadata:
  name: aws-provider-runtime
spec:
  serviceAccountTemplate:
    metadata:
      name: crossplane-provider-aws
  deploymentTemplate:
    spec:
      selector: {}
      template:
        spec:
          containers:
            - name: package-runtime
              resources:
                requests:
                  cpu: 100m
                  memory: 256Mi
```

What it does: sets runtime properties for package pods. Attach it from a provider with `spec.runtimeConfigRef`.

## Related links

- [Crossplane component model](component-model.md)
- [Back to index](index.md)
