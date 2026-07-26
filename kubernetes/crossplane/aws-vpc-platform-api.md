# AWS VPC platform API with Crossplane

## Purpose

Show how one Crossplane XR can request multiple deployable AWS networking resources: a VPC, private subnets, a network ACL, ACL rules, a route table, route table associations, and VPC endpoints.

> [!WARNING]
> This example can create billable AWS resources. Use a sandbox account and verify provider schemas, IAM permissions, naming, quotas, endpoint service availability, and deletion policy before using it.

## What this example creates

The user applies one `PlatformNetwork` XR. Crossplane uses the matching Composition to create these AWS managed resources:

| Composed resource | AWS purpose |
| --- | --- |
| `VPC` | Main network boundary. |
| `Subnet` x2 | Private subnets in two availability zones. |
| `NetworkACL` | Stateless network ACL for the VPC. |
| `NetworkACLRule` x2 | Allow internal ingress and outbound egress. |
| `RouteTable` | Route table associated with the private subnets. |
| `RouteTableAssociation` x2 | Associates each subnet with the route table. |
| `VPCEndpoint` x2 | Gateway endpoints for S3 and DynamoDB. |
| `VPCEndpointRouteTableAssociation` x2 | Associates the gateway endpoints with the route table. |

## Install the AWS EC2 provider

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: upbound-provider-aws-ec2
spec:
  package: xpkg.upbound.io/upbound/provider-aws-ec2:v2.6.1
```

Apply it:

```bash
kubectl apply -f provider-aws-ec2.yaml
kubectl get providers
```

What it does: installs the AWS EC2 provider package, which includes namespaced managed resources such as `VPC`, `Subnet`, `NetworkACL`, `RouteTable`, and `VPCEndpoint`.

## Define the PlatformNetwork XRD

```yaml
apiVersion: apiextensions.crossplane.io/v2
kind: CompositeResourceDefinition
metadata:
  name: platformnetworks.platform.example.org
spec:
  group: platform.example.org
  scope: Namespaced
  names:
    kind: PlatformNetwork
    plural: platformnetworks
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
                - eu-central-1
                - us-east-1
              cidrBlock:
                type: string
              environment:
                type: string
                enum:
                - dev
                - staging
                - prod
              privateSubnetA:
                type: object
                properties:
                  availabilityZone:
                    type: string
                  cidrBlock:
                    type: string
                required:
                - availabilityZone
                - cidrBlock
              privateSubnetB:
                type: object
                properties:
                  availabilityZone:
                    type: string
                  cidrBlock:
                    type: string
                required:
                - availabilityZone
                - cidrBlock
              deletionPolicy:
                type: string
                enum:
                - Delete
                - Orphan
                default: Delete
            required:
            - region
            - cidrBlock
            - environment
            - privateSubnetA
            - privateSubnetB
