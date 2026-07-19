# Crossplane deployment patterns and references

## Purpose

Use this page to understand how to deploy multiple related resources with Crossplane, how to model Terraform-style `count` and `for_each`, and how resources reference each other when one resource needs values from another.

Crossplane can deploy multiple resources together, but it does not work exactly like Terraform. Terraform builds a plan-time expression graph. Crossplane stores desired state in Kubernetes, then controllers reconcile asynchronously. References are resolved by controllers through Kubernetes objects, labels, selectors, status, and connection details.

## Quick answer

| Terraform question | Crossplane answer |
| --- | --- |
| Can I put many resources in one file? | Yes. Use a multi-document YAML file separated with `---`. |
| Is there a native `count` or `for_each` in plain YAML? | No. Plain YAML repeats resources explicitly. |
| What is the Crossplane equivalent of reusable infrastructure? | XRDs, XRs, Compositions, Functions, and Configuration packages. |
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
- [Go templating function](https://github.com/crossplane-contrib/function-go-templating)
- [KCL function](https://github.com/crossplane-contrib/function-kcl)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
