# Velero AWS S3 and EBS installation

## Purpose

Use this page to install Velero on Amazon EKS with AWS S3 backup storage and Amazon EBS persistent volume snapshots.

## Contents

- [Prerequisites](#prerequisites)
- [Create backup storage](#create-backup-storage)
- [Prepare IAM](#prepare-iam)
- [Install the EKS snapshot controller](#install-the-eks-snapshot-controller)
- [Create an EBS VolumeSnapshotClass](#create-an-ebs-volumesnapshotclass)
- [Install Velero with the AWS plugin](#install-velero-with-the-aws-plugin)
- [Enable node-agent when needed](#enable-node-agent-when-needed)
- [Example Velero locations after install](#example-velero-locations-after-install)
- [Validate the installation](#validate-the-installation)

## Prerequisites

| Requirement | Why it matters |
| --- | --- |
| EKS cluster access | Velero installs CRDs, a deployment, service account, and optional node-agent. |
| AWS CLI and kubectl | Needed to create AWS resources and verify Kubernetes state. |
| Helm or Velero CLI | Velero server can be installed with either method. |
| S3 bucket | Stores backup metadata, logs, and repository data. |
| EBS CSI driver | Required for EBS CSI-provisioned persistent volumes. |
| CSI snapshot controller | Required for Kubernetes `VolumeSnapshot` workflows on EKS. |
| IAM role for Velero | Allows S3 and EBS snapshot API calls without static long-lived credentials. |

> [!WARNING]
> S3 storage, EBS snapshots, restored EBS volumes, and EKS clusters can create ongoing AWS cost. Add lifecycle, retention, and cleanup checks before production rollout.

## Create backup storage

```bash
export AWS_REGION=eu-west-1
export BUCKET_NAME=my-velero-backups

aws s3 mb s3://${BUCKET_NAME} --region ${AWS_REGION}
```

What it does: creates the S3 bucket Velero will use for backup objects and logs.

> [!IMPORTANT]
> Use a bucket and prefix strategy that avoids multiple clusters accidentally deleting or overwriting each other's backups. For production, configure encryption, access logging where required, bucket policy, lifecycle, and object retention intentionally.

## Prepare IAM

Velero needs permissions for the S3 bucket and, when using EBS snapshots, EC2 snapshot APIs. On EKS, prefer EKS Pod Identity where available or IRSA where that is the cluster standard.

Minimum policy design should include:

- `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`, `s3:ListBucket`, and multipart upload permissions scoped to the Velero bucket and prefix.
- `ec2:CreateSnapshot`, `ec2:DeleteSnapshot`, `ec2:DescribeSnapshots`, `ec2:DescribeVolumes`, and `ec2:CreateTags` for EBS snapshot workflows.
- Trust policy limited to the `velero` namespace and `velero` service account.

> [!WARNING]
> The default chart or install examples may grant broad Kubernetes permissions. Review RBAC before production use and reduce access where your restore scope permits it.

### Example IAM policy shape

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::my-velero-backups"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": "arn:aws:s3:::my-velero-backups/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateSnapshot",
        "ec2:DeleteSnapshot",
        "ec2:DescribeSnapshots",
        "ec2:DescribeVolumes",
        "ec2:CreateTags"
      ],
      "Resource": "*"
    }
  ]
}
```

What it does: shows the permission categories Velero needs for S3 backup storage and EBS snapshot workflows. Scope this further to the account, region, bucket, tags, and snapshot ownership model used by your environment.

### Service account identity example

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: velero
  namespace: velero
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::<account-id>:role/velero-backup-role
```

What it does: shows the IRSA-style annotation that connects the Velero service account to an IAM role. If your platform uses EKS Pod Identity instead, bind the role through that mechanism and keep the service account name consistent.

## Install the EKS snapshot controller

```bash
aws eks create-addon \
  --cluster-name my-eks-cluster \
  --addon-name snapshot-controller \
  --region ${AWS_REGION}
```

What it does: installs the managed EKS snapshot controller add-on so CSI snapshot resources can be reconciled.

## Create an EBS VolumeSnapshotClass

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: ebs-csi-snapclass
  labels:
    velero.io/csi-volumesnapshot-class: "true"
  annotations:
    snapshot.storage.kubernetes.io/is-default-class: "true"
driver: ebs.csi.aws.com
deletionPolicy: Delete
```

What it does: defines the snapshot class Velero can use for EBS CSI-backed PVC snapshots.

> [!NOTE]
> Some EKS modes or examples may use a different EBS CSI driver name. Match the driver name used by your cluster's StorageClass and EBS CSI installation.

## Install Velero with the AWS plugin

The exact command depends on whether you use Helm or `velero install`. The important settings are the AWS plugin image, S3 backup storage location, AWS region, EBS snapshot location, and CSI feature flag.

### Install with Helm values

```yaml
serviceAccount:
  server:
    create: true
    name: velero
    annotations:
      eks.amazonaws.com/role-arn: arn:aws:iam::<account-id>:role/velero-backup-role
configuration:
  backupStorageLocation:
  - name: default
    provider: aws
    bucket: my-velero-backups
    prefix: clusters/prod-eks
    config:
      region: eu-west-1
  volumeSnapshotLocation:
  - name: default
    provider: aws
    config:
      region: eu-west-1
  features: EnableCSI
credentials:
  useSecret: false
deployNodeAgent: true
nodeAgent:
  podVolumePath: /var/lib/kubelet/pods
initContainers:
- name: velero-plugin-for-aws
  image: velero/velero-plugin-for-aws:v1.14.0
  volumeMounts:
  - mountPath: /target
    name: plugins
```

What it does: configures the Helm chart to use AWS S3 for backups, AWS EBS snapshots for volume snapshots, the AWS plugin, and workload identity instead of a static credentials secret.

### Install the chart

```bash
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts
helm repo update
helm install velero vmware-tanzu/velero \
  --namespace velero \
  --create-namespace \
  --values velero-values.yaml
```

What it does: installs Velero into the `velero` namespace with the prepared values.

### Equivalent CLI install shape

```bash
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.14.0 \
  --bucket my-velero-backups \
  --prefix clusters/prod-eks \
  --backup-location-config region=eu-west-1 \
  --snapshot-location-config region=eu-west-1 \
  --features EnableCSI \
  --use-node-agent \
  --no-secret
```

What it does: installs Velero with the AWS plugin, S3 backup location, AWS snapshot location, CSI support, node-agent, and workload identity instead of a credentials file.

> [!NOTE]
> `--no-secret` assumes the Velero pod receives AWS credentials from workload identity such as IRSA or EKS Pod Identity. If you use a credentials file for a lab, keep it out of Git and rotate it after testing.

## Enable node-agent when needed

Install or enable node-agent when using File System Backup or Velero built-in data mover.

```bash
velero install --use-node-agent --features=EnableCSI
```

What it does: shows the Velero CLI flags that enable the node-agent DaemonSet and CSI feature support.

> [!WARNING]
> Node-agent may require privileged or host filesystem access in some environments. Review cluster security policy before enabling file-system backup or data movement.

## Example Velero locations after install

```yaml
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: my-velero-backups
    prefix: clusters/prod-eks
  config:
    region: eu-west-1
  accessMode: ReadWrite
---
apiVersion: velero.io/v1
kind: VolumeSnapshotLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  config:
    region: eu-west-1
```

What it does: shows the two location resources Velero uses: object storage for backup archives and provider configuration for EBS snapshots.

## Validate the installation

```bash
kubectl get pods -n velero
velero backup-location get
velero snapshot-location get
kubectl get volumesnapshotclass
kubectl get daemonset node-agent -n velero
```

What it does: checks that Velero pods are running, backup and snapshot locations are available, and Kubernetes has a snapshot class.

### Run a smoke-test backup

```bash
kubectl create namespace velero-smoke-test
kubectl create configmap smoke-test \
  --from-literal=created-by=velero-docs \
  -n velero-smoke-test

velero backup create velero-smoke-test \
  --include-namespaces velero-smoke-test \
  --snapshot-volumes=false \
  --wait

velero backup describe velero-smoke-test --details
```

What it does: creates a tiny test namespace, backs up only Kubernetes resources, and shows whether Velero can write and describe a backup.

### Run a smoke-test restore

```bash
velero restore create velero-smoke-restore \
  --from-backup velero-smoke-test \
  --namespace-mappings velero-smoke-test:velero-smoke-restore \
  --wait

kubectl get configmap smoke-test -n velero-smoke-restore
velero restore describe velero-smoke-restore --details
```

What it does: restores the smoke-test ConfigMap into a different namespace so you can verify restore behavior without touching production workloads.

> [!WARNING]
> Clean up only the smoke-test namespaces you created. Do not run namespace deletion commands against production namespaces.

## Related links

- [Velero AWS plugin](https://github.com/velero-io/velero-plugin-for-aws)
- [Amazon EKS CSI snapshot controller](https://docs.aws.amazon.com/eks/latest/userguide/csi-snapshot-controller.html)
- [Amazon EBS CSI driver](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html)
- [Backup and restore workflows](backup-restore-workflows.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
