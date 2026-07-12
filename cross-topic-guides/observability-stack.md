# Observability stack

Status: Initial outline

## Purpose

Describe the monitoring, logging, tracing, and alerting capabilities needed for cloud and Kubernetes operations.

## Expected content

- Metrics collection.
- Log aggregation.
- Distributed tracing.
- Alert routing.
- Dashboards and SLOs.

## Design questions

- Which user journeys need SLOs?
- Which signals indicate saturation, errors, latency, and traffic?
- How long must logs and metrics be retained?
- Which alerts require immediate action?

## Related links

- [AWS CloudWatch documentation](https://docs.aws.amazon.com/cloudwatch/)
- [Kubernetes monitoring documentation](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-usage-monitoring/)
- [Back to cross-topic guides](README.md)
- [Back to root index](../README.md)