```

What it does: defines the API contract. Users can request a network without knowing the low-level AWS provider fields for each composed resource.

## Define the AWS network Composition

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: platformnetwork-aws-private
  labels:
    provider: aws
    service: ec2
    network: private
spec:
  compositeTypeRef:
    apiVersion: platform.example.org/v1alpha1
    kind: PlatformNetwork
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
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              cidrBlock: 10.0.0.0/16
              enableDnsSupport: true
              enableDnsHostnames: true
              tags:
                managed-by: crossplane
                platform-api: platformnetwork
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.cidrBlock
          toFieldPath: spec.forProvider.cidrBlock
        - type: FromCompositeFieldPath
          fromFieldPath: spec.environment
          toFieldPath: spec.forProvider.tags.environment
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: private-subnet-a
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: Subnet
          metadata:
            labels:
              network.platform.example.org/subnet: private-a
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              availabilityZone: eu-west-1a
              cidrBlock: 10.0.1.0/24
              mapPublicIpOnLaunch: false
              vpcIdSelector:
                matchControllerRef: true
              tags:
                tier: private
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.privateSubnetA.availabilityZone
          toFieldPath: spec.forProvider.availabilityZone
        - type: FromCompositeFieldPath
          fromFieldPath: spec.privateSubnetA.cidrBlock
          toFieldPath: spec.forProvider.cidrBlock
        - type: FromCompositeFieldPath
          fromFieldPath: spec.environment
          toFieldPath: spec.forProvider.tags.environment
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: private-subnet-b
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: Subnet
          metadata:
            labels:
              network.platform.example.org/subnet: private-b
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              availabilityZone: eu-west-1b
              cidrBlock: 10.0.2.0/24
              mapPublicIpOnLaunch: false
              vpcIdSelector:
                matchControllerRef: true
              tags:
                tier: private
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.privateSubnetB.availabilityZone
          toFieldPath: spec.forProvider.availabilityZone
        - type: FromCompositeFieldPath
          fromFieldPath: spec.privateSubnetB.cidrBlock
          toFieldPath: spec.forProvider.cidrBlock
        - type: FromCompositeFieldPath
          fromFieldPath: spec.environment
          toFieldPath: spec.forProvider.tags.environment
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: network-acl
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: NetworkACL
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              vpcIdSelector:
                matchControllerRef: true
              subnetIdSelector:
                matchControllerRef: true
              tags:
                managed-by: crossplane
                tier: private
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.environment
          toFieldPath: spec.forProvider.tags.environment
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: network-acl-ingress
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: NetworkACLRule
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              networkAclIdSelector:
                matchControllerRef: true
              egress: false
              protocol: "-1"
              ruleAction: allow
              ruleNumber: 100
              cidrBlock: 10.0.0.0/16
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.cidrBlock
          toFieldPath: spec.forProvider.cidrBlock
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: network-acl-egress
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: NetworkACLRule
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              networkAclIdSelector:
                matchControllerRef: true
              egress: true
              protocol: "-1"
              ruleAction: allow
              ruleNumber: 100
              cidrBlock: 0.0.0.0/0
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: private-route-table
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: RouteTable
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              vpcIdSelector:
                matchControllerRef: true
              tags:
                tier: private
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.environment
          toFieldPath: spec.forProvider.tags.environment
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: private-route-table-association-a
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: RouteTableAssociation
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              routeTableIdSelector:
                matchControllerRef: true
              subnetIdSelector:
                matchControllerRef: true
                matchLabels:
                  network.platform.example.org/subnet: private-a
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: private-route-table-association-b
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: RouteTableAssociation
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              routeTableIdSelector:
                matchControllerRef: true
              subnetIdSelector:
                matchControllerRef: true
                matchLabels:
                  network.platform.example.org/subnet: private-b
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: s3-endpoint
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: VPCEndpoint
          metadata:
            labels:
              network.platform.example.org/endpoint: s3
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              vpcEndpointType: Gateway
              serviceName: com.amazonaws.eu-west-1.s3
              vpcIdSelector:
                matchControllerRef: true
              tags:
                service: s3
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.serviceName
          transforms:
          - type: string
            string:
              type: Format
              fmt: com.amazonaws.%s.s3
        - type: FromCompositeFieldPath
          fromFieldPath: spec.environment
          toFieldPath: spec.forProvider.tags.environment
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: dynamodb-endpoint
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: VPCEndpoint
          metadata:
            labels:
              network.platform.example.org/endpoint: dynamodb
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              vpcEndpointType: Gateway
              serviceName: com.amazonaws.eu-west-1.dynamodb
              vpcIdSelector:
                matchControllerRef: true
              tags:
                service: dynamodb
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.serviceName
          transforms:
          - type: string
            string:
              type: Format
              fmt: com.amazonaws.%s.dynamodb
        - type: FromCompositeFieldPath
          fromFieldPath: spec.environment
          toFieldPath: spec.forProvider.tags.environment
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: s3-endpoint-route-table-association
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: VPCEndpointRouteTableAssociation
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              routeTableIdSelector:
                matchControllerRef: true
              vpcEndpointIdSelector:
                matchControllerRef: true
                matchLabels:
                  network.platform.example.org/endpoint: s3
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
      - name: dynamodb-endpoint-route-table-association
        base:
          apiVersion: ec2.aws.m.upbound.io/v1beta1
          kind: VPCEndpointRouteTableAssociation
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              routeTableIdSelector:
                matchControllerRef: true
              vpcEndpointIdSelector:
                matchControllerRef: true
                matchLabels:
                  network.platform.example.org/endpoint: dynamodb
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.region
          toFieldPath: spec.forProvider.region
        - type: FromCompositeFieldPath
          fromFieldPath: spec.deletionPolicy
          toFieldPath: spec.deletionPolicy
```

