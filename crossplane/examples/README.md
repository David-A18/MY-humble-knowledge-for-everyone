# Crossplane examples

## Purpose

Provide practical AWS-focused Crossplane examples for installation, provider setup, direct S3 managed resources, XRDs, Compositions, and composite resources.

> [!WARNING]
> These examples can create billable AWS resources. Use a sandbox account, unique names, least-privilege credentials, and a cleanup plan.

## Prerequisites

- A Kubernetes cluster supported by the Crossplane version you install.
- Helm `v3.2.0` or later.
- `kubectl` configured for the target cluster.
- AWS credentials with permission to create and delete the example resources.
- Crossplane CLI if you want to use `crossplane beta trace` or `crossplane composition render`.

## Example walkthroughs

| Example | What it shows |
| --- | --- |
| [AWS VPC platform API](aws-vpc-platform-api.md) | One `PlatformNetwork` XR that composes a VPC, subnets, network ACLs, route table associations, and VPC endpoints. |

## Install Crossplane

```bash
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update
helm install crossplane crossplane-stable/crossplane \
  --namespace crossplane-system \
  --create-namespace
```

What it does: installs the Crossplane control plane into the `crossplane-system` namespace.

### Verify Crossplane

```bash
kubectl -n crossplane-system get pods
kubectl get crds | findstr crossplane
```

What it does: confirms the Crossplane pods are running and Crossplane CRDs are installed.

## Install the AWS S3 provider

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: crossplane-contrib-provider-aws-s3
spec:
  package: xpkg.crossplane.io/crossplane-contrib/provider-aws-s3:v2.0.0
```

Apply it:

```bash
kubectl apply -f provider-aws-s3.yaml
kubectl get providers
```

What it does: installs the AWS S3 provider package. The provider installs APIs for S3 managed resources and starts a controller that reconciles those resources.

Expected provider health after installation completes:

```text
NAME                              INSTALLED   HEALTHY
crossplane-contrib-provider-aws-s3 True        True
```

## Configure AWS credentials

Create an AWS credentials file:

```ini
[default]
aws_access_key_id = AKIAEXAMPLE
aws_secret_access_key = example-secret-key
```

Create the Kubernetes secret:

```bash
kubectl create secret generic aws-secret \
  -n crossplane-system \
  --from-file=creds=./aws-credentials.txt
```

What it does: stores AWS credentials where the provider can read them.

Create a cluster-wide provider configuration:

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

Apply it:

```bash
kubectl apply -f providerconfig.yaml
```

What it does: tells the AWS provider to use the `aws-secret` credentials for resources that reference `default`.

## Create a direct managed S3 bucket

```yaml
apiVersion: s3.aws.m.upbound.io/v1beta1
kind: Bucket
metadata:
  namespace: default
  generateName: app-logs-
spec:
  forProvider:
    region: eu-west-1
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
```

Apply it:

```bash
kubectl apply -f bucket.yaml
kubectl get buckets -n default
kubectl describe bucket -n default <bucket-name>
```

What it does: creates a namespaced Crossplane managed resource. The provider reconciles it into an AWS S3 bucket.

> [!TIP]
> If the provider supports it, use the `crossplane.io/external-name` annotation when you need the external cloud resource to have a specific name.

## Define an AppBucket XRD

```yaml
apiVersion: apiextensions.crossplane.io/v2
kind: CompositeResourceDefinition
metadata:
  name: appbuckets.platform.example.org
spec:
  group: platform.example.org
  scope: Namespaced
  names:
    kind: AppBucket
    plural: appbuckets
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
                description: AWS region where the bucket should be created.
                enum:
                - eu-west-1
                - eu-central-1
                - us-east-1
              environment:
                type: string
                description: Environment tag for the AWS bucket.
                enum:
                - dev
                - staging
                - prod
              deletionPolicy:
                type: string
                description: Whether Crossplane deletes or orphans the AWS bucket when the XR is deleted.
                enum:
                - Delete
                - Orphan
                default: Delete
            required:
            - region
            - environment
