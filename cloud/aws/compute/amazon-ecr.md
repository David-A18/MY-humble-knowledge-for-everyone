# Amazon ECR

## Purpose

Use this page to understand Amazon Elastic Container Registry (ECR), secure
private repositories, lifecycle management, repository permissions, and using
ECR as an OCI registry for Helm charts. It also shows how ECR fits into a
Crossplane-managed platform without confusing artifact delivery with
infrastructure reconciliation.

## What ECR is

Amazon ECR is AWS's managed container registry. A private ECR repository stores
container images, OCI images, and OCI-compatible artifacts. A registry belongs
to an AWS account and Region; repositories organize artifacts within it. ECR can
serve image pulls for EKS or ECS and OCI Helm charts for Helm clients.

| Concept | Meaning | Operational impact |
| --- | --- | --- |
| Registry | Account-and-Region ECR endpoint. | Authentication and image URLs are Region-specific. |
| Repository | Logical artifact collection, such as `payments/api`. | Apply repository controls and access policy here. |
| Image/tag/digest | Image artifact and its mutable tag or content digest. | Prefer an approved immutable tag or digest for deployment. |
| Repository policy | Resource-based policy attached to one repository. | Grants selected principals repository access. |
| IAM policy | Identity-based AWS permission policy. | Grants the principal the ability to call ECR APIs. |
| Lifecycle policy | Rules that expire or archive eligible artifacts. | Reduces stale-artifact cost, but can remove recoverable releases. |
| OCI artifact | Standard container-registry artifact format. | Lets ECR store Helm charts as well as images. |

## Private repository design

Choose repository names that reflect ownership and purpose, for example
`payments/api` or `platform/charts`. Use tags for release labels, but retain an
immutable digest for the exact artifact selected by deployment automation.

### Recommended controls

| Control | Why it matters | Verify with |
| --- | --- | --- |
| Least-privilege IAM | Limits who can authenticate, push, pull, or alter policy. | IAM policy review and CloudTrail. |
| Repository policy | Grants cross-account or service-specific access only where needed. | `get-repository-policy` and principal review. |
| Immutable tags | Prevents a tag from being overwritten. | Repository configuration and release workflow. |
| Encryption | Protects stored artifacts at rest. | Repository configuration and KMS ownership where used. |
| Scanning policy | Detects known image vulnerabilities according to the selected ECR scanning model. | Registry/repository scanning configuration and CI gates. |
| Lifecycle policy | Expires stale artifacts according to reviewed retention rules. | Lifecycle-policy preview before activation. |
| Audit trail | Investigates pushes, policy changes, and deletions. | CloudTrail events and retention. |

### Repository policies versus IAM policies

Repository policies are resource-based policies scoped to an ECR repository.
IAM policies grant permissions to identities and can be scoped across ECR or to
specific resources. AWS evaluates both; an explicit denial wins. A repository
policy does not remove the need for the caller to have IAM permission for
`ecr:GetAuthorizationToken` before it can authenticate to an ECR registry.

Use a repository policy for a narrow exception, such as allowing a role from a
different account to pull from one repository. Use IAM for broad identity
permissions and the required registry authentication capability. Avoid granting
anonymous or account-wide write access just to make a deployment work.

## Authenticate and push a container image

Set the placeholders in a shell that does not echo secrets to logs. The AWS CLI
returns a temporary registry password; the command sends it to Helm or Docker
through standard input rather than printing it.

```bash
export AWS_REGION=<aws-region>
export AWS_ACCOUNT_ID=<aws-account-id>
export ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

aws ecr get-login-password --region "$AWS_REGION" | \
  docker login --username AWS --password-stdin "$ECR_REGISTRY"
```

What it does: authenticates Docker to the account-and-Region ECR registry. The
AWS principal needs `ecr:GetAuthorizationToken` as well as the repository-level
actions required to push or pull.

```bash
docker build -t payments-api:<reviewed-tag> .
docker tag payments-api:<reviewed-tag> \
  "$ECR_REGISTRY/payments-api:<reviewed-tag>"
docker push "$ECR_REGISTRY/payments-api:<reviewed-tag>"
```

What it does: builds a local image, gives it its ECR destination name, and
pushes it. Build, signing, SBOM generation, and vulnerability gates normally
belong in CI/CD rather than an operator's workstation.

> [!WARNING]
> Do not paste ECR passwords, access keys, or `dockerconfigjson` values into
> Git, Helm values, terminal transcripts, or issue comments. Use workload
> identity or a secret-management process appropriate for the runner and target
> cluster.

## Lifecycle policies

ECR lifecycle policies contain ordered rules for expiring or archiving artifacts
that meet selected criteria. AWS recommends previewing the policy before
applying it. Eligible artifacts can be removed within 24 hours, so retention
rules must protect release artifacts required for rollback, incident response,
and regulatory retention.

