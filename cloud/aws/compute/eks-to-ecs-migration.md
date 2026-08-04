# EKS to ECS migration

## Purpose

Use this guide to plan a full-platform migration from Amazon EKS to Amazon ECS.

This is not only a Kubernetes manifest rewrite. It changes the platform API, deployment workflow, identity model, service discovery, autoscaling, observability, policy enforcement, and operating runbooks.

## When migration makes sense

| Situation | ECS migration fit |
| --- | --- |
| Workloads are mostly stateless services and workers | Strong fit. |
| Kubernetes is only used to run containers | Strong fit. |
| Team wants less Kubernetes platform ownership | Strong fit. |
| Platform depends heavily on CRDs and operators | Requires redesign. |
| Developers rely on Kubernetes as a self-service API | Requires a replacement platform interface. |
| Workloads use StatefulSets and PVC-heavy storage | Migrate carefully or keep on EKS. |
| Multi-cloud Kubernetes portability is required | Usually stay on EKS. |

## Migration assessment

Inventory the current EKS platform before creating ECS resources.

| Inventory area | What to collect | Why it matters |
| --- | --- | --- |
| Workloads | Deployments, StatefulSets, DaemonSets, Jobs, CronJobs, init containers, sidecars. | Determines ECS services, tasks, schedules, and unsupported patterns. |
| Traffic | Services, Ingress, Gateway API, load balancer annotations, TLS, DNS, WAF, CloudFront. | Determines ALB, NLB, Service Connect, Cloud Map, API Gateway, and DNS design. |
| Identity | Service accounts, IRSA, EKS Pod Identity, RBAC, namespace admins. | Maps workload permissions to ECS task roles and human access to IAM. |
| Configuration | ConfigMaps, Secrets, mounted files, environment variables. | Maps to task definition environment, Secrets Manager, SSM Parameter Store, S3, or baked configuration. |
| Storage | PVCs, StorageClasses, EBS, EFS, snapshots, backup tools. | Determines EFS, EBS, FSx, S3, or managed data-service changes. |
| Autoscaling | HPA, KEDA, Cluster Autoscaler, Karpenter, node groups. | Maps to ECS Service Auto Scaling and capacity providers. |
| Platform extensions | CRDs, operators, admission webhooks, policy engines, service mesh. | Identifies functionality that ECS will not preserve automatically. |
| Delivery | Helm, Kustomize, Argo CD, Flux, CI/CD, image promotion. | Determines ECS deployment pipeline and IaC ownership. |
| Observability | Logs, metrics, traces, dashboards, alerts, Kubernetes events. | Maps to CloudWatch logs, metrics, Container Insights, tracing, and service events. |
| Operations | `kubectl` runbooks, break-glass access, rollback, incident diagnostics. | Runbooks must change to ECS, AWS CLI, CloudWatch, ELB, and IAM workflows. |

### Inventory current Kubernetes resources

```bash
kubectl get deploy,statefulset,daemonset,job,cronjob -A
kubectl get svc,ingress,gateway,httproute -A
kubectl get hpa -A
kubectl get pvc,storageclass -A
kubectl get serviceaccount,role,rolebinding,clusterrole,clusterrolebinding -A
kubectl get crd
```

What it does: lists the Kubernetes workload, traffic, scaling, storage, identity, and extension surfaces that need a target design in ECS or another AWS service.

## Translation map

