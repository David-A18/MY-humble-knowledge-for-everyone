# Stateful vs. stateless on AWS

## Purpose

Use this page to classify AWS application components by where state lives and how that affects scaling, recovery, and operations.

## What state means

State is information from a previous request, packet, transaction, or execution that affects correct future behavior.

```text
stateful: the component must remember something
stateless: the component can process the request without private local history
```

A stateless API can still read and write large amounts of data. The difference is that durable data lives in shared systems such as RDS, DynamoDB, S3, EFS, SQS, MSK, or Step Functions instead of only inside one replaceable compute replica.

## Core distinction

| Type | Meaning | Operational effect |
| --- | --- | --- |
| Stateless component | Does not rely on local durable state to serve the next request. | Easier to replace, scale horizontally, and deploy. |
| Stateful component | Owns data or session state that must survive or stay consistent. | Needs backup, placement, failover, and careful scaling. |
| Persistent storage | Durable storage such as EBS, EFS, S3, or a database. | Persistence alone does not make an application highly available. |

## AWS examples

- Stateless web tier: ALB plus Auto Scaling group, ECS service, or Lambda backed by external data stores.
- Stateful data tier: RDS, DynamoDB, ElastiCache, MSK, EBS-backed workloads, or self-managed databases.
- Mixed design: stateless API with stateful authentication, queue, cache, database, or workflow layer.

## How replacement differs

```text
Stateless app replica fails
  -> load balancer marks it unhealthy
  -> Auto Scaling, ECS, or Kubernetes creates another
  -> new replica reads shared state

Stateful node fails
  -> failover, reattach, replay, restore, or elect
  -> verify data consistency
  -> resume traffic
```

What it does: highlights why stateful systems need runbooks and recovery tests, while stateless compute should be routinely replaceable.

## Design checklist

- Inventory all session, file, cache, queue, workflow, and database state.
- Externalize sessions and uploads before scaling application instances freely.
- Treat retries and duplicate processing as state-management concerns.
- Match recovery design to RPO and RTO, not just service names.

## Related links

- [Stateless application patterns](stateless-application-patterns.md)
- [Stateful design decision checklist](stateful-design-decision-checklist.md)
- [Stateful networking](../networking/stateful-networking.md)
- [Stateful workloads](../../../kubernetes/core-objects/stateful-workloads.md)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [Back to AWS architecture](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
