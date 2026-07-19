# Crossplane deployment patterns and references

## Purpose

Use this page to understand how to deploy multiple related resources with Crossplane, how to model Terraform-style `count` and `for_each`, and how resources reference each other when one resource needs values from another.

Crossplane can deploy multiple resources together, but it does not work exactly like Terraform. Terraform builds a plan-time expression graph. Crossplane stores desired state in Kubernetes, then controllers reconcile asynchronously. References are resolved by controllers through Kubernetes objects, labels, selectors, status, and connection details.

## Quick answer

| Terraform question | Crossplane answer |
| --- | --- |
| Can I put many resources in one file? | Yes. Use a multi-document YAML file separated with `---`. |
| Is there a native `count` or `for_each` in plain YAML? | No. Plain YAML repeats resources explicitly. |
| What is the Crossplane equivalent of reusable infrastructure? | Use an XRD as the API contract, a Composition as the implementation template, Functions for logic, and a Configuration package to distribute the platform API. |
| What is the equivalent of loops? | Composition Functions such as Go templating, KCL, CUE, Python, or custom functions. |
| Can resources reference each other? | Yes. Use provider `*Ref`, `*Selector`, `matchControllerRef`, patches, XR status, and connection secrets. |
| Can one resource use provider-generated IDs from another? | Yes, when the provider exposes references or when a Composition patches observed fields into a place another resource can use. |
| Does Crossplane have a Terraform-style plan? | Not an identical plan. Use `crossplane composition render`, server-side dry runs, GitOps review, policy, and sandbox reconciliation. |

## Pattern 1: multiple resources in one YAML file

The simplest way to deploy multiple resources is a normal Kubernetes multi-document YAML file.

```yaml
apiVersion: ec2.aws.m.upbound.io/v1beta1
kind: VPC
metadata:
  name: app-vpc
  namespace: platform
  labels:
    network.platform.example.com/name: app
spec:
  forProvider:
    region: eu-west-1
    cidrBlock: 10.20.0.0/16
    enableDnsSupport: true
    enableDnsHostnames: true
    tags:
      Name: app-vpc
      ManagedBy: crossplane
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
---
apiVersion: ec2.aws.m.upbound.io/v1beta1
kind: Subnet
metadata:
  name: app-private-a
  namespace: platform
  labels:
    network.platform.example.com/name: app
    network.platform.example.com/tier: private
    network.platform.example.com/az: a
spec:
  forProvider:
    region: eu-west-1
    availabilityZone: eu-west-1a
    cidrBlock: 10.20.1.0/24
    vpcIdRef:
      name: app-vpc
    tags:
      Name: app-private-a
      ManagedBy: crossplane
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
---
apiVersion: ec2.aws.m.upbound.io/v1beta1
kind: Subnet
metadata:
  name: app-private-b
  namespace: platform
  labels:
    network.platform.example.com/name: app
    network.platform.example.com/tier: private
    network.platform.example.com/az: b
spec:
  forProvider:
    region: eu-west-1
    availabilityZone: eu-west-1b
    cidrBlock: 10.20.2.0/24
    vpcIdRef:
      name: app-vpc
    tags:
      Name: app-private-b
      ManagedBy: crossplane
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
```

What it does: creates a VPC and two subnets from a single YAML file. The subnets use `vpcIdRef.name` to reference the Kubernetes `VPC` managed resource instead of hard-coding the AWS VPC ID.

> [!IMPORTANT]
> Provider API groups, versions, and field names change by provider package and version. Validate examples with `kubectl api-resources`, `kubectl explain`, and the provider documentation installed in your cluster.

### Apply the file

```bash
kubectl apply --dry-run=server -f network.yaml
kubectl apply -f network.yaml
```

What it does: validates all documents against the installed provider schemas, then stores the desired state in Kubernetes.

## Pattern 2: fixed repeated resources in a Composition

If the number of resources is known, a Composition can explicitly declare each resource template.

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: network-two-private-subnets
spec:
  compositeTypeRef:
    apiVersion: platform.example.com/v1alpha1
    kind: Network
  mode: Pipeline
  pipeline:
    - step: patch-and-transform
      functionRef:
        name: function-patch-and-transform
      input:
        apiVersion: pt.fn.crossplane.io/v1beta1
        kind: Resources
        resources:
          - name: vpc
            base:
              apiVersion: ec2.aws.m.upbound.io/v1beta1
              kind: VPC
              spec:
                forProvider:
                  region: eu-west-1
                  cidrBlock: 10.20.0.0/16
                providerConfigRef:
                  name: default
                  kind: ClusterProviderConfig
            patches:
              - type: FromCompositeFieldPath
                fromFieldPath: spec.region
                toFieldPath: spec.forProvider.region
              - type: FromCompositeFieldPath
                fromFieldPath: spec.cidrBlock
                toFieldPath: spec.forProvider.cidrBlock

          - name: private-subnet-a
            base:
              apiVersion: ec2.aws.m.upbound.io/v1beta1
              kind: Subnet
              spec:
                forProvider:
                  region: eu-west-1
                  availabilityZone: eu-west-1a
                  cidrBlock: 10.20.1.0/24
                  vpcIdSelector:
                    matchControllerRef: true
                providerConfigRef:
                  name: default
                  kind: ClusterProviderConfig

          - name: private-subnet-b
            base:
              apiVersion: ec2.aws.m.upbound.io/v1beta1
              kind: Subnet
              spec:
                forProvider:
                  region: eu-west-1
                  availabilityZone: eu-west-1b
                  cidrBlock: 10.20.2.0/24
                  vpcIdSelector:
                    matchControllerRef: true
                providerConfigRef:
                  name: default
                  kind: ClusterProviderConfig