| EKS source | ECS or AWS target | Migration notes |
| --- | --- | --- |
| Deployment | ECS service | Convert the Pod template into a task definition and desired replicas into desired task count. |
| Pod | ECS task | Containers in the same ECS task share lifecycle and can communicate on `localhost`. |
| Container image | Same image in ECR or registry | Review entrypoint, health check, platform, CPU, memory, and filesystem assumptions. |
| Kubernetes Service | Service Connect, AWS Cloud Map, ALB, or NLB | Choose by internal discovery, HTTP ingress, or TCP/UDP ingress. |
| Ingress | ALB listener rules, NLB, CloudFront, API Gateway, or WAF integration | Translate annotations into explicit AWS resources. |
| HPA | ECS Service Auto Scaling | Use CPU, memory, ALB request count, queue backlog, or custom CloudWatch metrics. |
| CronJob | EventBridge Scheduler plus ECS `RunTask` | Define execution role, retry behavior, and dead-letter queue where needed. |
| Job | Standalone ECS task | Add clear exit handling, logs, retries, and idempotency. |
| ConfigMap | Task definition env vars, SSM Parameter Store, S3, or app config | Avoid large or frequently changed config embedded in task definitions. |
| Secret | Secrets Manager or SSM Parameter Store | Reference secrets from task definitions; do not use plaintext values. |
| IRSA or Pod Identity | ECS task role | Create one task role per application permission boundary. |
| Kubernetes RBAC | IAM policies, ECS cluster boundaries, account boundaries, pipeline permissions | ECS has no namespace RBAC equivalent. |
| Namespace | ECS cluster, AWS account, tags, naming, or deployment pipeline boundary | Pick one isolation model intentionally. |
| PVC | EFS, EBS, FSx, S3, or managed service | Recheck durability, sharing, backup, and replacement behavior. |
| DaemonSet | Usually not a direct ECS service | Replace with managed services, EC2 user data, sidecars, agents on EC2 capacity, or keep on EKS if required. |
| CRD and operator | AWS managed service, IaC module, custom automation, or EKS | ECS does not provide Kubernetes reconciliation APIs. |
| Admission policy | IAM, CI checks, IaC policy, AWS Config, Security Hub, or service control policies | Shift policy left and enforce at AWS boundaries. |
| Argo CD or Flux | CodePipeline, GitHub Actions, Terraform, CDK, Copilot, or custom ECS deployer | Decide what owns task definitions, services, and infrastructure. |

## Full-platform changes

### Developer workflow

EKS developers often change Helm values, Kustomize overlays, or Kubernetes manifests. In ECS, the delivery unit becomes:

- Container image.
- Task definition revision.
- ECS service update.
- Supporting IaC for load balancers, IAM roles, security groups, schedules, and service discovery.

If developers used Kubernetes as a platform API through CRDs, replace that interface with one of:

- Terraform or CDK modules.
- AWS Service Catalog.
- A Backstage template or internal developer portal.
- A small platform service that writes ECS/IaC definitions.
- Keep the CRD-based platform on EKS if the Kubernetes API is the product.

### Traffic and service discovery

Move public traffic from Kubernetes Ingress or Gateway API to explicit AWS resources:

- ALB for HTTP and HTTPS routing.
- NLB for TCP, UDP, static IP, or low-level network routing.
- CloudFront and WAF when edge caching or internet-facing protection is needed.
- Service Connect or AWS Cloud Map for private service discovery.

> [!IMPORTANT]
> In ECS, service networking is VPC-native. Security groups, subnets, target groups, listeners, and DNS become first-class migration decisions instead of hidden side effects of Kubernetes annotations.

### Identity and access

Replace Kubernetes service-account based workload identity with ECS task roles. The application still receives AWS credentials from the runtime, but the trust path and resource configuration change.

| EKS | ECS |
| --- | --- |
| Kubernetes service account | ECS task definition. |
| IRSA or EKS Pod Identity association | Task role attached to the task definition. |
| Pod execution environment | ECS task runtime. |
| Kubernetes RBAC for platform access | IAM and CI/CD permissions. |

### Autoscaling and capacity

Replace HPA and node scaling with two ECS layers:

- Service scaling changes the number of running tasks.
- Capacity provider scaling changes the infrastructure available for tasks, unless using Fargate where capacity is serverless.

Use target tracking first when CPU, memory, or request count tracks demand well. Use custom CloudWatch metrics for queue depth, stream lag, or domain-specific saturation.

### Observability

Map Kubernetes logs, events, and controller status to ECS and AWS signals:

- ECS service events.
- Task stopped reasons.
- Container logs in CloudWatch Logs.
- ECS service and cluster metrics.
- Container Insights when task-level detail is needed.
- ALB or NLB target health and access logs.
- CloudTrail for ECS, IAM, and deployment API calls.

## Migration flow

1. Freeze the target architecture.
   - Select ECS Managed Instances, Fargate, or EC2 capacity providers.
   - Define cluster, VPC, subnet, security group, load balancer, DNS, logging, and tagging standards.

2. Classify workloads.
   - Move stateless Deployments first.
   - Convert CronJobs to EventBridge Scheduler.
   - Convert Jobs to standalone tasks.
   - Redesign StatefulSets, DaemonSets, CRDs, and operator-backed flows separately.

3. Build ECS infrastructure with IaC.
   - Create ECS clusters, capacity providers, IAM roles, log groups, target groups, listeners, services, schedules, and service discovery namespaces.
   - Keep task definitions and service definitions versioned.

4. Convert application runtime definitions.
   - Translate Pod containers to task definition containers.
   - Map probes to container health checks and load balancer health checks.
   - Map resources to task CPU and memory.
   - Move secrets to Secrets Manager or SSM Parameter Store references.

