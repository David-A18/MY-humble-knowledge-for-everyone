---
type: Explanation
title: 'IRSA S3 access on EKS: positive and negative tests'
description: Grant one Pod read access to a synthetic S3 prefix and prove that other
  actions and service accounts are rejected.
tags:
- cross-topic-guides
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: aws-service-account-role-procedure
  resource: https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html
  title: AWS service-account role procedure
- id: eksctl-iam-service-accounts
  resource: https://docs.aws.amazon.com/eks/latest/eksctl/iamserviceaccounts.html
  title: eksctl IAM service accounts
---

# IRSA S3 access on EKS: positive and negative tests

## Purpose

Grant one Pod read access to a synthetic S3 prefix and prove that other actions and service accounts are rejected.

Sources reviewed: 2026-10-29. See the [validation record](../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Prerequisites

Use an existing disposable EKS cluster, AWS CLI v2, eksctl, kubectl, Bash, and Python 3.13. The operator needs IAM/OIDC administration and namespace access. Prepare a dedicated S3 bucket containing a synthetic `public-lab/sample.txt` object. Use SSE-S3 for this introductory lab to avoid adding KMS policy complexity. The lab creates IAM resources and Pods; it does not create the cluster.[^aws-service-account-role-procedure][^eksctl-iam-service-accounts]

Set `CLUSTER`, `AWS_REGION`, and `BUCKET` to your lab values. Run from the repository root. The workload image is pinned to AWS CLI **2.31.0**. Live AWS execution was not performed on the authoring host.

> [!WARNING]
> These steps modify IAM trust and permissions. Verify AWS identity, account, region, cluster, and bucket before creating resources. Use only dedicated lab names.

## Create the read policy and service account

```bash
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export POLICY_NAME="kb-irsa-lab-${CLUSTER}"
python -c 'import json,os; print(json.dumps({"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"s3:GetObject","Resource":"arn:aws:s3:::"+os.environ["BUCKET"]+"/public-lab/*"}]}))' > /tmp/irsa-read-policy.json
aws iam create-policy --policy-name "$POLICY_NAME" --policy-document file:///tmp/irsa-read-policy.json
export POLICY_ARN="arn:aws:iam::$AWS_ACCOUNT_ID:policy/$POLICY_NAME"
eksctl utils associate-iam-oidc-provider --cluster "$CLUSTER" --region "$AWS_REGION" --approve
kubectl create namespace irsa-lab
eksctl create iamserviceaccount --cluster "$CLUSTER" --region "$AWS_REGION" --namespace irsa-lab --name s3-reader --attach-policy-arn "$POLICY_ARN" --approve
```

What it does: creates a prefix-scoped policy and an eksctl-managed role/service-account binding. The ARN example targets the standard AWS partition. Export `BUCKET` before the Python command. Inspect the created trust policy and confirm its exact `sub` and `aud` conditions.

## Start a workload using that service account

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: reader
  namespace: irsa-lab
spec:
  serviceAccountName: s3-reader
  containers:
    - name: aws
      image: public.ecr.aws/aws-cli/aws-cli:2.31.0
      command: [sh, -c, "sleep 3600"]
```

What it does: creates a command-capable lab container. Save as `/tmp/irsa-reader.yaml` and apply it after service-account creation so the workload identity integration can configure the Pod.

```bash
kubectl apply -f /tmp/irsa-reader.yaml
kubectl wait pod/reader -n irsa-lab --for=condition=Ready --timeout=120s
kubectl exec -n irsa-lab reader -- aws sts get-caller-identity
kubectl exec -n irsa-lab reader -- aws s3api get-object --bucket "$BUCKET" --key public-lab/sample.txt /tmp/sample.txt
kubectl exec -n irsa-lab reader -- aws s3api put-object --bucket "$BUCKET" --key public-lab/forbidden.txt --body /tmp/sample.txt
```

What it does: proves the intended role is assumed, a permitted read succeeds, and a write fails with AccessDenied. Do not interpret a missing object or network timeout as the expected authorization failure.

## Negative trust test

```bash
ROLE_ARN=$(kubectl get serviceaccount s3-reader -n irsa-lab -o jsonpath='{.metadata.annotations.eks\.amazonaws\.com/role-arn}')
kubectl create serviceaccount s3-denied -n irsa-lab
kubectl annotate serviceaccount s3-denied -n irsa-lab "eks.amazonaws.com/role-arn=$ROLE_ARN"
kubectl run denied-reader -n irsa-lab --image=public.ecr.aws/aws-cli/aws-cli:2.31.0 --restart=Never --overrides='{"spec":{"serviceAccountName":"s3-denied"}}' --command -- sh -c 'sleep 3600'
kubectl wait pod/denied-reader -n irsa-lab --for=condition=Ready --timeout=120s
kubectl exec -n irsa-lab denied-reader -- aws sts get-caller-identity
```

What it does: tries the same role with a different service-account subject. Role assumption must fail because the trust policy permits only `s3-reader`. Verify there are no static credentials or accessible node credentials masking this result. See [IRSA troubleshooting](../cloud/aws/security/irsa-troubleshooting.md).

## Cleanup

> [!WARNING]
> Verify the cluster, account, and resource names before deleting. Remove only the lab resources; retain shared OIDC providers and the existing cluster.

```bash
kubectl delete pod reader denied-reader -n irsa-lab --ignore-not-found
eksctl delete iamserviceaccount --cluster "$CLUSTER" --region "$AWS_REGION" --namespace irsa-lab --name s3-reader --wait
aws iam delete-policy --policy-arn "$POLICY_ARN"
kubectl delete namespace irsa-lab
```

What it does: removes the eksctl-managed binding/role and the custom policy after detachment. Leave the bucket under its existing owner; remove only synthetic objects you created if its retention rules permit.

## Related links

- [AWS service-account role procedure](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html)
- [eksctl IAM service accounts](https://docs.aws.amazon.com/eks/latest/eksctl/iamserviceaccounts.html)
- [Cloud](../cloud/index.md)
- [AWS](../cloud/aws/index.md)
- [Kubernetes](../kubernetes/index.md)
- [IRSA fundamentals](../cloud/aws/security/irsa-fundamentals.md)
- [Back to parent index](index.md)
- [Back to root index](../../README.md)

[^aws-service-account-role-procedure]: [AWS service-account role procedure](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html).
[^eksctl-iam-service-accounts]: [eksctl IAM service accounts](https://docs.aws.amazon.com/eks/latest/eksctl/iamserviceaccounts.html).
