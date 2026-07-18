# Crossplane AWS resource workflow

## Purpose

Use this workflow to understand every component and interaction from installing Crossplane to deploying, observing, updating, and deleting AWS resources.

This page shows two routes:

- Direct managed-resource workflow: useful for learning and low-level platform implementation.
- Platform API workflow: the professional pattern for developer self-service.

## Components and tools

| Component or tool | Used for | Interaction with Crossplane |
| --- | --- | --- |
| AWS account | Hosts external resources such as S3, VPC, RDS, and EKS. | Provider controllers call AWS APIs using configured credentials. |
| EKS or `kind` | Runs the Kubernetes API and Crossplane pods. | Crossplane must run inside a Kubernetes cluster. |
| Helm | Installs Crossplane core. | Creates Crossplane deployments, CRDs, and package controllers. |
| `kubectl` | Applies and inspects Kubernetes objects. | Sends desired state to Kubernetes; it does not call AWS directly. |
| Crossplane core | Manages packages, XRDs, XRs, Compositions, Functions, and Operations. | Watches Crossplane API objects and coordinates composition pipelines. |
| Provider package | Installs AWS APIs and controllers. | Adds managed-resource APIs and runs provider pods. |
| ProviderConfig | Tells providers how to authenticate. | Provider pods read it before calling AWS. |
| Managed resource | Kubernetes object representing one AWS resource. | Provider reconciles it to an external AWS object. |
| XRD | Defines a custom platform API. | Kubernetes serves the API after Crossplane installs it. |
| Composition | Implements an XR with composed resources. | Crossplane runs function pipelines to produce managed resources. |
| Function | Generates, patches, or transforms desired resources. | Called by Crossplane during composition or operation execution. |
| Argo CD or Flux | GitOps delivery. | Applies Crossplane manifests from Git and reports sync state. |
| AWS IAM | Controls AWS blast radius. | Provider credentials need enough permissions to reconcile but not broad admin. |
| CloudTrail and metrics | Audit and operations. | Confirm AWS API calls and controller health. |

## Workflow overview

```text
1. Bootstrap Kubernetes
2. Install Crossplane
3. Install AWS provider packages
4. Configure provider identity
5. Validate installed APIs
6. Deploy direct managed resources or platform APIs
7. Observe status and AWS state
8. Manage updates, drift, import, and deletion
9. Promote through GitOps
```

## Step 1: bootstrap Kubernetes

For a local lab:

```bash
kind create cluster --name crossplane-lab
kubectl cluster-info
kubectl get nodes
```

What it does: creates a local Kubernetes cluster for learning.

For production AWS:

```bash
eksctl create cluster \
  --name platform-management \
  --region eu-west-1 \
  --nodes 3
```

What it does: creates an EKS management cluster. In real organizations this is often managed by Terraform, AWS CDK, CloudFormation, or landing-zone tooling.

Interaction: Crossplane does not create this first cluster because Crossplane needs Kubernetes before it can run.

## Step 2: install Crossplane

```bash
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update

helm install crossplane \
  --namespace crossplane-system \
  --create-namespace \
  crossplane-stable/crossplane
```

What it does: installs Crossplane core into `crossplane-system`.

Check readiness:

```bash
kubectl get pods -n crossplane-system
kubectl get crds | grep crossplane
```

Interaction: Crossplane adds package, composition, function, managed-resource, and operation APIs to the cluster.

## Step 3: install AWS provider packages

Create `provider-aws-s3.yaml`:

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

Apply:

```bash
kubectl apply -f provider-aws-s3.yaml
kubectl get providers.pkg.crossplane.io -w
kubectl get providerrevisions.pkg.crossplane.io
```

What it does: installs the S3 provider package and starts provider controller pods.

Interaction:

1. Kubernetes stores the `Provider` object.
2. Crossplane package manager pulls the provider OCI package.
3. Crossplane creates provider revisions and runtime resources.
4. The provider adds S3 managed-resource APIs.
5. The provider pod starts watching S3 managed resources.

## Step 4: optionally limit the provider API surface

Large providers can expose many resource types. Use activation policies when supported by the provider and Crossplane version.

List installed ManagedResourceDefinitions first:

```bash
kubectl get mrds | grep -i s3
```

What it does: shows the exact MRD names to use in the activation policy for the provider package installed in your cluster.

```yaml
apiVersion: apiextensions.crossplane.io/v1alpha1
kind: ManagedResourceActivationPolicy
metadata:
  name: activate-s3-bucket-types
spec:
  activate:
    - buckets.s3.aws.m.upbound.io
    - bucketpublicaccessblocks.s3.aws.m.upbound.io
```

What it does: activates only selected managed-resource definitions instead of every API shipped by the provider.

Interaction: Crossplane keeps unused managed-resource definitions inactive, reducing API surface and cluster overhead.

> [!NOTE]
> Managed Resource Activation Policies are alpha in Crossplane v2.0+ and require provider support for safe start. Replace the example names with the exact MRD names from `kubectl get mrds`.

## Step 5: configure AWS identity

### Temporary local credentials