```

What it does: creates a reusable platform implementation that always produces one VPC and two subnets. `matchControllerRef: true` asks Crossplane to match a VPC created by the same XR instead of selecting any VPC in the namespace.

This is useful when the platform product shape is fixed, such as always creating two private subnets or one bucket plus required security resources.

## Pattern 3: Terraform-style loops with a Composition Function

Patch and Transform is good for fixed templates. For dynamic loops, use a function that supports programming logic, such as Go templating or KCL.

### Example XR input

```yaml
apiVersion: platform.example.com/v1alpha1
kind: Network
metadata:
  name: payments-network
  namespace: payments
spec:
  region: eu-west-1
  vpcCidr: 10.30.0.0/16
  subnets:
    - name: private-a
      availabilityZone: eu-west-1a
      cidrBlock: 10.30.1.0/24
      tier: private
    - name: private-b
      availabilityZone: eu-west-1b
      cidrBlock: 10.30.2.0/24
      tier: private
    - name: public-a
      availabilityZone: eu-west-1a
      cidrBlock: 10.30.101.0/24
      tier: public
```

What it does: lets the platform user request a variable number of subnets. This is the Crossplane input shape that feels closest to Terraform `for_each`.

### Install a templating function

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Function
metadata:
  name: function-go-templating
spec:
  package: xpkg.crossplane.io/crossplane-contrib/function-go-templating:v0.11.0
```

What it does: installs the Go templating composition function.

> [!IMPORTANT]
> Function packages have their own release cycles. Pin a version tested with your Crossplane release and verify the function's README before production use.

### Loop over subnets in Go templating

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: network-go-template
spec:
  compositeTypeRef:
    apiVersion: platform.example.com/v1alpha1
    kind: Network
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
              labels:
                network.platform.example.com/name: {{ $xr.metadata.name }}
            spec:
              forProvider:
                region: {{ $xr.spec.region }}
                cidrBlock: {{ $xr.spec.vpcCidr }}
                tags:
                  Name: {{ $xr.metadata.name }}-vpc
                  ManagedBy: crossplane
              providerConfigRef:
                name: default
                kind: ClusterProviderConfig
            {{ range $index, $subnet := $xr.spec.subnets }}
            ---
            apiVersion: ec2.aws.m.upbound.io/v1beta1
            kind: Subnet
            metadata:
              annotations:
                gotemplating.fn.crossplane.io/composition-resource-name: subnet-{{ $subnet.name }}
              labels:
                network.platform.example.com/name: {{ $xr.metadata.name }}
                network.platform.example.com/subnet-name: {{ $subnet.name }}
                network.platform.example.com/tier: {{ $subnet.tier }}
            spec:
              forProvider:
                region: {{ $xr.spec.region }}
                availabilityZone: {{ $subnet.availabilityZone }}
                cidrBlock: {{ $subnet.cidrBlock }}
                vpcIdSelector:
                  matchControllerRef: true
                tags:
                  Name: {{ $xr.metadata.name }}-{{ $subnet.name }}
                  Tier: {{ $subnet.tier }}
                  ManagedBy: crossplane
              providerConfigRef:
                name: default
                kind: ClusterProviderConfig
            {{ end }}
```

What it does: renders one VPC and as many Subnet resources as the XR's `spec.subnets` list contains. The `range` loop is the Terraform `for_each` equivalent.

## Pattern 4: reference generated resources from other resources

Crossplane providers commonly expose reference fields beside raw provider ID fields.

| Reference form | Example | Use it when |
| --- | --- | --- |
| Direct reference | `vpcIdRef.name: app-vpc` | The referenced Kubernetes resource has a known name. |
| Label selector | `vpcIdSelector.matchLabels` | You want to select by labels rather than name. |
| Controller reference | `matchControllerRef: true` | Resources are composed by the same XR. |
| Selector plus labels | `subnetIdSelector.matchLabels` | More than one resource is composed and you need a specific one. |
| Patch through XR status | `ToCompositeFieldPath` then `FromCompositeFieldPath` | A provider-generated value must become part of the platform API status or feed another template. |
| Connection secret | `writeConnectionSecretToRef` or composition connection details | Workloads need runtime connection data such as endpoints or passwords. |

### EC2 instance selecting one composed subnet

```yaml
apiVersion: ec2.aws.m.upbound.io/v1beta1
kind: Instance
metadata:
  name: app-server-a
  namespace: platform
