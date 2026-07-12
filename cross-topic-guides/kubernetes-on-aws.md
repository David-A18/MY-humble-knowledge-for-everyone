# Kubernetes on AWS

## Purpose

Collect guidance for running Kubernetes workloads on AWS infrastructure.

## EKS mental model

| Area | Kubernetes view | AWS/EKS view |
| --- | --- | --- |
| Control plane | Kubernetes API, scheduler, controllers | AWS manages the EKS control plane. |
| Data plane | Nodes run pods | EC2 managed node groups, self-managed nodes, Fargate, or newer EKS-managed options. |
| Identity | Service accounts and RBAC | IAM authenticates users and can grant workloads AWS permissions. |
| Networking | Pods, Services, Ingress, NetworkPolicy | VPC CNI, subnets, security groups, load balancers, and route tables. |
| Storage | PVs, PVCs, StorageClasses | EBS, EFS, and CSI drivers. |
| Observability | Logs, metrics, events, traces | CloudWatch, Container Insights, managed Prometheus, and third-party tooling. |

EKS runs upstream Kubernetes, so standard Kubernetes commands and manifests remain the core operating model. AWS adds managed control-plane operations and integrations for identity, networking, storage, load balancing, and observability.

## Daily operating checks

```bash
aws sts get-caller-identity
aws eks update-kubeconfig --region eu-west-1 --name production-platform
kubectl config current-context
kubectl get nodes -o wide
kubectl get pods -A --field-selector=status.phase!=Running
```

What it does: confirms AWS identity, connects `kubectl` to the cluster, confirms context, checks nodes, and finds pods that are not Running.

## Identity and access

| Need | Use | Notes |
| --- | --- | --- |
| Human or automation access to the Kubernetes API | EKS access entries and Kubernetes RBAC | Keep IAM authentication and Kubernetes authorization both intentional. |
| Workload access to AWS services | EKS Pod Identity or IRSA | Use one role per permission boundary where practical. |
| In-cluster authorization | Kubernetes Roles, ClusterRoles, and bindings | Keep namespace and cluster-wide permissions separate. |
| Debug access | Temporary least-privilege access | Remove elevated access after the incident or maintenance window. |

### Check identity and permissions

```bash
aws sts get-caller-identity
kubectl auth can-i get pods -n app
kubectl auth can-i update deployments -n app
```

What it does: confirms the AWS principal and checks what that authenticated identity can do inside Kubernetes.

> [!IMPORTANT]
> AWS IAM authentication does not automatically mean Kubernetes authorization. EKS access, RBAC, and namespace scope all matter.

## Networking and traffic

| Topic | Practical check | Why it matters |
| --- | --- | --- |
| VPC CNI | `kubectl get pods -n kube-system -l k8s-app=aws-node` | Pod networking depends on the CNI. |
| Services | `kubectl get svc,endpoints -n <namespace>` | Services need matching Ready endpoints. |
| Load balancers | `kubectl describe svc <service> -n <namespace>` | LoadBalancer Services create AWS load balancers through controllers or cloud integration. |
| Ingress | `kubectl get ingress -n <namespace>` | Ingress usually depends on an installed controller. |
| Network policy | `kubectl get networkpolicy -A` | Policy support depends on the networking implementation. |

### Debug Service reachability

```bash
kubectl get svc,endpoints,endpointslice -n app
kubectl describe svc web -n app
kubectl get pods -n app --show-labels
```

What it does: checks whether the Service selector matches Ready pods and whether endpoints are being created.

## Add-ons and platform components

| Component | What to check |
| --- | --- |
| Amazon VPC CNI | Add-on version, pod health, IP capacity, and subnet sizing. |
| CoreDNS | Pod health and DNS resolution from application pods. |
| kube-proxy | Add-on version and node compatibility. |
| AWS Load Balancer Controller | Controller health, IAM permissions, and annotations. |
| EBS or EFS CSI drivers | Driver pods, StorageClasses, PVC events, and IAM permissions. |

### Check managed add-ons

```bash
aws eks list-addons --cluster-name production-platform --region eu-west-1
kubectl get pods -n kube-system
```

What it does: lists EKS add-ons and checks the Kubernetes system namespace for component health.

## Storage

| Need | AWS service | Kubernetes object |
| --- | --- | --- |
| Block storage for one pod at a time | Amazon EBS | PersistentVolumeClaim and StorageClass. |
| Shared filesystem access | Amazon EFS | PersistentVolumeClaim and CSI driver. |
| Object storage | Amazon S3 | Application SDK access through Pod Identity or IRSA. |

### Check PVC issues

```bash
kubectl get pvc -n app
kubectl describe pvc <claim-name> -n app
kubectl get storageclass
```

What it does: checks claim state, provisioning events, and available StorageClasses.

## Cost visibility

| Practice | Why it helps |
| --- | --- |
| Label workloads consistently | Enables cost grouping by app, team, or environment. |
| Use namespaces intentionally | Helps separate operational and reporting boundaries. |
| Right-size requests | Avoids reserving capacity that workloads do not use. |
| Review idle nodes and overprovisioning | Reduces compute waste. |
| Use cost tooling such as Kubecost where appropriate | Provides Kubernetes-level cost allocation on EKS. |

## Operational questions

- Which workloads require public ingress?
- Which AWS services does the workload need to access?
- How are cluster upgrades planned and tested?
- Which logs and metrics are required for operations?
- Which namespaces, labels, and tags are required for cost allocation?
- Which identities can administer the cluster, deploy workloads, and read Secrets?

## Related links

- [Kubernetes commands](../kubernetes/commands/README.md)
- [EKS operations](eks-operations.md)
- [Deploying to EKS](deploying-to-eks.md)
- [Amazon EKS Best Practices Guide](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html)
- [Amazon EKS documentation](https://docs.aws.amazon.com/eks/)
- [Amazon EKS networking best practices](https://docs.aws.amazon.com/eks/latest/best-practices/networking.html)
- [Amazon EKS cost optimization best practices](https://docs.aws.amazon.com/eks/latest/best-practices/cost-opt.html)
- [Kubernetes index](../kubernetes/README.md)
- [AWS index](../aws/README.md)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
