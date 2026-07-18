# Amazon MSK

## Purpose

Use this page to understand when Amazon Managed Streaming for Apache Kafka is the right AWS home for Kafka workloads.

## What MSK manages

Amazon MSK provides managed control-plane operations for Apache Kafka clusters while applications continue to use Kafka-compatible producers, consumers, topics, and APIs.

| Area | MSK helps with | You still design |
| --- | --- | --- |
| Cluster lifecycle | Create, update, and delete clusters. | Topic strategy, schemas, producers, and consumers. |
| Availability | Multi-AZ broker placement options. | Replication factor, client retry behavior, and failure handling. |
| Security | AWS networking and authentication integrations. | Least privilege, topic authorization, and secret handling. |
| Monitoring | CloudWatch and service metrics. | Alerts, dashboards, lag ownership, and runbooks. |

## EKS client considerations

- Put clients and brokers in reachable VPC networking paths.
- Treat bootstrap broker addresses, TLS, and authentication as environment-specific configuration.
- Monitor consumer lag per consumer group.
- Keep retry and dead-letter behavior explicit in application code.

## Related links

- [Kafka fundamentals](../../../databases/kafka/fundamentals.md)
- [Kafka operations](../../../databases/kafka/operations.md)
- [EKS to MSK applications](../../../cross-topic-guides/eks-to-msk-applications.md)
- [Amazon MSK documentation](https://docs.aws.amazon.com/msk/)
- [Back to AWS databases](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
