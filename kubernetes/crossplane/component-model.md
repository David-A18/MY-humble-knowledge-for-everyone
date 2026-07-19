# Crossplane component model

## Purpose

Use this page to understand every Crossplane-specific component that appears in a professional control plane: XRDs, XRs, Compositions, Functions, Configuration packages, providers, managed resources, activation policies, operations, environment data, usages, and package runtime controls.

This is the map to read before writing a platform API. Workflow pages show how to deploy resources; this page explains what each object is responsible for and how the objects interact.

## Big picture

Crossplane turns Kubernetes into a control plane for external systems. The Kubernetes API server stores desired state, Crossplane core decides which controllers or functions must act, and providers reconcile external APIs such as AWS.

```text
GitOps, portal, CLI, or user
        |
        v
Kubernetes API server
        |
        +--> Crossplane package manager installs Providers, Functions, and Configurations
        |
        +--> Crossplane composition engine watches XRs and runs Composition pipelines
        |
        +--> Provider controllers watch managed resources and call external APIs
        |
        v
AWS, Azure, Google Cloud, GitHub, Kubernetes, or another external API
```

## Component map

| Component | Kubernetes object | Main job |
| --- | --- | --- |
| Crossplane core | Helm release and core controllers | Runs package management, composition, operation, and Crossplane control logic. |
| Provider package | `Provider` | Installs managed-resource APIs and controllers for an external system. |
| Provider revision | `ProviderRevision` | Tracks an installed provider package version and active or inactive revision state. |
| Provider runtime config | `DeploymentRuntimeConfig` | Customizes provider pod deployment settings such as service account, labels, tolerations, or resources. |
| Image config | `ImageConfig` | Centralizes package image pull secrets, verification, runtime config, or image path rewriting. |
| Managed Resource Definition | `ManagedResourceDefinition` | Represents a provider resource API before or while it is activated into a Kubernetes CRD. |
| Managed Resource Activation Policy | `ManagedResourceActivationPolicy` | Selects which managed-resource APIs from a provider should become active. |
| Managed resource | Provider-specific resource such as `Bucket` or `VPC` | Represents one external object and stores desired state, observed state, finalizers, and external name mapping. |
| Provider config | `ProviderConfig` or `ClusterProviderConfig` | Supplies provider authentication and endpoint configuration for managed resources. |
| Composite Resource Definition | `CompositeResourceDefinition` | Defines a custom platform API schema, known as an XRD. |
| Composite resource | Any resource created from an XRD | Represents one user request for a platform API, known as an XR. |
| Composition | `Composition` | Defines the function pipeline that turns an XR into composed resources. |
| Composition revision | `CompositionRevision` | Captures immutable versions of a Composition for rollout and rollback. |
| Composition function | `Function` package plus function pod | Runs reusable logic inside Composition or Operation pipelines. |
| Function revision | `FunctionRevision` | Tracks an installed function package version and active or inactive revision state. |
| Configuration package | `Configuration` | Installs portable platform APIs, usually XRDs, Compositions, and package dependencies. |
| Configuration revision | `ConfigurationRevision` | Tracks an installed Configuration package version and active or inactive state. |
| Environment config | `EnvironmentConfig` | Provides cluster-scoped data that a Composition can merge into an XR-specific in-memory environment. |
| Usage | `Usage` or `ClusterUsage` | Protects resources from accidental deletion and controls deletion ordering. |
| Operation | `Operation` | Runs a function pipeline once for a maintenance or operational task. |
| Cron operation | `CronOperation` | Creates Operations on a schedule. |
| Watch operation | `WatchOperation` | Creates Operations when selected Kubernetes resources change. |

## Crossplane core

Crossplane core is installed into Kubernetes, usually with Helm. It does not directly know how to create every AWS, Azure, or Google Cloud resource. Instead, it manages packages, watches composite resources, runs composition pipelines, and coordinates Crossplane-specific APIs.

Professional teams treat Crossplane core like a privileged platform service:

- Pin the Crossplane version.
- Back up the management cluster.
- Monitor core controller logs, package health, function health, and reconciliation metrics.
- Upgrade in lower environments before production.

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

## Managed-resource layer

### ManagedResourceDefinition

An MRD represents a provider managed-resource API. Crossplane v2 introduced MRDs so large providers can avoid immediately activating every resource CRD. MRDs are enabled by default in Crossplane v2 and are currently an alpha feature.

```bash
kubectl get managedresourcedefinitions
kubectl get mrd
kubectl describe mrd buckets.s3.aws.m.upbound.io
```

What it does: checks which provider resource APIs exist and whether a specific API is active.

### ManagedResourceActivationPolicy

An MRAP activates selected MRDs. This is useful for large providers where the platform only needs a small subset of services.

