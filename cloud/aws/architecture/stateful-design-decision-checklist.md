# Stateful design decision checklist

## Purpose

Use this checklist before running stateful workloads, network appliances, databases, brokers, or workflow systems on AWS.

## Classification questions

| Question | Why it matters |
| --- | --- |
| What exact state exists? | Avoid vague labels such as "the app is stateful." |
| Where is the state stored? | Recovery depends on the storage boundary. |
| Is the state authoritative or rebuildable? | Authoritative state needs stronger durability. |
| Is the state local or shared? | Local state makes replicas harder to replace. |
| Which failure must it survive? | Process, host, AZ, Region, and operator error require different designs. |
| What are RPO and RTO? | Backup and failover choices need measurable targets. |
| How is split brain prevented? | Stateful leaders require fencing or quorum discipline. |

## Stateful AWS examples

| Area | Example | Design concern |
| --- | --- | --- |
| Networking | NAT Gateway, Security Group tracking, Network Firewall stateful engine. | Flow state and symmetric routing. |
| Storage | EBS, EFS, S3. | Durability, backup, access mode, and deletion protection. |
| Databases | RDS, Aurora, DynamoDB, self-managed MongoDB. | Replication, backup, failover, and consistency. |
| Streaming | Amazon MSK. | Partitions, offsets, broker health, and replay. |
| Workflows | Step Functions. | Execution history, retries, and timeout behavior. |
| Kubernetes | StatefulSet with PVC. | Stable identity does not replace application-level replication. |

## Network-state checklist

- Security Groups are stateful and allow tracked return traffic.
- Network ACLs are stateless and need both directions permitted.
- Stateful firewalls must see both directions of a flow.
- Transit Gateway appliance mode and Gateway Load Balancer stickiness can help preserve flow path.
- VPC Flow Logs can show accept/reject decisions but do not replace route, firewall, and app logs.

## Data-state checklist

- Backups are separate from replication.
- Restore procedures are tested, not assumed.
- Encryption and access policies cover the state store.
- Lifecycle policies do not delete required recovery points.
- Scale-in procedures protect leaders, partitions, and attached volumes.
- Monitoring covers replication lag, disk, quorum, and failed backups.

## Kubernetes-state checklist

- StatefulSet identity is required and understood.
- The StorageClass topology mode matches the workload.
- EBS volumes and Pods land in compatible Availability Zones.
- Operators or application logic handle replication and failover.
- Pod disruption budgets and maintenance windows protect quorum.
- PVC deletion and reclaim policies are intentional.

> [!WARNING]
> A StatefulSet gives Pods stable names and storage association. It does not automatically make PostgreSQL, Kafka, MongoDB, or another database highly available.

## Related links

- Official documentation: [Kubernetes StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- Official documentation: [Amazon EBS volume attachment](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-attaching-volume.html)
- [Stateful vs. stateless](stateful-vs-stateless.md)
- [Stateless application patterns](stateless-application-patterns.md)
- [Stateful networking](../networking/stateful-networking.md)
- [Stateful workloads](../../../kubernetes/core-objects/stateful-workloads.md)
- [Back to AWS architecture](README.md)
- [Back to AWS index](../README.md)
- [Back to root index](../../../README.md)
