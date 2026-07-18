# EKS to MSK applications

## Purpose

Use this guide to connect Kubernetes applications on EKS to Amazon MSK.

## Connection checklist

| Area | Check |
| --- | --- |
| Networking | EKS nodes or Pods can reach MSK broker endpoints through VPC routing and security groups. |
| Authentication | Client mechanism matches the MSK cluster configuration. |
| Configuration | Bootstrap brokers, TLS, credentials, and topic names are environment-specific. |
| Scaling | Consumer replicas do not exceed useful partition parallelism. |
| Operations | Consumer lag and application errors have clear owners. |

## Application design

- Keep producers idempotent where retries can duplicate writes.
- Commit consumer offsets after side effects are safe.
- Use dead-letter topics for events that cannot be processed.
- Avoid using Kafka as the only database for business state unless replay, retention, and recovery are designed.

## Related links

- [Amazon MSK](../cloud/aws/databases/amazon-msk.md)
- [Kafka fundamentals](../databases/kafka/fundamentals.md)
- [Kafka operations](../databases/kafka/operations.md)
- [Kubernetes on AWS](kubernetes-on-aws.md)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
