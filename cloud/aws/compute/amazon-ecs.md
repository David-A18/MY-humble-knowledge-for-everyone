# Amazon ECS

## Purpose

Use this guide to understand Amazon Elastic Container Service (Amazon ECS), what runs there, how its main components fit together, and which operational patterns are practical in real AWS environments.

Amazon ECS is AWS-native container orchestration. You define containers, networking, IAM, storage, scaling, and deployment behavior in ECS and adjacent AWS services instead of operating a Kubernetes API, controllers, add-ons, and cluster-level abstractions.

## When to use ECS

| Situation | ECS fit | Why |
| --- | --- | --- |
| Public web application or API | Strong fit | Run an ECS service behind an Application Load Balancer or Network Load Balancer. |
| Internal microservices | Strong fit | Use Service Connect or AWS Cloud Map for service discovery and service-to-service traffic. |
| Background workers | Strong fit | Run queue consumers as ECS services and scale from CPU, memory, queue depth, or custom CloudWatch metrics. |
| Scheduled processing | Strong fit | Use EventBridge Scheduler to run ECS tasks on one-time, rate, or cron schedules. |
| One-off jobs | Strong fit | Use standalone ECS tasks for migrations, maintenance, and batch-style commands. |
| Windows containers | Good fit | ECS supports Windows containers on supported Fargate or EC2 options. |
| GPU workloads | Good fit with managed or EC2 capacity | Use ECS Managed Instances or EC2 GPU capacity when tasks need NVIDIA GPUs. |
| Durable databases | Usually not the first choice | Prefer managed databases such as RDS, DynamoDB, DocumentDB, ElastiCache, or MSK unless you have a strong reason to run state inside containers. |

## Mental model

| ECS concept | What it means | Kubernetes rough equivalent |
| --- | --- | --- |
| Cluster | Regional logical boundary where ECS runs tasks and services on configured capacity. | Cluster, but without a Kubernetes API surface. |
| Task definition | Versioned JSON blueprint for one or more containers, resources, IAM roles, networking mode, logging, secrets, and volumes. | Pod template plus selected parts of Deployment, ConfigMap, Secret, and volume configuration. |
| Task | A running instance of a task definition. | Pod. |
| Service | Keeps a desired number of tasks running and replaces failed or unhealthy tasks. | Deployment or ReplicaSet controller behavior. |
| Standalone task | A task run directly for finite work. | Job-like one-off Pod, but without Kubernetes Job semantics. |
| Capacity provider | Strategy for where tasks run and how infrastructure capacity is managed. | Node group, Fargate profile, or autoscaler boundary. |
| Launch type | Older direct selection of `FARGATE`, `EC2`, or `EXTERNAL`; still useful for task compatibility. | Runtime target, not a direct Kubernetes equivalent. |
| Service Connect | ECS-managed service discovery, connectivity, and traffic telemetry. | Service discovery plus service-mesh-like connectivity for ECS services. |

## Core components

### Cluster and capacity

An ECS cluster groups services and tasks. It is Regional and can use different infrastructure capacity choices:

| Capacity option | Use when | Operational notes |
| --- | --- | --- |
| ECS Managed Instances | You want AWS to manage EC2 provisioning, scaling, patching, and lifecycle while keeping EC2-style flexibility. | AWS currently recommends this for many new workloads because it balances control and operational simplicity. |
| Fargate | You want serverless container compute with no host management. | Best for variable workloads, simple operations, and teams that do not need host customization. |
| Fargate Spot | Tasks tolerate interruption. | Good for workers, development, staging, and batch jobs. Design for a two-minute interruption notice. |
| EC2 Auto Scaling group capacity provider | You need custom AMIs, instance families, GPUs, daemon processes, or host-level control. | You manage more of the instance lifecycle, but ECS can manage cluster scaling through the capacity provider. |
| External instances | You need ECS to schedule containers on infrastructure outside normal AWS managed capacity. | Useful for hybrid or edge patterns, but adds operational ownership. |

