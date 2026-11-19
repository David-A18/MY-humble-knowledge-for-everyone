---
type: Explanation
title: Crossplane reusable templates versus Terraform modules
description: Compare how Terraform modules and Crossplane XRDs, Compositions, and functions package reusable infrastructure.
tags: [kubernetes, crossplane, terraform]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# Crossplane reusable templates versus Terraform modules

If you already know Terraform modules, this page maps that idea onto Crossplane's reusable templates. It is part of [Crossplane deployment patterns and references](deployment-patterns-and-references.md).

## Terraform modules versus Crossplane reusable templates

Terraform modules and Crossplane platform APIs solve a similar reuse problem, but they run in different systems.

A Terraform module is a reusable Terraform code unit. A caller passes variables, Terraform builds an execution graph, plans the changes, applies them, and writes outputs to Terraform state.

Crossplane does not use "modules" as the main reuse primitive. The closest professional pattern is:

| Terraform module concept | Crossplane equivalent | What changes operationally |
| --- | --- | --- |
| Module input variables | XR `spec` fields defined by an XRD | Users submit Kubernetes objects instead of calling module blocks. |
| Module resources | Composed resources produced by a Composition | Crossplane controllers reconcile resources continuously after creation. |
| Module logic | Composition Functions | Loops, conditionals, transforms, validation, and lookups happen in function pipelines. |
| Module outputs | XR `status` fields and connection secrets | Outputs are observed asynchronously and stored on Kubernetes resources. |
| Module version | Configuration package version or GitOps-managed Composition version | Platform teams promote package versions or Composition revisions. |
| Module registry | OCI registry or Upbound Marketplace package | Crossplane packages are installed into a control plane. |
| Module call | XR manifest | Application teams request a product-like API instance. |
| `terraform plan` | Composition render, dry-run, policy, Git review, and sandbox reconciliation | Crossplane does not provide the same native plan/apply approval loop. |

The important difference is ownership. In Terraform, the module caller often sees and controls the module inputs directly from an IaC repository. In Crossplane, the platform team usually owns the XRD, Composition, Functions, and Configuration package. Application teams create only the XR, which should be small, validated, and stable.

### Crossplane reusable-template layers

| Layer | Reuse role | Example |
| --- | --- | --- |
| XRD | Defines the reusable product API. | `ApplicationNetwork`, `SecureBucket`, `PostgresInstance`. |
| Composition | Defines the infrastructure template behind that API. | One VPC, N subnets, route tables, tags, and optional EC2 instances. |
| Function | Adds template logic. | Loop over `spec.subnets`, enforce naming rules, copy IDs to XR status. |
| Configuration package | Ships the reusable API as a versioned bundle. | `xpkg.example.com/platform/networking:v1.4.0`. |
| XR | Calls the reusable API. | `kind: ApplicationNetwork` with a region and subnet list. |

Use a Composition alone when the reusable template is internal to one cluster and lifecycle is simple. Use a Configuration package when the platform API should be versioned, promoted, shared across clusters, installed as a dependency, or treated like a product release.

For a full fixed-resource AWS network example, see [AWS VPC platform API](aws-vpc-platform-api.md). It shows a single `PlatformNetwork` XR that composes VPC, subnet, network ACL, route table, and VPC endpoint managed resources.

### Example Terraform module call

```hcl
module "network" {
  source  = "git::https://example.com/platform/terraform-aws-network.git?ref=v1.4.0"
  name    = "payments"
  region  = "eu-west-1"
  vpc_cidr = "10.30.0.0/16"

  subnets = {
    private-a = {
      availability_zone = "eu-west-1a"
      cidr_block        = "10.30.1.0/24"
    }
    private-b = {
      availability_zone = "eu-west-1b"
      cidr_block        = "10.30.2.0/24"
    }
  }
}
```

What it does: calls a reusable Terraform module. Terraform expands the module, plans the graph, applies the resources, and stores outputs in Terraform state.

### Example Crossplane XR call

```yaml
apiVersion: platform.example.com/v1alpha1
kind: ApplicationNetwork
metadata:
  name: payments
  namespace: payments
spec:
  region: eu-west-1
  vpcCidr: 10.30.0.0/16
  subnets:
    - name: private-a
      availabilityZone: eu-west-1a
      cidrBlock: 10.30.1.0/24
    - name: private-b
      availabilityZone: eu-west-1b
      cidrBlock: 10.30.2.0/24
```

