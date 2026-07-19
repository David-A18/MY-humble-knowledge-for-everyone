# Stateful design decision checklist

## Purpose

Use this checklist before running stateful workloads, network appliances, databases, brokers, or workflow systems on AWS.

## How state changes the design

Stateful components must recover specific information after failure. That changes scaling, deployment, backup, networking, and security decisions.

```text
stateless replica failure
  -> stop routing
  -> replace replica

stateful replica failure
  -> protect data
  -> preserve quorum or leadership
  -> reattach or rebuild state
  -> verify consistency
  -> then resume traffic
```

## Components to identify

| Component | Questions to answer |
| --- | --- |
| State owner | Which service or process is authoritative? |
| Storage layer | Where does the state physically live? |
| Replication layer | How many copies exist and where? |
| Backup layer | What separate recovery copy exists? |
| Coordination layer | How are leaders, locks, or partitions assigned? |
| Network path | Do stateful network devices need symmetric flow routing? |
| Runbook | Who can fail over, restore, replay, or scale down safely? |

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

### NACL return traffic example

```text
Inbound:
allow TCP 443 from client

Outbound:
allow TCP ephemeral ports to client
```

What it does: permits both directions for a stateless Network ACL. A Security Group would track the connection, but a NACL evaluates each direction independently.

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

## Production readiness evidence

- Restore was tested from backup into an isolated environment.
- Failover was tested without creating two writers.
- Monitoring covers lag, quorum, disk saturation, and backup failures.
- Scale-in has a drain or decommission procedure.
- Security policy covers snapshots, backups, logs, and replicas.
- RPO and RTO are written down and accepted by the service owner.

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