> [!TIP]
> Prefer capacity providers for launching services and tasks. Use launch types mainly to declare task-definition compatibility.

### Task definitions

A task definition is the deployable contract for a containerized workload. It defines:

- Container images and commands.
- CPU and memory at task or container level.
- Linux or Windows platform settings.
- Network mode, usually `awsvpc`.
- Port mappings and health checks.
- Log drivers and destinations.
- Environment variables and secrets.
- Task role and task execution role.
- Volumes such as EBS, EFS, or FSx where supported.

After a task definition revision is registered, ECS can run it as an ECS service or a standalone task.

### Tasks and services

Use an ECS service for long-running applications. The service scheduler maintains the desired task count and replaces tasks that fail container health checks or load balancer target health checks.

Use standalone tasks for finite work such as:

- Data backfills.
- Database migrations.
- Report generation.
- Image processing.
- Maintenance commands.
- Operational smoke tests.

Use EventBridge Scheduler when that finite work needs a one-time, rate-based, or cron-based schedule.

## Networking and traffic

### Task networking

For most workloads, use `awsvpc` network mode. In this mode, ECS gives each task its own elastic network interface and private IP address. Security groups can be applied at the task boundary, and containers in the same task can communicate over `localhost`.

| Need | ECS pattern |
| --- | --- |
| Internet-facing HTTP or HTTPS | ECS service behind an Application Load Balancer. |
| TCP or UDP traffic | ECS service behind a Network Load Balancer. |
| Private service-to-service traffic | Service Connect or AWS Cloud Map. |
| Private outbound AWS API access | Private subnets with NAT gateway or VPC endpoints. |
| Task-level firewalling | Security groups attached to task ENIs. |

> [!IMPORTANT]
> With `awsvpc`, target groups for ECS services normally use target type `ip`, because traffic is sent to task ENIs rather than instance IDs.

### Service discovery

Use Service Connect when you want ECS to manage service discovery, connection behavior, and traffic metrics. Applications can call short service names and standard ports instead of tracking task IPs directly.

Use AWS Cloud Map service discovery when you need DNS-based discovery without the Service Connect proxy behavior.

## Identity, secrets, and security

| Need | ECS control |
| --- | --- |
| Application access to AWS APIs | Task role. |
| ECS agent access to pull images and write logs | Task execution role. |
| Human or pipeline access to ECS APIs | IAM policies scoped to clusters, services, task definitions, and tags. |
| Secrets in containers | Secrets Manager or Systems Manager Parameter Store references in task definitions. |
| Network isolation | VPC subnets, route tables, security groups, private endpoints, and load balancer placement. |

> [!WARNING]
> Do not put passwords, tokens, or database credentials in plaintext environment variables. Store sensitive values in Secrets Manager or Systems Manager Parameter Store and reference them from the task definition.

## Storage

| Storage option | Use it for | Notes |
| --- | --- | --- |
| Ephemeral task storage | Temporary files, caches, scratch space. | Data disappears when the task stops. |
| Amazon EFS | Shared persistent files for Linux tasks. | Good for content, shared uploads, and horizontally scaled services that need file semantics. |
| Amazon EBS | Block storage for data-intensive tasks. | Persistence depends on task type and service usage; design carefully for replacement and failure. |
| FSx for Windows File Server | Windows shared file workloads on EC2. | Use for Windows applications that need SMB-backed shared storage. |
| FSx for NetApp ONTAP | Enterprise file workloads with NFS/SMB requirements. | Native mounting is EC2-oriented; Fargate can access data through S3 Access Points for FSx where appropriate. |
| Managed AWS data services | Databases, queues, caches, streams, object storage. | Usually the safest durability boundary for production state. |

## Deployment and scaling