5. Replace platform functions.
   - Replace GitOps with the chosen ECS deployment pipeline.
   - Replace Kubernetes admission policy with CI/IaC policy and AWS controls.
   - Replace operators with AWS managed services, IaC, or targeted automation.

6. Run in parallel.
   - Deploy ECS service beside the EKS workload.
   - Mirror non-mutating traffic or run synthetic tests.
   - Compare latency, error rate, scaling behavior, logs, and cost.

7. Shift traffic gradually.
   - Use weighted DNS, ALB listener rules, CloudFront origin weighting, or blue/green deployment strategy.
   - Keep EKS rollback available until ECS success criteria are met.

8. Decommission EKS pieces.
   - Remove traffic from EKS.
   - Stop workloads.
   - Archive manifests and runbooks.
   - Remove unused load balancers, node groups, add-ons, IAM roles, and clusters after the rollback window.

## Real-life scenarios

### Simple API migration

Move a Kubernetes Deployment and Ingress to an ECS service behind an ALB.

Implementation pattern:

- One task definition for the API.
- One ECS service with desired count greater than one.
- ALB listener rules for HTTP paths or hostnames.
- Task role for RDS, S3, DynamoDB, or Secrets Manager access.
- CloudWatch logs and target-tracking scaling.

### Internal microservices platform

Move Kubernetes Deployments and Services to ECS services with Service Connect.

Implementation pattern:

- One ECS service per microservice.
- Shared Service Connect namespace.
- Service-specific task roles.
- Private subnets and security groups.
- CloudWatch dashboards for latency, errors, CPU, memory, and task count.

### Queue worker system

Move Kubernetes worker Deployments or KEDA-scaled consumers to ECS services.

Implementation pattern:

- ECS service for steady workers.
- Scale from SQS backlog, MSK lag, or custom CloudWatch metrics.
- Fargate Spot or EC2 Spot only if processing is idempotent and interruption-safe.
- Dead-letter queues and replay runbooks.

### Scheduled processing

Move Kubernetes CronJobs to EventBridge Scheduler invoking ECS tasks.

Implementation pattern:

- One task definition per scheduled command family.
- EventBridge schedule with an execution role.
- CloudWatch Logs for output.
- Dead-letter queue for missed or failed invocations where required.

### Service mesh replacement

Move from in-cluster service mesh patterns to ECS Service Connect where requirements are service discovery, short names, and basic traffic telemetry.

Implementation pattern:

- Service Connect configuration on client and server services.
- Cloud Map namespace.
- ECS deployments to roll Service Connect config consistently.
- Keep EKS or choose another mesh pattern if you require Kubernetes-specific mesh policy, sidecar injection, or advanced traffic controls that ECS Service Connect does not cover.

### Case where staying on EKS is better

Stay on EKS when the platform relies on CRDs and operators as the main control plane. Examples include Crossplane platform APIs, custom controllers, admission webhooks, policy engines, and developer workflows that depend on `kubectl`, Helm, Argo CD, or Flux. In this case, reducing Kubernetes operations may be better handled by EKS Auto Mode, managed add-ons, or platform simplification rather than moving to ECS.

## Cutover checklist

- [ ] ECS service passes health checks.
- [ ] Logs, metrics, traces, and alarms are active.
- [ ] Task role permissions are least privilege.
- [ ] Secrets are referenced from managed stores.
- [ ] Scaling policy has been tested.
- [ ] Rollback target remains available.
- [ ] DNS TTL and cache behavior are understood.
- [ ] Runbooks no longer require Kubernetes commands for the migrated workload.
- [ ] Cost tags are applied to ECS, load balancer, log, and data resources.
- [ ] Unused EKS resources are removed only after the rollback window.

## Official documentation

- [Amazon ECS documentation](https://docs.aws.amazon.com/ecs/)
- [Amazon ECS task definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
- [Amazon ECS services](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html)
- [ECS launch types and capacity providers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/capacity-launch-type-comparison.html)
- [Interconnect Amazon ECS services](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/interconnecting-services.html)
- [Amazon ECS task IAM role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html)
- [Automatically scale your Amazon ECS service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-auto-scaling.html)
- [What is Amazon EKS?](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)

## Related links

- [Amazon ECS](amazon-ecs.md)
- [ECS vs. EKS](ecs-vs-eks.md)
- [Kubernetes on AWS](../../../cross-topic-guides/kubernetes-on-aws.md)
- [EKS operations](../../../cross-topic-guides/eks-operations.md)
- [AWS compute](README.md)
- [AWS index](../README.md)
- [Back to root index](../../../README.md)
