# Stateless application patterns on AWS

## Purpose

Use this guide to move application compute toward replaceable, horizontally scalable replicas while keeping required state in services designed to persist, replicate, secure, and recover it.

## Core rule

```text
If a replica can be destroyed and recreated without losing required
information or continuity, it behaves as stateless compute.
```

Stateless does not mean the application has no data. It means the compute instance does not privately own required history.

## How it works

Stateless compute moves durable state out of the replica and into shared services.

```text
ALB
  -> app replica A
  -> app replica B
  -> app replica C
        |
        +-> DynamoDB, RDS, S3, ElastiCache, SQS, MSK, Step Functions
```

Any healthy replica can serve the next request because required state is retrieved from shared stores or included in the request.

## Components

| Component | Role |
| --- | --- |
| Load balancer | Routes requests only to healthy replicas. |
| Auto Scaling group, ECS service, or Kubernetes Deployment | Maintains replaceable compute capacity. |
| Shared data store | Holds authoritative state. |
| Configuration store | Provides reproducible runtime settings. |
| Secret store | Provides credentials without baking them into images. |
| Queue or workflow service | Holds work while workers remain replaceable. |
| Observability pipeline | Keeps logs and metrics after a replica is gone. |

## State inventory

| State type | Avoid storing only in | Prefer |
| --- | --- | --- |
| Login session | Instance RAM or container filesystem. | Shared session store or token model. |
| User uploads | Local disk or container layer. | S3 or EFS where POSIX access is required. |
| Job progress | Process memory. | DynamoDB, RDS, SQS, Step Functions, or Kafka offsets. |
| Configuration | Manual SSH changes. | Image, IaC, Parameter Store, Secrets Manager, or AppConfig. |
| Logs | Local filesystem only. | CloudWatch Logs or another centralized store. |
| Cache | Authoritative local cache. | ElastiCache, MemoryDB, or rebuildable local cache. |

## Conversion workflow

1. List every piece of state the process uses.
2. Mark each item as authoritative, derived, or disposable.
3. Move authoritative state to a managed or shared service.
4. Make configuration reproducible from code or approved runtime stores.
5. Send logs, metrics, and traces off the replica.
6. Add graceful shutdown so in-flight work drains or checkpoints.
7. Terminate a healthy replica in a controlled test.

### Prove replaceability

```bash
aws autoscaling terminate-instance-in-auto-scaling-group \
  --instance-id i-0123456789abcdef0 \
  --should-decrement-desired-capacity false
```

What it does: removes one Auto Scaling instance while keeping desired capacity, forcing replacement.

> [!WARNING]
> Run replacement tests only in an approved environment and window. Confirm the target is an interchangeable application replica, not a stateful database, broker, firewall, or manually configured singleton.

### Kubernetes replacement example

```bash
kubectl delete pod -n payments -l app=payments-api
kubectl rollout status deployment/payments-api -n payments
```

What it does: removes current application Pods and verifies that the Deployment replaces them successfully.

## AWS patterns

| Workload | Stateless pattern | Stateful dependency |
| --- | --- | --- |
| Web API on ECS or EKS | Multiple interchangeable tasks or Pods. | RDS, DynamoDB, ElastiCache, S3. |
| Background worker | Replaceable workers consuming from a queue. | SQS backlog, Kafka topic, Step Functions state. |
| Lambda function | Treat every invocation as independent. | External state in AWS services. |
| WebSocket service | Externalize connection registry and user state. | DynamoDB, API Gateway WebSocket connection IDs. |
| Batch job | Checkpoint progress externally. | S3, database, queue, or workflow engine. |

## Common traps

| Trap | Why it hurts |
| --- | --- |
| Sticky sessions as the only session strategy. | Target failure still loses local session state. |
| Writing uploads to container layers. | Data disappears when the container is replaced. |
| Treating Lambda `/tmp` as durable. | Execution environment reuse is not guaranteed. |
| Keeping logs only on instances. | Failed or replaced replicas remove diagnostic context. |
| Scaling down workers without draining. | In-flight jobs can be repeated or abandoned. |

## Validation checklist

- A new replica starts without manual SSH or console edits.
- Terminating a replica does not lose uploads, sessions, or job progress.
- Logs and metrics remain available after termination.
- Health checks remove bad replicas before users see errors.
- Graceful shutdown drains in-flight requests or checkpoints work.
- Backups protect state stores, not disposable compute nodes.

## Related links

- Official documentation: [AWS Well-Architected stateless services guidance](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_stateless.html)
- Official documentation: [AWS Lambda application design](https://docs.aws.amazon.com/lambda/latest/dg/concepts-application-design.html)
- [Stateful vs. stateless](stateful-vs-stateless.md)
- [Stateful networking](../networking/stateful-networking.md)
- [Back to AWS architecture](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