What it does: creates a fixed two-AZ private network pattern from one XR. The `matchControllerRef` selectors bind composed resources that belong to the same XR, so subnets can find the composed VPC and associations can find the composed route table.

> [!IMPORTANT]
> Provider field names can change between AWS provider versions. Before using this in a real cluster, check the installed CRDs with commands such as `kubectl explain vpc.spec.forProvider`, `kubectl explain networkacl.spec.forProvider`, and `kubectl explain vpcendpoint.spec.forProvider`.

## Call the API with a PlatformNetwork XR

```yaml
apiVersion: platform.example.org/v1alpha1
kind: PlatformNetwork
metadata:
  namespace: payments
  name: payments-network
spec:
  region: eu-west-1
  cidrBlock: 10.40.0.0/16
  environment: prod
  privateSubnetA:
    availabilityZone: eu-west-1a
    cidrBlock: 10.40.1.0/24
  privateSubnetB:
    availabilityZone: eu-west-1b
    cidrBlock: 10.40.2.0/24
  deletionPolicy: Orphan
  crossplane:
    compositionRef:
      name: platformnetwork-aws-private
```

Apply it:

```bash
kubectl apply -f platformnetwork-payments.yaml
kubectl get platformnetworks -n payments
crossplane beta trace platformnetwork.platform.example.org/payments-network -n payments
```

What it does: creates one XR that represents the whole AWS networking stack. Crossplane composes all dependent resources and reports status through the `PlatformNetwork`.

## Inspect the composed AWS resources

```bash
kubectl get vpcs,subnets,networkacls,networkaclrules,routetables,routetableassociations,vpcendpoints -n payments
kubectl describe platformnetwork payments-network -n payments
crossplane beta trace platformnetwork.platform.example.org/payments-network -n payments
```

What it does: verifies that the XR created a resource tree and shows which composed AWS resources are not ready if the stack is still reconciling.

## How this differs from a Terraform VPC module

With Terraform, the caller would pass variables into a VPC module, review `terraform plan`, and run `terraform apply`. Terraform stores the resource mapping in state.

With Crossplane:

- The XRD defines the network API.
- The XR is the persisted network request.
- The Composition is the implementation.
- AWS resources are Kubernetes managed resources.
- Crossplane keeps reconciling after the first apply.

This is useful when platform teams want Kubernetes-native self-service instead of exposing raw Terraform module internals to every application team.

## Cleanup

```bash
kubectl delete platformnetwork payments-network -n payments
```

What it does: deletes the XR. Crossplane then deletes or orphans the composed AWS resources according to the `deletionPolicy` patched into each managed resource.

## Related links

- [Crossplane XRDs](https://docs.crossplane.io/latest/composition/composite-resource-definitions/)
- [Crossplane composite resources](https://docs.crossplane.io/latest/composition/composite-resources/)
- [Crossplane Compositions](https://docs.crossplane.io/latest/composition/compositions/)
- [Function Patch and Transform](https://docs.crossplane.io/latest/guides/function-patch-and-transform/)
- [Crossplane providers](https://docs.crossplane.io/latest/packages/providers/)
- [Upbound AWS EC2 provider resources](https://marketplace.upbound.io/providers/upbound/provider-aws-ec2/v2.6.1?tab=managedResources)
- [Crossplane component model](component-model.md)
- [Crossplane compositions](compositions.md)
- [Deployment patterns and references](deployment-patterns-and-references.md)
- [Back to Crossplane index](README.md)
- [Back to root index](../../README.md)