```yaml
apiVersion: apiextensions.crossplane.io/v1alpha1
kind: ManagedResourceActivationPolicy
metadata:
  name: aws-networking-and-s3
spec:
  activate:
    - buckets.s3.aws.m.upbound.io
    - vpcs.ec2.aws.m.upbound.io
    - subnets.ec2.aws.m.upbound.io
```

What it does: activates only the managed-resource APIs needed for an S3 and VPC platform instead of exposing the entire provider surface.

> [!NOTE]
> MRDs and MRAPs are Crossplane v2 alpha features. Verify provider support and behavior with the exact Crossplane and provider versions before using them in production.

### Managed Resource

An MR is the Kubernetes representation of one external resource. It has desired state in `spec.forProvider`, observed provider state in `status.atProvider`, conditions in `status.conditions`, and lifecycle controls such as finalizers, external-name annotations, and management policies.

```yaml
apiVersion: ec2.aws.m.upbound.io/v1beta1
kind: VPC
metadata:
  name: payments-vpc
  namespace: payments
spec:
  forProvider:
    region: eu-west-1
    cidrBlock: 10.40.0.0/16
    tags:
      ManagedBy: crossplane
      Owner: payments
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
```

What it does: declares an AWS VPC. The AWS provider controller creates or updates the real VPC and writes observed values back to status.

### Usage

A `Usage` declares that one resource depends on another. It helps prevent accidental deletion and can enforce deletion ordering.

```yaml
apiVersion: apiextensions.crossplane.io/v1beta1
kind: Usage
metadata:
  name: instance-uses-subnet
  namespace: payments
spec:
  of:
    apiVersion: ec2.aws.m.upbound.io/v1beta1
    kind: Subnet
    resourceRef:
      name: private-a
  by:
    apiVersion: ec2.aws.m.upbound.io/v1beta1
    kind: Instance
    resourceRef:
      name: app-server-a
```

What it does: records that an EC2 instance uses a subnet, which helps protect the subnet while the instance exists.

## Platform API layer

### CompositeResourceDefinition

An XRD defines a custom platform API. It is the contract between platform users and platform maintainers. It defines the group, kind, scope, versions, schema, defaults, composition selection defaults, and update policy.

```yaml
apiVersion: apiextensions.crossplane.io/v2
kind: CompositeResourceDefinition
metadata:
  name: applicationnetworks.platform.example.com
spec:
  scope: Namespaced
  group: platform.example.com
  names:
    kind: ApplicationNetwork
    plural: applicationnetworks
  defaultCompositionRef:
    name: application-network-aws
  defaultCompositionUpdatePolicy: Manual
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
                    - us-east-1
                cidrBlock:
                  type: string
                subnetCount:
                  type: integer
                  minimum: 1
                  maximum: 6
              required:
                - region
                - cidrBlock
```

What it does: creates a namespaced `ApplicationNetwork` API and defaults instances to a specific AWS Composition with manual revision updates.

### Composite Resource

An XR is an instance of an XRD-defined API. It is the object application teams, portals, or GitOps workflows usually create.

```yaml
apiVersion: platform.example.com/v1alpha1
kind: ApplicationNetwork
metadata:
  name: payments
  namespace: payments
spec:
  region: eu-west-1
  cidrBlock: 10.40.0.0/16
  subnetCount: 3
```

What it does: requests one application network. Crossplane selects a Composition, runs its function pipeline, creates composed resources, and updates XR status.

### Composition

A Composition is the implementation of an XR. It chooses a function pipeline, passes function input, and names the composed resources that should exist for each XR.

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: application-network-aws
  labels:
    provider: aws
spec:
  compositeTypeRef:
    apiVersion: platform.example.com/v1alpha1
    kind: ApplicationNetwork
  mode: Pipeline
  pipeline:
    - step: render-network
      functionRef:
        name: function-go-templating
      input:
        apiVersion: gotemplating.fn.crossplane.io/v1beta1
        kind: GoTemplate
        source: Inline
        inline:
          template: |
            {{ $xr := getCompositeResource . }}
            ---
            apiVersion: ec2.aws.m.upbound.io/v1beta1
            kind: VPC
            metadata:
              annotations:
                gotemplating.fn.crossplane.io/composition-resource-name: vpc
            spec:
              forProvider:
                region: {{ $xr.spec.region }}
                cidrBlock: {{ $xr.spec.cidrBlock }}
              providerConfigRef:
                name: default
                kind: ClusterProviderConfig
```

What it does: uses a function pipeline to render an AWS VPC from the XR input.

### CompositionRevision

Crossplane creates CompositionRevisions when a Composition changes. XRs can follow the latest compatible revision automatically or stay pinned until a platform operator moves them.

Use manual revision policies for production APIs where a Composition change may resize, replace, or delete infrastructure.

## Functions and environments

### Composition Functions

Functions receive observed state, desired state, function input, pipeline context, and optional required resources. They return desired composed resources and context for later pipeline steps. Functions are how Crossplane implements loops, conditionals, validation, templating, patching, and complex platform logic.

For fixed resource sets, use Patch and Transform. For Terraform-like `for_each`, use Go templating, KCL, CUE, Python, or a custom function.

### EnvironmentConfig

An `EnvironmentConfig` is cluster-scoped data that a Composition can merge into an XR-specific in-memory environment. Use it for shared regional defaults, naming rules, account metadata, or other values that should not be repeated in every XR.

```yaml
apiVersion: apiextensions.crossplane.io/v1beta1
kind: EnvironmentConfig
metadata:
  name: aws-eu-west-1