### Preview before applying

```bash
aws ecr start-lifecycle-policy-preview \
  --repository-name payments-api \
  --lifecycle-policy-text file://lifecycle-policy.json \
  --region "$AWS_REGION"

aws ecr get-lifecycle-policy-preview \
  --repository-name payments-api \
  --region "$AWS_REGION"
```

What it does: starts an ECR evaluation of a local policy file and retrieves the
candidate artifacts before changing repository retention. Review a completed
preview and preserve artifacts referenced by current deployments and rollback
plans.

> [!WARNING]
> A lifecycle policy is a deletion policy. Do not deploy a policy based only on
> an example or a tag naming assumption. Test its preview against a
> representative non-production repository first.

## Helm charts in ECR through OCI

Helm packages a chart as an OCI artifact. ECR can store that artifact in a
private repository. The ECR repository name must match the chart name, and Helm
uses an `oci://` reference to push and pull it.

### Package and publish a chart

```bash
export AWS_REGION=<aws-region>
export AWS_ACCOUNT_ID=<aws-account-id>
export ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

helm package charts/payments-api

aws ecr create-repository \
  --repository-name payments-api \
  --region "$AWS_REGION"

aws ecr get-login-password --region "$AWS_REGION" | \
  helm registry login --username AWS --password-stdin "$ECR_REGISTRY"

helm push payments-api-<chart-version>.tgz "oci://$ECR_REGISTRY"
```

What it does: packages the chart, creates its corresponding ECR repository,
authenticates Helm, and pushes the chart artifact. The chart's `name` field must
match the ECR repository name. In an established environment, create the
repository through reviewed infrastructure code or a Crossplane API rather than
having every CI job create it.

### Pull, inspect, and install a chart

```bash
helm show chart "oci://$ECR_REGISTRY/payments-api" \
  --version <reviewed-chart-version>

helm upgrade --install payments-api "oci://$ECR_REGISTRY/payments-api" \
  --namespace payments \
  --create-namespace \
  --version <reviewed-chart-version> \
  --values values-production.yaml \
  --dry-run --debug
```

What it does: reads chart metadata from the OCI repository, then previews the
chart installation with a pinned version and reviewed values. Run the command
again without `--dry-run --debug` only after confirming the rendered changes.

## ECR with Crossplane

Crossplane can manage an ECR repository as a provider-defined managed resource.
The provider reconciles ECR configuration; it does not build, scan, sign, or
push an application artifact. Use a Composition and XRD when teams should ask
for a standard repository or delivery capability without controlling every AWS
field.

```text
Crossplane ProviderConfig -> ECR provider -> Repository managed resource -> AWS ECR
Platform XR -> Composition -> ECR repository + Kubernetes workload objects
CI/CD -> build, sign, scan, push -> ECR image or Helm chart artifact
```

The [Application delivery platform API](../../../kubernetes/crossplane/application-delivery-platform-api.md) presents an `ApplicationDelivery` XR that generates an ECR repository, Deployment, and Service. It deliberately accepts an existing image reference because artifact creation belongs to the delivery pipeline.

### Validate a Crossplane ECR resource schema

```bash
kubectl get providers.pkg.crossplane.io
kubectl api-resources | grep -i ecr
kubectl explain repository.ecr.aws.m.upbound.io.spec.forProvider
```

What it does: confirms provider health and the exact provider schema available
in the cluster. Package versions move independently, so do not copy an ECR
managed-resource field from an example without this check.

## Troubleshooting

| Symptom | Likely cause | First check |
| --- | --- | --- |
| Login succeeds but push is denied | Missing repository action or repository policy restriction. | IAM permissions, repository policy, and ECR events. |
| EKS Pod cannot pull an image | Wrong image URI, image does not exist, or node/workload identity cannot pull. | Pod events, image digest/tag, and ECR pull permissions. |
| Helm push fails | Chart name and ECR repository differ, login expired, or OCI reference is wrong. | `Chart.yaml`, repository name, and registry login. |
| Rollback image disappeared | Lifecycle policy expired a required artifact. | Lifecycle preview, image detail, and release retention policy. |
| Crossplane repository is not ready | Provider package, identity, IAM, or ECR resource schema problem. | MR conditions, events, and provider controller logs. |

## Related links

- [Helm for Kubernetes and Crossplane](../../../kubernetes/applications-and-tools/helm.md)
- [Application delivery platform API](../../../kubernetes/crossplane/application-delivery-platform-api.md)
- [Providers, managed resources, and compositions](../../../kubernetes/crossplane/providers-compositions-and-managed-resources.md)
- [Amazon ECR documentation](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
- [Amazon ECR private repositories](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html)
- [Amazon ECR repository policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policies.html)
- [Amazon ECR lifecycle policies](https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html)
- [Push a Helm chart to Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/push-oci-artifact.html)
- [Back to AWS compute](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