spec:
  forProvider:
    region: eu-west-1
    ami: ami-0123456789abcdef0
    instanceType: t3.micro
    subnetIdSelector:
      matchControllerRef: true
      matchLabels:
        network.platform.example.com/subnet-name: private-a
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
```

What it does: deploys an EC2 instance into the subnet labeled `private-a` that belongs to the same XR. This avoids hard-coding the AWS subnet ID.

> [!NOTE]
> If a selector can match more than one resource, add labels that make the match unique. `matchControllerRef` is useful, but by itself it may be too broad when the same XR composes several subnets.

## Pattern 5: pass provider output through XR status

Sometimes a field is not available as a direct provider reference, or you want to expose it as platform API status.

Patch and Transform can patch values from a composed resource back to the XR with `ToCompositeFieldPath`, then later resources or users can read the XR status.

```yaml
patches:
  - type: ToCompositeFieldPath
    fromFieldPath: status.atProvider.id
    toFieldPath: status.vpcId
```

What it does: copies the observed VPC ID from the composed VPC into the composite resource's status.

Another resource template can consume XR fields with `FromCompositeFieldPath`:

```yaml
patches:
  - type: FromCompositeFieldPath
    fromFieldPath: status.vpcId
    toFieldPath: spec.forProvider.vpcId
```

What it does: copies a value from XR status into another composed resource.

> [!IMPORTANT]
> Status-driven patches are asynchronous. The first reconciliation may create the VPC, a later reconciliation observes its ID, and a later pass may apply that ID elsewhere. Prefer provider-native refs and selectors when they exist.

## Pattern 6: package a deployment as a platform API

For a professional reusable deployment, define a product-like API instead of asking users to submit raw VPC, subnet, route, and instance resources.

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
      cidrBlock: 10.30.1.0/24
      availabilityZone: eu-west-1a
    - name: private-b
      cidrBlock: 10.30.2.0/24
      availabilityZone: eu-west-1b
```

What it does: gives application teams a compact request while the platform team owns the implementation details in Composition Functions.

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

## Deployment workflow

1. Install Crossplane, providers, and functions.
2. Define an XRD that exposes the deployment inputs, such as region, CIDR, subnet list, and instance shape.
3. Write a Composition.
4. Use Patch and Transform for fixed resource sets, or Go templating/KCL for loops.
5. Use provider refs and selectors for dependencies such as VPC to Subnet and Subnet to Instance.
6. Use labels plus `matchControllerRef` when a composed resource must select one sibling resource from the same XR.
7. Use `ToCompositeFieldPath` for provider-generated values that should appear on XR status.
8. Render locally before applying.
9. Apply to a sandbox control plane.
10. Observe conditions, events, and external AWS state.
11. Promote through GitOps.

### Render before deploying

```bash
crossplane composition render \
  network-xr.yaml \
  network-composition.yaml \
  functions.yaml \
  --xrd network-xrd.yaml
```

What it does: renders the desired composed resources before the cluster reconciles them.

### Deploy and inspect

```bash
kubectl apply --dry-run=server -f network-xrd.yaml
kubectl apply -f network-xrd.yaml
kubectl apply -f network-composition.yaml
kubectl apply -f network-xr.yaml

kubectl describe network payments-network -n payments
kubectl get managed -n payments
kubectl get events -n payments --sort-by=.lastTimestamp
```

What it does: validates and applies the platform API, then inspects XR status, managed resources, and events.

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

- [Crossplane](README.md)
- [Crossplane compositions](compositions.md)
- [Managed resources and lifecycle](managed-resources-and-lifecycle.md)
- [AWS resource workflow](aws-resource-workflow.md)
- [Professional operating model](professional-operating-model.md)
- [Crossplane references](references.md)
- [Managed resources documentation](https://docs.crossplane.io/latest/managed-resources/managed-resources/)
- [Function Patch and Transform](https://docs.crossplane.io/latest/guides/function-patch-and-transform/)
- [Compositions documentation](https://docs.crossplane.io/latest/composition/compositions/)
- [Configuration packages documentation](https://docs.crossplane.io/latest/packages/configurations/)
- [Control plane projects documentation](https://docs.crossplane.io/latest/get-started/get-started-with-control-plane-projects/)
- [Go templating function](https://github.com/crossplane-contrib/function-go-templating)
- [KCL function](https://github.com/crossplane-contrib/function-kcl)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