data:
  region: eu-west-1
  tags:
    CostCenter: platform
    ManagedBy: crossplane
```

What it does: defines reusable composition environment data. Each XR gets its own merged in-memory environment; it cannot read another XR's environment.

## Operations

Operations run function pipelines for tasks that do not fit continuous resource reconciliation. They are useful for validation, backups, maintenance, reporting, and run-to-completion workflows.

```yaml
apiVersion: ops.crossplane.io/v1alpha1
kind: Operation
metadata:
  name: validate-platform-networking
spec:
  mode: Pipeline
  pipeline:
    - step: validate
      functionRef:
        name: function-platform-validator
      input:
        apiVersion: platform.example.com/v1alpha1
        kind: ValidationInput
        environment: production
```

What it does: runs one function pipeline for an operational validation task.

`CronOperation` schedules Operations. `WatchOperation` creates Operations when selected Kubernetes resources change.

> [!NOTE]
> Operations, CronOperations, and WatchOperations are Crossplane v2 alpha features. Use them deliberately and verify the current feature status before production adoption.

## How the pieces interact

1. A platform team installs Crossplane core.
2. The team installs provider packages and function packages.
3. Provider packages create MRDs and provider controllers.
4. MRAPs optionally activate only selected managed-resource APIs.
5. The team configures provider authentication with `ProviderConfig` or `ClusterProviderConfig`.
6. The team defines an XRD to create a stable platform API.
7. The team writes a Composition that points to installed Functions.
8. A user, portal, or GitOps controller creates an XR.
9. Crossplane selects a Composition and runs the function pipeline.
10. Functions render composed resources, usually managed resources plus ordinary Kubernetes resources.
11. Provider controllers reconcile managed resources against AWS or another external API.
12. Managed-resource status, connection details, conditions, and events flow back into Kubernetes.
13. Composition patches or functions can expose selected provider outputs on XR status.
14. GitOps, policy, monitoring, and operators observe the whole system through Kubernetes APIs.

## Inspection commands

```bash
kubectl get providers.pkg.crossplane.io
kubectl get providerrevisions.pkg.crossplane.io
kubectl get functions.pkg.crossplane.io
kubectl get functionrevisions.pkg.crossplane.io
kubectl get configurations.pkg.crossplane.io
kubectl get configurationrevisions.pkg.crossplane.io
kubectl get deploymentruntimeconfigs.pkg.crossplane.io
kubectl get imageconfigs.pkg.crossplane.io
kubectl get managedresourcedefinitions.apiextensions.crossplane.io
kubectl get managedresourceactivationpolicies.apiextensions.crossplane.io
kubectl get xrds
kubectl get compositions
kubectl get compositionrevisions
kubectl get managed -A
kubectl get usages.apiextensions.crossplane.io -A
kubectl get operations.ops.crossplane.io -A
kubectl get cronoperations.ops.crossplane.io -A
kubectl get watchoperations.ops.crossplane.io -A
```

What it does: lists the installed packages, package revisions, platform API definitions, composition runtime objects, managed-resource APIs, managed resources, dependency guards, and operation resources.

## Related links

- [Crossplane](README.md)
- [Crossplane compositions](compositions.md)
- [Deployment patterns and references](deployment-patterns-and-references.md)
- [Managed resources and lifecycle](managed-resources-and-lifecycle.md)
- [Providers and authentication](providers-and-authentication.md)
- [Production, GitOps, and operations](production-gitops-and-operations.md)
- [Crossplane references](references.md)
- [Crossplane packages](https://docs.crossplane.io/latest/packages/providers/)
- [Crossplane functions](https://docs.crossplane.io/latest/packages/functions/)
- [Crossplane configurations](https://docs.crossplane.io/latest/packages/configurations/)
- [Crossplane composition documentation](https://docs.crossplane.io/latest/composition/compositions/)
- [Composite Resource Definitions](https://docs.crossplane.io/latest/composition/composite-resource-definitions/)
- [Composite Resources](https://docs.crossplane.io/latest/composition/composite-resources/)
- [Managed Resource Definitions](https://docs.crossplane.io/latest/managed-resources/managed-resource-definitions/)
- [Managed Resource Activation Policies](https://docs.crossplane.io/latest/managed-resources/managed-resource-activation-policies/)
- [Crossplane Operations](https://docs.crossplane.io/latest/operations/operation/)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
