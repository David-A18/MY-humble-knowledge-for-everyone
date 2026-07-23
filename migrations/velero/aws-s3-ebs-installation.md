# Velero AWS S3 and EBS installation

## Purpose

Use this page to install Velero on Amazon EKS with AWS S3 backup storage and Amazon EBS persistent volume snapshots.

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
configuration:
  backupStorageLocation:
  - name: default
    provider: aws
    bucket: my-velero-backups
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

## Enable node-agent when needed

Install or enable node-agent when using File System Backup or Velero built-in data mover.

```bash
velero install --use-node-agent --features=EnableCSI
```

What it does: shows the Velero CLI flags that enable the node-agent DaemonSet and CSI feature support.

> [!WARNING]
> Node-agent may require privileged or host filesystem access in some environments. Review cluster security policy before enabling file-system backup or data movement.

## Validate the installation

```bash
kubectl get pods -n velero
velero backup-location get
velero snapshot-location get
kubectl get volumesnapshotclass
```

What it does: checks that Velero pods are running, backup and snapshot locations are available, and Kubernetes has a snapshot class.

## Related links

- [Velero AWS plugin](https://github.com/velero-io/velero-plugin-for-aws)
- [Amazon EKS CSI snapshot controller](https://docs.aws.amazon.com/eks/latest/userguide/csi-snapshot-controller.html)
- [Amazon EBS CSI driver](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html)
- [Backup and restore workflows](backup-restore-workflows.md)
- [Back to Velero index](README.md)
- [Back to migrations index](../README.md)
- [Back to root index](../../README.md)