```

Apply it:

```bash
kubectl apply -f xrd-appbucket.yaml
kubectl get xrd
```

What it does: creates a Kubernetes API named `appbuckets.platform.example.org`. Users can now create `AppBucket` resources.

## Install Function Patch and Transform

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Function
metadata:
  name: function-patch-and-transform
spec:
  package: xpkg.crossplane.io/crossplane-contrib/function-patch-and-transform:v0.8.2
```

Apply it:

```bash
kubectl apply -f function-patch-and-transform.yaml
kubectl get functions
```

What it does: installs the function used by the Composition pipeline to produce composed resources.

## Define a Composition for AppBucket

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: appbucket-s3-standard
  labels:
    provider: aws
    service: s3
    tier: standard
spec:
  compositeTypeRef:
    apiVersion: platform.example.org/v1alpha1
    kind: AppBucket
  mode: Pipeline
  pipeline:
  - step: create-s3-bucket
    functionRef:
      name: function-patch-and-transform
    input:
      apiVersion: pt.fn.crossplane.io/v1beta1
      kind: Resources
      resources:
      - name: bucket
        base:
          apiVersion: s3.aws.m.upbound.io/v1beta1
          kind: Bucket
          spec:
            deletionPolicy: Delete
            providerConfigRef:
              name: default
              kind: ClusterProviderConfig
            forProvider:
              region: eu-west-1
              tags:
                managed-by: crossplane
                platform-api: appbucket
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
```

Apply it:

```bash
kubectl apply -f composition-appbucket-s3-standard.yaml
kubectl get compositions
```

What it does: connects the `AppBucket` API to an AWS S3 `Bucket` managed resource, injects platform tags, maps the user-selected environment tag, and applies the requested deletion policy.

## Call the platform API with an XR

```yaml
apiVersion: platform.example.org/v1alpha1
kind: AppBucket
metadata:
  namespace: payments
  name: receipts
spec:
  region: eu-west-1
  environment: prod
  deletionPolicy: Orphan
  crossplane:
    compositionRef:
      name: appbucket-s3-standard
```

Apply it:

```bash
kubectl apply -f appbucket-receipts.yaml
kubectl get appbuckets -n payments
kubectl describe appbucket receipts -n payments
kubectl get buckets -n payments
```

What it does: creates a composite resource in the `payments` namespace. Crossplane reads the XR, uses the selected AWS S3 Composition, creates the composed S3 Bucket managed resource, and reports readiness on the XR.

Trace the resource tree:

```bash
crossplane beta trace appbucket.platform.example.org/receipts -n payments
```

What it does: shows the XR and the resources Crossplane composed for it, making it easier to debug readiness problems.

## Render a Composition locally

```bash
crossplane composition render appbucket-receipts.yaml composition-appbucket-s3-standard.yaml function-patch-and-transform.yaml
```

What it does: runs the Composition function locally and prints the resources the Composition would generate. The Crossplane CLI uses Docker for function execution by default.

## Cleanup

Delete the user-facing XR first:

```bash
kubectl delete appbucket receipts -n payments
```

Then confirm the composed managed resource and external resource are gone:

```bash
kubectl get buckets -n payments
kubectl get events -n payments --sort-by=.lastTimestamp
```

> [!WARNING]
> Do not remove a provider before deleting the managed resources it owns. Removing the provider first can leave external resources orphaned and unmanaged.

## Related links

- [Crossplane managed resources](https://docs.crossplane.io/latest/managed-resources/)
- [Crossplane providers](https://docs.crossplane.io/latest/packages/providers/)
- [Crossplane Compositions](https://docs.crossplane.io/latest/composition/compositions/)
- [Crossplane CLI command reference](https://docs.crossplane.io/cli/latest/command-reference/)
- [XRDs and XRs](../xrd-and-xr/README.md)
- [Compositions](../compositions/README.md)
- [Back to Crossplane index](../README.md)
- [Back to root index](../../README.md)
