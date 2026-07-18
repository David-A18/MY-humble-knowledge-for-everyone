# Crossplane local AWS S3 lab

## Purpose

Use this hands-on lab to install Crossplane in a local Kubernetes cluster, install an AWS S3 provider, create a real S3 bucket, observe reconciliation, test drift correction, and clean up safely.

This lab is intentionally provider-specific. For production AWS architecture, use [Crossplane on AWS](../../cross-topic-guides/crossplane-on-aws.md).

## Prerequisites

- A sandbox AWS account.
- AWS CLI authenticated to the sandbox account.
- `kubectl`, Helm 3, Docker, and `kind`.
- A budget or cost guardrail for the sandbox account.
- No production data and no production credentials.

> [!WARNING]
> This lab creates real AWS resources. Use a sandbox account, least-privilege temporary credentials, and a unique bucket name. Do not commit credentials or generated manifests containing secrets.

## Verify AWS identity

```bash
aws sts get-caller-identity
export AWS_REGION=eu-west-1
```

What it does: confirms which AWS account the lab will use and sets the target region.

## Create a local cluster

```bash
kind create cluster --name crossplane-lab
kubectl cluster-info
kubectl get nodes
```

What it does: creates a local Kubernetes cluster for Crossplane and confirms that `kubectl` can reach it.

## Install Crossplane

```bash
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update

helm install crossplane \
  --namespace crossplane-system \
  --create-namespace \
  crossplane-stable/crossplane
```

What it does: installs Crossplane core into the `crossplane-system` namespace.

### Wait for readiness

```bash
kubectl get pods -n crossplane-system -w
```

What it does: waits for the Crossplane pods to become ready.

## Install the AWS S3 provider

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

Apply it:

```bash
kubectl apply -f provider-aws-s3.yaml
kubectl get providers.pkg.crossplane.io -w
```

What it does: installs the S3 provider and watches for `INSTALLED=True` and `HEALTHY=True`.

> [!IMPORTANT]
> Provider versions and schemas change independently from Crossplane core. Verify the current provider package and resource schema before reusing this lab later.

## Create temporary AWS credentials

Create `aws-credentials.ini`:

```ini
[default]
aws_access_key_id = REPLACE_WITH_TEMPORARY_LAB_KEY
aws_secret_access_key = REPLACE_WITH_TEMPORARY_LAB_SECRET
```

Protect the file:

```bash
chmod 600 aws-credentials.ini
```

Create the Kubernetes Secret:

```bash
kubectl create secret generic aws-secret \
  --namespace=crossplane-system \
  --from-file=creds=./aws-credentials.ini
```

What it does: stores temporary lab credentials in Kubernetes for the provider.

## Configure the provider

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

Apply it:

```bash
kubectl apply -f provider-config.yaml
```

What it does: tells the AWS provider where to find credentials.

## Create a unique bucket

Generate a unique name:

```bash
export AWS_ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
export BUCKET_NAME="xp-lab-${AWS_ACCOUNT_ID}-$(date +%s)"
echo "$BUCKET_NAME"
```

What it does: creates a globally unique S3 bucket name.

Create `bucket.yaml`:

```yaml
apiVersion: s3.aws.m.upbound.io/v1beta1
kind: Bucket
metadata:
  name: REPLACE_WITH_BUCKET_NAME
  namespace: default
  labels:
    app.kubernetes.io/managed-by: crossplane
    platform.example.com/environment: lab
spec:
  forProvider:
    region: eu-west-1
    tags:
      Environment: lab
      ManagedBy: crossplane
      Project: crossplane-learning
  providerConfigRef:
    name: default
    kind: ClusterProviderConfig
  managementPolicies:
    - "*"
```

Replace `REPLACE_WITH_BUCKET_NAME` with the generated bucket name.

Validate and apply:

```bash
kubectl apply --dry-run=server -f bucket.yaml
kubectl apply -f bucket.yaml
```

What it does: validates the manifest against installed provider schemas, then creates the managed resource.