Create `aws-credentials.ini` for a sandbox-only lab:

```ini
[default]
aws_access_key_id = REPLACE_WITH_TEMPORARY_LAB_KEY
aws_secret_access_key = REPLACE_WITH_TEMPORARY_LAB_SECRET
```

Create the Secret:

```bash
kubectl create secret generic aws-secret \
  --namespace=crossplane-system \
  --from-file=creds=./aws-credentials.ini
```

What it does: gives the provider a credential file through a Kubernetes Secret.

> [!WARNING]
> Static access keys are for temporary labs only. Use EKS Pod Identity, IRSA, or another workload identity pattern for production.

### ProviderConfig declaration

Create `provider-config.yaml`:

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

Apply:

```bash
kubectl apply -f provider-config.yaml
```

What it does: creates a cluster-wide AWS provider config named `default`.

Interaction: When the provider reconciles an S3 managed resource, it follows `providerConfigRef`, loads credentials from this config, then calls AWS.

### Production EKS identity

For EKS, prefer EKS Pod Identity when the provider image and AWS SDK path support it. IRSA remains appropriate when your controls or compatibility require it.

EKS Pod Identity interaction:

```text
Provider pod ServiceAccount
        |
EKS Pod Identity association
        |
EKS Auth and Pod Identity Agent
        |
Temporary IAM role credentials
        |
AWS APIs
```

IRSA interaction:

```text
Provider pod ServiceAccount annotation
        |
Projected service account OIDC token
        |
AWS STS AssumeRoleWithWebIdentity
        |
Temporary IAM role credentials
        |
AWS APIs
```

## Step 6: validate installed APIs

```bash
kubectl api-resources | grep -i s3
kubectl explain bucket.s3.aws.m.upbound.io.spec.forProvider
kubectl explain bucketpublicaccessblock.s3.aws.m.upbound.io.spec.forProvider
```

What it does: confirms the provider installed the expected resource kinds and shows the schema supported by this cluster.

Interaction: Kubernetes API discovery reflects the APIs added by provider installation.

## Step 7: deploy a direct AWS managed resource

Create `bucket.yaml`:

```yaml
apiVersion: s3.aws.m.upbound.io/v1beta1
kind: Bucket
metadata:
  name: xp-lab-123456789012-001
  namespace: default
  labels:
    app.kubernetes.io/managed-by: crossplane
    platform.example.com/environment: lab
  annotations:
    crossplane.io/external-name: xp-lab-123456789012-001
spec:
  forProvider:
    region: eu-west-1
    tags:
      Environment: lab
      ManagedBy: crossplane
      Owner: platform-team
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
  managementPolicies:
    - "*"
```

Validate and apply:

```bash
kubectl apply --dry-run=server -f bucket.yaml
kubectl apply -f bucket.yaml
```

What it does: creates the Kubernetes-side S3 bucket managed resource.

Interaction:

1. Kubernetes accepts the object.
2. S3 provider sees a new `Bucket`.
3. Provider reads the `ClusterProviderConfig`.
4. Provider calls AWS S3 to observe whether the bucket exists.
5. Provider creates or adopts the external bucket according to external-name and policy behavior.
6. Provider writes `status.conditions`, `status.atProvider`, and events.

## Step 8: add a dependent managed resource

Create `bucket-public-access.yaml`:

```yaml
apiVersion: s3.aws.m.upbound.io/v1beta1
kind: BucketPublicAccessBlock
metadata:
  name: xp-lab-123456789012-001-public-access
  namespace: default
spec:
  forProvider:
    region: eu-west-1
    bucketRef:
      name: xp-lab-123456789012-001
    blockPublicAcls: true
    blockPublicPolicy: true
    ignorePublicAcls: true
    restrictPublicBuckets: true
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
  managementPolicies:
    - "*"
```

Apply:

```bash
kubectl apply --dry-run=server -f bucket-public-access.yaml
kubectl apply -f bucket-public-access.yaml
```

What it does: adds public-access blocking to the S3 bucket.

Interaction: `bucketRef.name` lets the provider resolve the bucket resource rather than hard-coding the bucket identifier everywhere.

## Step 9: observe status and AWS state

```bash
kubectl get buckets.s3.aws.m.upbound.io -n default
kubectl describe bucket.s3.aws.m.upbound.io xp-lab-123456789012-001 -n default
kubectl get events -n default --sort-by=.lastTimestamp
```

What it does: reads Kubernetes-side readiness, provider messages, and warning events.

Verify AWS:

```bash
aws s3api head-bucket --bucket xp-lab-123456789012-001
aws s3api get-bucket-tagging --bucket xp-lab-123456789012-001
aws s3api get-public-access-block --bucket xp-lab-123456789012-001
```

What it does: confirms the external AWS resources match the desired state.

## Step 10: manage updates

Edit `bucket.yaml`:

```yaml
spec:
  forProvider:
    region: eu-west-1
    tags:
      Environment: lab
      ManagedBy: crossplane
      Owner: platform-team
      CostCenter: platform-learning
```

Apply:

```bash
kubectl apply -f bucket.yaml
```

What it does: changes desired tags in Kubernetes.

Interaction: The provider notices the spec change, updates the external AWS resource if the field is supported and mutable, then updates status.

## Step 11: test drift correction

Change AWS manually:

```bash
aws s3api put-bucket-tagging \
  --bucket xp-lab-123456789012-001 \
  --tagging 'TagSet=[{Key=ManagedBy,Value=manual},{Key=Environment,Value=lab}]'
```

Request reconciliation:

```bash
kubectl annotate bucket.s3.aws.m.upbound.io xp-lab-123456789012-001 \
  -n default \
  crossplane.io/reconcile-requested-at="$(date +%s)" \
  --overwrite
```

What it does: creates drift, then asks the provider to reconcile.

Interaction: The provider observes the external resource, compares it to desired state, and updates fields it owns and supports.

## Step 12: pause reconciliation during maintenance

```bash
kubectl annotate bucket.s3.aws.m.upbound.io xp-lab-123456789012-001 \
  -n default \
  crossplane.io/paused="true" \
  --overwrite
```

What it does: pauses reconciliation for a single managed resource.

Resume:

```bash
kubectl annotate bucket.s3.aws.m.upbound.io xp-lab-123456789012-001 \
  -n default \
  crossplane.io/paused-
```

What it does: removes the pause annotation so the provider can reconcile again.

## Step 13: expose a professional platform API

Direct managed resources are useful, but professional self-service normally starts with an XR.

Developer request:

```yaml
apiVersion: platform.example.com/v1alpha1
kind: SecureBucket
metadata:
  name: payments-artifacts
  namespace: payments
spec:
  region: eu-west-1
  retentionDays: 90
```

What it does: asks for a storage product. The developer does not need to know S3 managed-resource schemas.

Platform XRD:

```yaml
apiVersion: apiextensions.crossplane.io/v2
kind: CompositeResourceDefinition
metadata:
  name: securebuckets.platform.example.com
spec:
  scope: Namespaced
  group: platform.example.com
  names:
    kind: SecureBucket
    plural: securebuckets
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
                retentionDays:
                  type: integer
                  minimum: 30
                  maximum: 365
              required:
                - region
                - retentionDays
```

What it does: declares the user-facing API contract.

Composition shape:

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: securebucket-s3
spec:
  compositeTypeRef:
    apiVersion: platform.example.com/v1alpha1
    kind: SecureBucket
  mode: Pipeline
  pipeline:
    - step: render-secure-bucket
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
                forProvider:
                  region: eu-west-1
                  tags:
                    ManagedBy: crossplane
                    Product: secure-bucket
                providerConfigRef:
                  name: default
                  kind: ClusterProviderConfig
            patches:
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.name
                toFieldPath: metadata.name
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.namespace
                toFieldPath: metadata.namespace
              - type: FromCompositeFieldPath
                fromFieldPath: spec.region
                toFieldPath: spec.forProvider.region
```

What it does: shows the declaration pattern for a Composition. Production compositions usually also generate public-access blocks, encryption, versioning, lifecycle rules, logging, and required tags.

Render before rollout:

```bash
crossplane composition render \
  securebucket-xr.yaml \
  securebucket-composition.yaml \
  functions.yaml \
  --xrd securebucket-xrd.yaml
```

What it does: runs the function pipeline locally and shows generated resources before the cluster reconciles them.

## Step 14: manage deletion

Delete dependent resources first when working directly:

```bash
kubectl delete -f bucket-public-access.yaml
kubectl delete -f bucket.yaml
```

What it does: asks Crossplane to delete the managed resources and the external AWS resources.

Watch:

```bash
kubectl get buckets.s3.aws.m.upbound.io -n default -w
kubectl get events -n default --sort-by=.lastTimestamp
```

Interaction:

1. Kubernetes marks the resource for deletion.
2. Finalizer keeps the Kubernetes object present.
3. Provider deletes or detaches the external AWS resource.
4. Provider removes the finalizer.
5. Kubernetes removes the object.

> [!WARNING]
> If deletion hangs, inspect finalizers, provider logs, AWS dependencies, and IAM delete permissions before removing finalizers.

## Step 15: operate through GitOps

Recommended GitOps order:

1. Crossplane core.
2. Providers and Functions.
3. ProviderConfigs and runtime configs.
4. XRDs.
5. Compositions.
6. XRs or direct managed resources.

Interaction:

```text
Pull request
    |
CI validation and composition render
    |
Argo CD or Flux sync
    |
Kubernetes API desired state
    |
Crossplane reconciliation
    |
AWS resources and status feedback
```

GitOps owns whether manifests are present in the cluster. Crossplane owns whether external resources match those manifests.

## Related links

- [Crossplane](README.md)
- [Professional operating model](professional-operating-model.md)
- [Managed resources and lifecycle](managed-resources-and-lifecycle.md)
- [Providers and authentication](providers-and-authentication.md)
- [Crossplane compositions](compositions.md)
- [Crossplane troubleshooting](troubleshooting.md)
- [Crossplane references](references.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