| Capability | ECS approach |
| --- | --- |
| Rolling deployment | Update the ECS service to a new task definition revision. |
| Safer release with traffic validation | ECS blue/green deployment with managed traffic shifting through a load balancer or Service Connect. |
| Rollback | Revert the service to a previous task definition revision or use blue/green rollback behavior. |
| Service scaling | ECS Service Auto Scaling through Application Auto Scaling and CloudWatch metrics. |
| Cluster capacity scaling | Capacity providers, Fargate capacity, ECS Managed Instances, or Auto Scaling group capacity providers. |
| Scheduled scale changes | Scheduled actions for ECS service scaling. |

### Deploy a new image revision

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs update-service \
  --cluster production \
  --service web \
  --task-definition web:42
```

What it does: registers a new task definition revision and asks ECS to deploy that revision to the `web` service.

> [!WARNING]
> `update-service` changes live desired state. Confirm the AWS account, Region, cluster, service, image tag, and rollback revision before running it in production.

### Run a one-off task

```bash
aws ecs run-task \
  --cluster production \
  --task-definition maintenance:7 \
  --capacity-provider-strategy capacityProvider=FARGATE,weight=1 \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-abc123],securityGroups=[sg-abc123],assignPublicIp=DISABLED}"
```

What it does: starts a standalone Fargate task in selected subnets and security groups for finite maintenance work.

## Real-life ECS scenarios

| Scenario | ECS solution | Key design choices |
| --- | --- | --- |
| Public API | ECS service on Fargate behind ALB. | Private subnets, ALB health checks, task role for AWS access, target tracking on CPU or request count. |
| Internal microservices | ECS services with Service Connect. | Shared namespace, service-specific task roles, CloudWatch metrics and logs, private traffic only. |
| Queue workers | ECS service consuming SQS, MSK, or another queue. | Scale from backlog metrics, make processing idempotent, use Fargate Spot only when interruption is acceptable. |
| Scheduled jobs | EventBridge Scheduler invoking `RunTask`. | Execution role, dead-letter queue where needed, private networking, clear retry behavior. |
| Image or media processing | ECS tasks on Fargate or EC2. | Use S3 for input/output, EFS for shared intermediate files only when needed, tune CPU and memory per task. |
| GPU inference | ECS Managed Instances or EC2 GPU capacity provider. | GPU task definition requirements, GPU-capable AMI or managed capacity, model artifact storage outside the container. |
| Legacy Windows service | Windows containers on supported ECS capacity. | Confirm Windows support for chosen capacity, logging, storage, and image lifecycle. |

## Practical design checklist

- Choose ECS Managed Instances, Fargate, or EC2 capacity before writing task definitions.
- Use one ECS service per independently deployable long-running application.
- Keep task definitions small and versioned through IaC or a deployment pipeline.
- Use task roles per application permission boundary.
- Put services in private subnets unless the task itself must have a public IP.
- Use ALB for HTTP and HTTPS; use NLB for TCP, UDP, static IP, or low-level network requirements.
- Use Service Connect for ECS-native service-to-service discovery and metrics.
- Externalize durable state to managed data services where possible.
- Turn on CloudWatch logs and consider Container Insights for production services.
- Define rollback and scaling behavior before the first production deployment.

## Official documentation

- [Amazon ECS documentation](https://docs.aws.amazon.com/ecs/)
- [Amazon ECS clusters](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/clusters.html)
- [Amazon ECS task definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
- [Amazon ECS services](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html)
- [ECS launch types and capacity providers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/capacity-launch-type-comparison.html)
- [Interconnect Amazon ECS services](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/interconnecting-services.html)
- [Amazon ECS task networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking-awsvpc.html)
- [Amazon ECS storage options](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_data_volumes.html)

## Related links

- [ECS vs. EKS](ecs-vs-eks.md)
- [EKS to ECS migration](eks-to-ecs-migration.md)
- [AWS compute](README.md)
- [AWS index](../README.md)
- [Back to root index](../../../README.md)