What it does: creates one request for a reusable Crossplane platform API. The user does not apply raw VPC, subnet, route-table, or security resources. Crossplane selects the Composition and continuously reconciles the composed resources.

### Example Configuration package metadata

```yaml
apiVersion: meta.pkg.crossplane.io/v1
kind: Configuration
metadata:
  name: platform-networking
spec:
  crossplane:
    version: ">=v2.0.0"
  dependsOn:
    - apiVersion: pkg.crossplane.io/v1
      kind: Provider
      package: xpkg.upbound.io/upbound/provider-aws-ec2
      version: ">=v2.6.1"
    - apiVersion: pkg.crossplane.io/v1
      kind: Function
      package: xpkg.crossplane.io/crossplane-contrib/function-go-templating
      version: ">=v0.11.0"
```

What it does: defines package metadata for a reusable Crossplane platform API. The package can include XRD and Composition YAML files, and it can declare provider or function dependencies.

### Install the reusable Crossplane package

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Configuration
metadata:
  name: platform-networking
spec:
  package: xpkg.example.com/platform/networking:v1.4.0
  revisionActivationPolicy: Manual
```

What it does: installs the reusable platform package into a Crossplane control plane. With manual activation, operators can inspect the `ConfigurationRevision` before promoting the new implementation.

### Build and publish a Configuration package

```bash
crossplane xpkg build \
  --package-root package \
  --package-file platform-networking.xpkg

crossplane xpkg push \
  xpkg.example.com/platform/networking:v1.4.0 \
  --package-files platform-networking.xpkg
```

What it does: builds and publishes a Crossplane Configuration package from a directory containing `crossplane.yaml`, XRDs, and Compositions.

> [!IMPORTANT]
> Configuration packages are for platform APIs, not arbitrary Kubernetes YAML bundles. Keep bootstrap objects such as namespaces, provider credentials, RBAC, and GitOps application objects in the platform bootstrap layer unless the package documentation explicitly supports including them.

### When to choose each pattern

| Situation | Prefer Terraform module | Prefer Crossplane platform API |
| --- | --- | --- |
| You need a reviewed plan before every change | Yes | Only with extra GitOps, render, policy, and environment gates. |
| You are bootstrapping the management cluster | Yes | No, Crossplane needs Kubernetes first. |
| Developers need self-service infrastructure from Kubernetes | Usually no | Yes. |
| Infrastructure must be continuously reconciled | Usually no | Yes. |
| One platform team owns a standard product across many teams | Sometimes | Yes. |
| The resource shape changes rarely and is not Kubernetes-centered | Yes | Maybe not. |
| You want a stable API that hides provider details | Possible, but module callers still use Terraform | Yes, use an XRD and Composition. |

The strongest pattern is not "replace every Terraform module." Use Terraform modules for bootstrap and plan-heavy infrastructure, then use Crossplane platform APIs for long-lived self-service products that benefit from Kubernetes RBAC, GitOps, status, and reconciliation.

## Terraform comparison

| Terraform pattern | Crossplane pattern |
| --- | --- |
| `count` for N similar resources | Function loop over a number or list from XR spec. |
| `for_each` over a map/list | Go templating `range`, KCL loop, CUE, Python, or custom function. |
| Reusable module | XRD plus Composition; distribute with a Configuration package when reuse crosses clusters or teams. |
| `aws_vpc.main.id` | `vpcIdRef`, `vpcIdSelector`, or a status patch from VPC to XR. |
| `aws_subnet.private["a"].id` | Labels plus `subnetIdSelector.matchLabels`, usually with `matchControllerRef`. |
| Module output | XR `status`, connection secrets, or a higher-level platform API. |
| Terraform state | Kubernetes desired state, status, external-name annotations, finalizers, and provider runtime state. |
| Plan | Composition render, dry-run, Git review, policy, and sandbox reconciliation. |

## Related links

- [Crossplane deployment patterns and references](deployment-patterns-and-references.md)
- [Back to index](index.md)