## Observe reconciliation

```bash
kubectl get buckets.s3.aws.m.upbound.io -n default -w
```

What it does: watches Crossplane synchronize the Kubernetes object with AWS.

Inspect details:

```bash
kubectl describe bucket.s3.aws.m.upbound.io "$BUCKET_NAME" -n default
kubectl get bucket.s3.aws.m.upbound.io "$BUCKET_NAME" -n default -o yaml
```

What it does: shows conditions, provider messages, status, external name, and events.

Verify in AWS:

```bash
aws s3api head-bucket --bucket "$BUCKET_NAME"
aws s3api get-bucket-tagging --bucket "$BUCKET_NAME"
```

What it does: confirms the external bucket exists and has the expected tags.

## Add public-access blocking

Create `bucket-public-access.yaml`:

```yaml
apiVersion: s3.aws.m.upbound.io/v1beta1
kind: BucketPublicAccessBlock
metadata:
  name: REPLACE_WITH_BUCKET_NAME-public-access
  namespace: default
spec:
  forProvider:
    region: eu-west-1
    bucketRef:
      name: REPLACE_WITH_BUCKET_NAME
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

Validate and apply:

```bash
kubectl apply --dry-run=server -f bucket-public-access.yaml
kubectl apply -f bucket-public-access.yaml
```

What it does: creates a separate S3 managed resource that blocks public access for the bucket.

Verify:

```bash
aws s3api get-public-access-block --bucket "$BUCKET_NAME"
```

What it does: confirms the public-access block is present in AWS.

## Test drift correction

Manually change tags in AWS:

```bash
aws s3api put-bucket-tagging \
  --bucket "$BUCKET_NAME" \
  --tagging 'TagSet=[{Key=ManagedBy,Value=manual-change},{Key=Environment,Value=lab}]'
```

Request reconciliation:

```bash
kubectl annotate bucket.s3.aws.m.upbound.io "$BUCKET_NAME" \
  -n default \
  crossplane.io/reconcile-requested-at="$(date +%s)" \
  --overwrite
```

Check tags:

```bash
aws s3api get-bucket-tagging --bucket "$BUCKET_NAME"
```

What it does: proves which fields the provider observes and reconciles for the installed provider version.

> [!NOTE]
> Do not assume every cloud-computed or optional provider field is continuously overwritten. Confirm behavior with status, events, provider logs, and the external API.

## Inspect provider logs

```bash
kubectl logs -n crossplane-system \
  -l pkg.crossplane.io/provider=provider-aws-s3 \
  --tail=200
```

What it does: shows recent provider controller logs for debugging.

Events are often more useful:

```bash
kubectl get events -A --sort-by=.lastTimestamp
```

What it does: shows recent Kubernetes events across namespaces.

## Clean up safely

Delete dependent resources first:

```bash
kubectl delete -f bucket-public-access.yaml
```

Delete the bucket managed resource:

```bash
kubectl delete -f bucket.yaml
```

Watch until it disappears:

```bash
kubectl get buckets.s3.aws.m.upbound.io -n default -w
```

Confirm the AWS bucket is gone:

```bash
aws s3api head-bucket --bucket "$BUCKET_NAME"
```

What it does: should fail after successful deletion because the bucket no longer exists.

Delete the local cluster:

```bash
kind delete cluster --name crossplane-lab
```

Remove the credential file:

```bash
shred -u aws-credentials.ini 2>/dev/null || rm -f aws-credentials.ini
```

> [!WARNING]
> Do not delete the management cluster before Crossplane has deleted the external resources unless you intentionally want to orphan them.

## Related links

- [Crossplane](README.md)
- [Managed resources and lifecycle](managed-resources-and-lifecycle.md)
- [Providers and authentication](providers-and-authentication.md)
- [Crossplane on AWS](../../cross-topic-guides/crossplane-on-aws.md)
- [Crossplane managed-resource tutorial](https://docs.crossplane.io/latest/get-started/get-started-with-managed-resources/)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
