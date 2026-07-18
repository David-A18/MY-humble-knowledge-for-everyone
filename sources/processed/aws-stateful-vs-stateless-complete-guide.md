# Stateful vs. Stateless on AWS

> A practical and detailed study guide for networking, security, compute, containers, Kubernetes, storage, databases, messaging, APIs, workflows, scaling, resiliency, and architecture design.

**Last reviewed:** 18 July 2026  
**Primary scope:** AWS and Amazon EKS  
**Correct terminology:** **stateful** and **stateless** — not “statefull.”

---

## Table of contents

1. [The fundamental meaning of state](#1-the-fundamental-meaning-of-state)
2. [Stateful vs. stateless: complete comparison](#2-stateful-vs-stateless-complete-comparison)
3. [Stateful is not the same as persistent](#3-stateful-is-not-the-same-as-persistent)
4. [A system can be stateless at one layer and stateful at another](#4-a-system-can-be-stateless-at-one-layer-and-stateful-at-another)
5. [AWS networking and security](#5-aws-networking-and-security)
6. [Security Groups vs. Network ACLs](#6-security-groups-vs-network-acls)
7. [Connection tracking and ephemeral ports](#7-connection-tracking-and-ephemeral-ports)
8. [NAT Gateway and egress-only internet gateway](#8-nat-gateway-and-egress-only-internet-gateway)
9. [AWS Network Firewall](#9-aws-network-firewall)
10. [Stateful appliances, symmetric routing, Transit Gateway, and GWLB](#10-stateful-appliances-symmetric-routing-transit-gateway-and-gwlb)
11. [Load balancers, sessions, and stickiness](#11-load-balancers-sessions-and-stickiness)
12. [REST, HTTP, WebSocket, and authentication state](#12-rest-http-websocket-and-authentication-state)
13. [AWS compute: EC2, Auto Scaling, Lambda, ECS, and Fargate](#13-aws-compute-ec2-auto-scaling-lambda-ecs-and-fargate)
14. [Storage: instance store, EBS, EFS, and S3](#14-storage-instance-store-ebs-efs-and-s3)
15. [Databases, caches, queues, and streams](#15-databases-caches-queues-and-streams)
16. [Kubernetes and Amazon EKS](#16-kubernetes-and-amazon-eks)
17. [Kubernetes Deployment vs. StatefulSet](#17-kubernetes-deployment-vs-statefulset)
18. [PersistentVolume, PersistentVolumeClaim, and StorageClass](#18-persistentvolume-persistentvolumeclaim-and-storageclass)
19. [EBS and EFS considerations in EKS](#19-ebs-and-efs-considerations-in-eks)
20. [Stateful distributed-system concepts](#20-stateful-distributed-system-concepts)
21. [Retries, idempotency, and duplicate processing](#21-retries-idempotency-and-duplicate-processing)
22. [Scaling and failure recovery](#22-scaling-and-failure-recovery)
23. [Reference architectures](#23-reference-architectures)
24. [How to convert a stateful application tier into a stateless tier](#24-how-to-convert-a-stateful-application-tier-into-a-stateless-tier)
25. [Common mistakes and anti-patterns](#25-common-mistakes-and-anti-patterns)
26. [Troubleshooting guide](#26-troubleshooting-guide)
27. [Decision framework](#27-decision-framework)
28. [AWS service classification table](#28-aws-service-classification-table)
29. [Interview and certification questions](#29-interview-and-certification-questions)
30. [Final rules to remember](#30-final-rules-to-remember)
31. [Official references](#31-official-references)

---

# 1. The fundamental meaning of state

A component has **state** when information from a previous event, request, packet, execution, transaction, or interaction is necessary to correctly process the next one.

A simple definition is:

- **Stateful:** the component must remember something that happened before.
- **Stateless:** the component can process the current operation without depending on private local memory of previous operations.

Consider a conversation:

```text
Request 1: Log in as Alice
Request 2: Show my profile
```

A stateful server may remember in its own memory that the current connection belongs to Alice. When the second request arrives, it uses that stored session.

A stateless server expects the second request to include proof of identity, such as a token:

```http
GET /profile
Authorization: Bearer <token>
```

The server can validate the token and process the request without depending on the same server having processed the login.

## The most important correction

**Stateless does not mean “the application has no data.”**

A stateless application server may read and write large amounts of data in:

- Amazon DynamoDB
- Amazon RDS or Aurora
- Amazon S3
- Amazon EFS
- Amazon ElastiCache or MemoryDB
- Amazon SQS
- Amazon MSK

The server is stateless because the important information is not owned only by that particular server instance.

A common AWS design is therefore:

```text
Stateless and replaceable compute
                +
Managed stateful data services
```

AWS Well-Architected guidance recommends making services stateless where possible because stateless application nodes are easier to scale horizontally and replace after failures.[1]

---

# 2. Stateful vs. stateless: complete comparison

| Characteristic | Stateful | Stateless |
|---|---|---|
| Remembers previous interactions | Yes | Not in private local application state |
| Current request depends on earlier requests | Often | Ideally no |
| Typical state location | RAM, local disk, persistent volume, session store, database, connection table, execution history | Current request or an external shared service |
| Instance identity matters | Often | Usually not |
| Replacement of an instance | Requires recovery, reattachment, synchronization, or session migration | Usually terminate and recreate |
| Horizontal scaling | Requires coordination, partitioning, replication, or affinity | Add interchangeable replicas |
| Load balancing | May require session affinity or flow stickiness | Any healthy target can normally process a request |
| Scale-in | Must protect or move state before removing a node | Remove a healthy drained instance |
| Failure effect | May lose state or require failover | Another replica can normally continue |
| Backup requirements | Usually essential | The compute node itself normally does not need backup |
| Data consistency concerns | Central concern | Usually delegated to the external state store |
| Deployment complexity | Higher | Lower |
| Recovery time | Can include restore, election, replay, or synchronization | Usually instance replacement and health check |
| Example | Database primary, Kafka broker, StatefulSet Pod, TCP connection table | REST API replica, Lambda invocation, ECS worker, EKS Deployment Pod |

## Why stateless compute is easier to operate

Assume an application has ten stateless servers behind an Application Load Balancer:

```text
ALB
 ├── app-01
 ├── app-02
 ├── app-03
 └── ...
```

If `app-03` fails:

1. The health check fails.
2. The load balancer stops routing new requests to it.
3. Auto Scaling, ECS, or Kubernetes creates a replacement.
4. The replacement reads configuration and shared state from external services.
5. It begins serving traffic.

No unique business data should need to be copied from `app-03`.

With a stateful node, the recovery process may also require:

- Finding the latest copy of the data
- Attaching the correct storage
- Replaying logs
- Electing a new leader
- Preventing two leaders from accepting writes
- Rebalancing partitions
- Rebuilding replicas
- Restoring a backup
- Reconnecting clients

---

# 3. Stateful is not the same as persistent

Several related words are frequently confused.

| Term | Meaning |
|---|---|
| **Stateful** | Remembers previous information that affects future processing |
| **Stateless** | Does not depend on private local history between operations |
| **Persistent** | Data survives the process, container, or compute resource that created it |
| **Durable** | Data is protected against defined failures with a stated reliability design |
| **Ephemeral** | Temporary and expected to disappear |
| **Replicated** | Multiple copies of state exist |
| **Highly available** | The service can continue during specified failures |
| **Backup** | A separate recoverable copy exists |
| **Cache** | A usually replaceable copy used to improve performance |

## Examples

| Example | Stateful? | Persistent? | Durable? |
|---|---:|---:|---:|
| User session in EC2 RAM | Yes | No | No |
| Security Group connection-tracking entry | Yes, at network-flow level | Temporary | Not business-data durability |
| File in a container writable layer | Possibly | No after container deletion | No |
| File on EC2 instance store | Yes if the app depends on it | Only during the instance lifetime | Not suitable as the only long-term copy |
| Record in DynamoDB | Yes | Yes | Managed durability |
| Object in S3 | Yes | Yes | Managed durability |
| Cache item in ElastiCache | Yes | Configuration-dependent | Treat as replaceable unless designed otherwise |
| StatefulSet Pod using `emptyDir` | The Pod may have identity | No persistent application data | No |
| StatefulSet Pod using EBS | Yes | Yes | Backups and application replication still matter |

## Important conclusion

A component can be:

- Stateful but non-persistent, such as an in-memory session.
- Persistent but not independently highly available, such as a single EBS-backed database server.
- Stateless while continuously reading and writing persistent data elsewhere.

---

# 4. A system can be stateless at one layer and stateful at another

Always ask:

> Stateful relative to which boundary?

The same architecture can contain multiple forms of state.

| Layer | Example state |
|---|---|
| Network flow | TCP connection, NAT translation, firewall connection table |
| Authentication | Login session, refresh token, access token, device session |
| Application | Shopping cart, wizard progress, user preferences |
| Compute process | Variables in memory, local cache, open file handles |
| Container | Writable filesystem layer |
| VM | Local files, operating-system configuration, memory |
| Storage | Blocks, files, objects |
| Database | Rows, indexes, transaction logs, locks |
| Messaging | Queued messages, offsets, ordering information |
| Workflow | Current state, completed steps, retries, execution history |
| Kubernetes | Pod identity, persistent volume binding, ordinal number |

A typical application can be described accurately as:

```text
The application tier is stateless.
The database and storage tiers are stateful.
The network devices track flows.
The whole system contains state.
```

Saying that the “entire application is stateless” is usually an oversimplification. Business applications almost always retain some form of state.

---

# 5. AWS networking and security

In networking, **state** normally means information about a traffic flow or connection.

For a TCP flow, a stateful component may track information such as:

```text
Source IP
Source port
Destination IP
Destination port
Protocol
TCP flags and connection phase
Idle timeout
NAT translation
```

The combination of source IP, source port, destination IP, destination port, and protocol is commonly called a **five-tuple**.

Example:

```text
Client 203.0.113.20:53142
        ->
Server 10.0.2.15:443
Protocol TCP
```

A stateful firewall knows that return traffic from `10.0.2.15:443` to `203.0.113.20:53142` belongs to an allowed connection.

A stateless packet filter evaluates the return packet independently. It does not automatically associate the packet with the original request.

---

# 6. Security Groups vs. Network ACLs

This is the most important AWS networking example.

| Feature | Security Group | Network ACL |
|---|---|---|
| State model | **Stateful** | **Stateless** |
| Applied to | Elastic network interface and associated resource | Subnet boundary |
| Rules | Allow only | Allow and deny |
| Return traffic | Automatically allowed for tracked permitted traffic | Must match an explicit rule |
| Direction | Inbound and outbound rule sets | Inbound and outbound rule sets |
| Rule evaluation | All applicable rules combine | Lowest numbered matching rule wins |
| Reference another Security Group | Yes | No |
| Typical role | Primary resource-level access control | Coarse subnet guardrail and explicit deny layer |

AWS documents Security Groups as stateful: responses to allowed outbound requests may return regardless of inbound rules, and responses to allowed inbound traffic may leave regardless of outbound rules.[2]

AWS documents NACLs as stateless: response traffic is not automatically allowed and must match the NACL rules in the reverse direction.[3]

## HTTPS example

A user connects to an EC2-hosted website:

```text
Client: 198.51.100.10:51844
Server: 10.0.1.20:443
```

### Security Group configuration

```text
Inbound:
Allow TCP 443 from 198.51.100.10/32
```

The request enters on destination port `443`. The Security Group tracks the connection. The server response is automatically recognized as return traffic:

```text
10.0.1.20:443 -> 198.51.100.10:51844
```

You do not create an inbound Security Group rule for client port `51844`.

### NACL configuration

Because the NACL is stateless, an illustrative rule set could be:

```text
Inbound NACL:
Allow TCP destination port 443 from 198.51.100.10/32

Outbound NACL:
Allow TCP destination ephemeral ports to 198.51.100.10/32
```

The exact ephemeral-port range depends on the operating system and client implementation. AWS recommends choosing the range appropriate to the client and use case rather than blindly copying a range.[4]

## Easy memory rule

```text
Security Group:
“I allowed this conversation, so its reply is recognized.”

Network ACL:
“I evaluate each direction separately.”
```

## Which should be the primary control?

AWS VPC guidance recommends Security Groups as the primary network-access mechanism. NACLs are useful as a secondary, coarse-grained subnet control or to express an explicit deny requirement.[5]

---

# 7. Connection tracking and ephemeral ports

## Security Group connection tracking

Security Groups use connection tracking to maintain information about traffic to and from an ENI. Rules are then applied using the connection state.[6]

Connection tracking explains why this can work:

```text
Inbound Security Group rule:
Allow TCP 443 from the internet

Outbound Security Group rule:
No explicit rule for the client's temporary port
```

The HTTPS response is allowed because it is part of the tracked flow.

### Advanced nuance

Security Groups are correctly described as stateful, but AWS also documents tracked and untracked connection behavior for particular broad rule combinations and service paths. At high scale, connection-tracking allowances and idle timeouts can become operational considerations.[6]

For normal architecture discussions and certification questions, the correct classification remains:

```text
Security Group = stateful
NACL = stateless
```

## What are ephemeral ports?

A server usually listens on a known destination port:

- HTTP: `80`
- HTTPS: `443`
- SSH: `22`
- PostgreSQL: `5432`

The client normally selects a temporary source port:

```text
Client 10.0.3.25:52716 -> Server 10.0.8.10:443
```

The response is:

```text
Server 10.0.8.10:443 -> Client 10.0.3.25:52716
```

A stateless NACL on the client subnet must permit the return traffic to the client's ephemeral destination port.

## NACL rule ordering

NACL rules are evaluated from the lowest rule number upward. The first matching rule is applied, even if a later rule contradicts it.[7]

Example:

```text
Rule 100: DENY TCP 22 from 0.0.0.0/0
Rule 200: ALLOW ALL from 0.0.0.0/0
```

SSH is denied because rule `100` matches first.

This differs from Security Groups, where allow rules are combined rather than processed as a first-match ordered list.

---

# 8. NAT Gateway and egress-only internet gateway

## NAT Gateway

A NAT Gateway is stateful at the flow and translation level.

Suppose a private EC2 instance initiates an internet connection:

```text
Private instance: 10.0.2.15:45000
NAT public address: 203.0.113.5:61000
External server: 198.51.100.8:443
```

The NAT Gateway records a translation similar to:

```text
10.0.2.15:45000 <-> 203.0.113.5:61000
```

When the external server replies, the NAT Gateway uses the mapping to send the response to the original instance.

AWS states that connections through a NAT Gateway must be initiated from the VPC side. The NAT Gateway permits outbound traffic and traffic received in response to an outbound request, which AWS explicitly describes as stateful behavior.[8][9]

### What a NAT Gateway is not

A NAT Gateway is not a general inbound publication mechanism. It does not allow an arbitrary internet client to initiate a new connection to a private EC2 instance through an existing public address.

For inbound application traffic, use a suitable service such as:

- Application Load Balancer
- Network Load Balancer
- API Gateway
- Public EC2 address, where justified

### Security controls around a NAT Gateway

You do not attach a Security Group directly to a NAT Gateway. Security is normally implemented with:

- Security Groups on workloads
- NACLs on the relevant subnets
- Route tables
- AWS Network Firewall or other inspection architecture where required

## Egress-only internet gateway

For IPv6, an egress-only internet gateway lets resources initiate outbound IPv6 connections while preventing unsolicited inbound initiation. AWS describes it as stateful because it forwards outbound traffic and returns the associated response traffic.[10]

---

# 9. AWS Network Firewall

AWS Network Firewall supports two inspection engines:

| Engine | Behavior | Typical use |
|---|---|---|
| Stateless engine | Inspects each packet in isolation | Fast IP, protocol, port, direction, and TCP-flag filtering |
| Stateful engine | Evaluates traffic in flow context | Intrusion prevention, protocol-aware rules, domain inspection, Suricata-compatible rules |

AWS states that the stateless engine examines each packet independently and does not use the context of related packets.[11]

Stateful rule groups use Suricata-compatible intrusion-prevention specifications and can inspect traffic as part of a flow.[12]

## Example

A stateless rule can express:

```text
Drop every packet from source 198.51.100.50.
```

A stateful rule can reason about a flow:

```text
Allow an established TCP flow to an approved destination,
while inspecting application protocol behavior for a malicious signature.
```

## Stateless default actions and stateful processing

A firewall policy can send packets that do not match stateless rules to the stateful engine. This enables architectures in which simple filters happen first and deeper inspection happens afterward.

## Why symmetric routing is critical

The stateful engine must see both directions of the flow to maintain correct connection state. AWS Network Firewall documentation states that symmetric routing is required for stateful inspection.[13]

Bad path:

```text
Forward packet  -> Firewall endpoint A
Return packet   -> Firewall endpoint B
```

Potential result:

- Firewall B has no record of the original flow.
- The return packet may be dropped or incorrectly inspected.
- Troubleshooting appears inconsistent because only one direction is visible at each appliance.

Correct objective:

```text
Forward and return packets traverse the same stateful inspection path.
```

---

# 10. Stateful appliances, symmetric routing, Transit Gateway, and GWLB

## Stateful network appliance

Examples include:

- Third-party firewall
- IDS/IPS appliance
- Deep-packet-inspection system
- Proxy with connection state
- AWS Network Firewall endpoint

A stateful appliance usually needs both directions of a flow to pass through the same logical appliance path.

## Transit Gateway appliance mode

AWS Transit Gateway appliance mode is important when traffic is routed through a stateful appliance VPC. AWS states that appliance mode selects a network interface for the lifetime of a flow, helping maintain the required routing behavior.[14]

Without suitable appliance-mode and routing design, different Availability Zone paths can create asymmetric routing.

## Gateway Load Balancer flow stickiness

Gateway Load Balancer distributes network flows to virtual appliances. Flow stickiness is configured at the target-group level.[15]

The usual five-tuple is:

```text
Source IP
Source port
Destination IP
Destination port
Protocol
```

Flow stickiness keeps packets belonging to the same flow associated with an appliance target. This is essential when the appliance maintains a state table.

## Design rule

When introducing any stateful network appliance, explicitly validate:

1. The forward route.
2. The return route.
3. Availability Zone behavior.
4. Transit Gateway appliance mode.
5. GWLB flow stickiness.
6. Failure behavior when an appliance target becomes unhealthy.
7. Session draining and connection reset behavior.
8. Logging for both traffic directions.

---

# 11. Load balancers, sessions, and stickiness

A load balancer and the application behind it must be classified separately.

## Load-balancer connection state vs. application session state

An Application Load Balancer is a managed proxy that accepts client connections and sends requests to targets. It necessarily handles connection and request context. However, it is not automatically the owner of your shopping cart, authenticated user session, or workflow progress.

Your backend can still be either:

- Stateless
- Stateful
- Partially stateful

## Stateless backend

```text
Request 1 -> Server A
Request 2 -> Server C
Request 3 -> Server B
```

All requests succeed because any server can validate the request and obtain shared data.

## Stateful backend with local sessions

```text
Login request -> Server A
Server A stores session in RAM
Next request -> Server B
Server B does not know the session
```

Possible symptoms:

- User appears logged out intermittently.
- Shopping cart contents disappear.
- Multi-step forms restart.
- WebSocket or long-polling behavior becomes inconsistent.

## Sticky sessions

An ALB normally routes requests independently, but AWS supports sticky sessions, also called session affinity, to bind a user's session to a target for a period.[16]

```text
User A -> Server 1
User B -> Server 2
User C -> Server 3
```

### Advantages

- Can support legacy applications that store temporary session data locally.
- Reduces immediate refactoring effort.
- Useful when a protocol or application genuinely requires affinity.

### Disadvantages

- Server failure can still lose the local session.
- Traffic may become uneven.
- Scale-in becomes more delicate.
- Deployments require draining active sessions.
- Availability depends more heavily on a particular target.
- It can hide an architectural problem rather than solve it.

### Preferred pattern for common web applications

```text
Client
  ->
Application Load Balancer
  ->
Interchangeable application replicas
  ->
Shared session store such as DynamoDB, ElastiCache, or MemoryDB
```

The system still has session state, but the application servers do not privately own it.

---

# 12. REST, HTTP, WebSocket, and authentication state

## Stateless HTTP API

Each request includes the information needed to authorize and process it:

```http
GET /orders/123
Authorization: Bearer <access-token>
```

Any healthy API replica can:

1. Validate the token.
2. Read order `123` from a database.
3. Apply authorization rules.
4. Return the result.

The API node does not need the previous request to be routed to the same process.

## Server-side session API

The login creates a session record:

```text
session-789:
  user = alice
  roles = [buyer]
  cart = [item-1, item-4]
```

Later requests send:

```http
Cookie: session-789
```

This design can still have stateless compute if `session-789` is stored in a shared system. It becomes locally stateful if only one server's RAM contains the record.

## Token-based authentication is not “no state”

A self-contained access token can reduce server-side session lookup, but the wider security system may still retain state for:

- Refresh tokens
- Revocation
- User accounts
- Device sessions
- MFA enrollment
- Key rotation
- Risk decisions
- Logout invalidation

Therefore, token-based authentication is often stateless **per API request**, not state-free as a complete identity system.

## WebSocket

A WebSocket creates a long-lived bidirectional connection. API Gateway documentation describes WebSocket APIs as stateful frontends, unlike normal REST request-response interaction.[17]

Typical state includes:

- Connection ID
- Connected user
- Connected room or channel
- Subscription list
- Last heartbeat
- Connection time

A scalable WebSocket architecture often externalizes connection metadata:

```text
API Gateway WebSocket
       ->
Lambda handlers
       ->
DynamoDB connection registry
```

When a message must be pushed to a user, the backend retrieves one or more connection IDs and calls the API Gateway management endpoint.

---

# 13. AWS compute: EC2, Auto Scaling, Lambda, ECS, and Fargate

## Is EC2 stateful or stateless?

**EC2 is neither inherently stateful nor inherently stateless.**

The classification depends on how the instance is used.

### Stateful EC2 design

```text
EC2 instance
- User sessions in RAM
- Uploaded files on local disk
- Application database on the instance
- Manually edited configuration
- Cron-job progress stored locally
- Unique fixed hostname required by the application
```

Replacement can fail because the application depends on that specific machine.

### Stateless EC2 design

```text
EC2 instance
- Immutable AMI or repeatable bootstrap
- Configuration from Parameter Store or AppConfig
- Secrets from Secrets Manager
- Sessions in DynamoDB or ElastiCache
- Files in S3 or EFS
- Data in RDS, Aurora, or DynamoDB
- Logs in CloudWatch Logs
- Jobs in SQS
```

The instance can be recreated from declared configuration.

## EC2 Auto Scaling

Auto Scaling works best when instances are interchangeable.

Expected behavior:

```text
Instance A fails
    ->
Health check detects failure
    ->
Auto Scaling launches Instance D
    ->
Instance D bootstraps and becomes healthy
```

A stateful application tier can block this process if:

- The terminated node contained the only copy of a file.
- An IP allowlist depends on a specific private IP.
- Sessions are stored in local RAM.
- Software was installed manually and is missing from the AMI.
- A singleton job runs without distributed locking.
- Scale-in terminates a node with unfinished work.

## Lambda

The normal Lambda programming model should be treated as stateless compute. AWS design guidance includes implementing statelessness in functions.[18]

A Lambda invocation should obtain state from:

- The event itself
- DynamoDB
- S3
- RDS or Aurora
- SQS
- Step Functions
- Another external service

### Execution-environment reuse

AWS may reuse a Lambda execution environment. Global variables, connections, or `/tmp` content can sometimes remain available between invocations. AWS also documents that environments may be frozen and thawed for reuse.[19]

This reuse is an optimization, not a persistence guarantee.

Correct:

```text
Reuse a database connection when available.
Recreate it when not available.
```

Incorrect:

```text
Invocation 2 will always run in the same environment as Invocation 1.
```

AWS explicitly advises not relying on function instances being long-lived and to store application state elsewhere.[20]

## ECS and Fargate

Containers have a writable layer. AWS ECS documentation states that files created, modified, or deleted in that writable layer disappear when the container terminates.[21]

### Stateless ECS task

```text
Task receives SQS message
Task downloads an object from S3
Task processes it
Task stores the result in S3
Task deletes the message
Task terminates
```

The task can run anywhere with the required IAM permissions and networking.

### Stateful ECS task

```text
Task runs a database
Task requires persistent storage
Task must reconnect to the correct volume
Task must shut down consistently
Task needs backup and replication planning
```

ECS supports persistent storage options including EFS and, in supported configurations, EBS and FSx options.[22]

## Container principle

Treat the container filesystem as disposable unless a named persistent volume or external storage service explicitly provides persistence.

---

# 14. Storage: instance store, EBS, EFS, and S3

Storage services are intentionally stateful because their purpose is to retain data. However, the persistence and access model differs.

| Storage | Model | Typical use | Important state consideration |
|---|---|---|---|
| EC2 RAM | Memory | Process data, caches | Lost when process or instance ends |
| Instance store | Temporary local block | Scratch data, buffers, rebuildable cache | Lost on stop, hibernate, or terminate |
| EBS | Persistent block | Boot disk, databases, filesystems | Attached within an Availability Zone; lifecycle settings matter |
| EFS | Shared file | Multi-instance and multi-container shared files | Multiple clients can mount the filesystem |
| S3 | Object | Documents, images, backups, data lake | Accessed through object APIs, not a normal block disk |

## EC2 instance store

AWS states that instance-store data survives a reboot but does not survive instance stop, hibernation, or termination. Long-term data must be copied to persistent storage such as EBS, S3, or EFS.[23]

Good uses:

- Temporary processing workspace
- Rebuildable cache
- Distributed system replica where loss is tolerated
- High-speed scratch data with external source of truth

Bad use:

- The only copy of customer uploads
- The only database copy
- The only checkpoint for a long-running job

## Amazon EBS

EBS provides persistent block storage that can outlive the running life of an EC2 instance.[24]

Important details:

- The EBS volume and attached EC2 instance must normally be in the same Availability Zone.[25]
- A root or data volume can be deleted or retained at instance termination depending on `DeleteOnTermination` settings.
- Snapshots provide point-in-time backup capability.
- Persistent does not automatically mean the application is highly available.

A database on one EC2 instance with one EBS volume is stateful and persistent, but the architecture still needs:

- Backup
- Restore testing
- Monitoring
- Failover strategy
- Application-consistent snapshots or native database backup
- Recovery-time and recovery-point objectives

## Amazon EFS

EFS provides shared elastic file storage that multiple clients can mount over NFS.[26]

EFS is useful when multiple stateless compute nodes need access to the same files:

```text
ECS Task A ---\
ECS Task B ----> EFS shared filesystem
EKS Pod C  ---/
```

Using EFS may remove local file ownership from compute, but the application still needs to handle:

- Concurrent writers
- File locking
- Directory permissions
- Throughput behavior
- Small-file workload characteristics
- Backup and lifecycle requirements

## Amazon S3

S3 is object storage. It is often the preferred location for user uploads, static assets, exports, logs, backups, and data-lake objects.

Moving uploads from local EC2 disk to S3 is a common step in converting an application tier from stateful to stateless.

---

# 15. Databases, caches, queues, and streams

## Databases are stateful by design

Examples:

- Amazon RDS
- Amazon Aurora
- Amazon DynamoDB
- Amazon DocumentDB
- Amazon Neptune
- Amazon OpenSearch Service

They retain records, indexes, transaction information, or search state.

The design question is not whether the database is stateful. It is:

- How is data replicated?
- What consistency model is required?
- How is failover handled?
- How are backups and point-in-time recovery configured?
- What are the recovery objectives?
- How are schema changes deployed?
- How are connections managed during failover?

## Cache state

ElastiCache or MemoryDB may store:

- User sessions
- Frequently read objects
- Distributed locks
- Rate-limit counters
- Leader-election information
- Computed results

A cache is stateful because it remembers data, but you must decide whether that state is:

- Rebuildable
- Authoritative
- Persistent
- Replicated
- Acceptable to lose

A critical rule is:

> Do not call something “only a cache” if losing it would lose the only copy of important business data.

## SQS queue state

SQS retains messages until they are consumed, expire, or are removed. AWS describes queue messages as redundantly stored across multiple SQS servers.[27]

The queue is stateful even when its workers are stateless.

```text
SQS queue: stateful work backlog
Workers: stateless and horizontally scalable
```

This is a powerful AWS pattern:

1. Producers place tasks in SQS.
2. Many interchangeable workers receive tasks.
3. Each worker writes results externally.
4. Failed processing becomes visible again after the visibility timeout.

## Kafka and Amazon MSK

Kafka is stateful because brokers retain an ordered event log and consumers maintain offsets.

Stateful concerns include:

- Partition leadership
- Replicas
- In-sync replicas
- Consumer-group offsets
- Rebalancing
- Disk capacity
- Retention
- Ordering
- Recovery after broker loss

Applications consuming Kafka can still be stateless if their durable progress and materialized state are managed externally or by Kafka's mechanisms.

## Workflow state

AWS Step Functions uses state machines to orchestrate distributed applications and records workflow progress and execution history.[28]

A common design is:

```text
Step Functions: stateful orchestration
Lambda: stateless task execution
DynamoDB/S3/RDS: persistent business state
```

---

# 16. Kubernetes and Amazon EKS

Kubernetes continuously reconciles actual state toward desired state. The control plane itself manages cluster state, but application workloads can be stateless or stateful.

## Stateless Kubernetes workload

Examples:

- REST API
- Web frontend
- Independent background worker
- Reverse proxy
- Metrics exporter

Characteristics:

- Replicas are interchangeable.
- A replacement Pod does not need the old Pod's hostname.
- Important data is externalized.
- Horizontal Pod Autoscaler can add and remove replicas.
- Rolling updates are straightforward.

## Stateful Kubernetes workload

Examples:

- PostgreSQL
- MySQL
- Kafka
- ZooKeeper-like coordination system
- RabbitMQ
- Elasticsearch/OpenSearch nodes
- Stateful game server

Characteristics may include:

- Stable Pod identity
- Stable network name
- One persistent volume per replica
- Ordered startup or termination
- Leader and replica roles
- Quorum requirements
- Controlled upgrades

---

# 17. Kubernetes Deployment vs. StatefulSet

| Feature | Deployment | StatefulSet |
|---|---|---|
| Primary use | Stateless applications | Stateful applications |
| Pod names | Generated and replaceable | Stable ordinal identities such as `db-0`, `db-1` |
| Replica interchangeability | Expected | Not always |
| Stable network identity | No guarantee per replica | Yes, with stable identity semantics |
| Persistent storage | Can use it, but no automatic unique identity semantics | Commonly one claim per Pod through `volumeClaimTemplates` |
| Startup and termination ordering | Not identity-ordered | Ordered guarantees are available |
| Rolling updates | Generic replica update | Ordered and identity-aware behavior |
| Typical example | Web API | Database or broker cluster |

Kubernetes documents StatefulSet as the workload object for applications needing persistent storage or stable, unique network identity. It maintains a sticky identity for its Pods.[29]

## Deployment example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orders-api
  template:
    metadata:
      labels:
        app: orders-api
    spec:
      containers:
        - name: api
          image: example/orders-api:1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: ORDERS_TABLE
              value: orders
```

Possible Pod names:

```text
orders-api-6c57f7d6b9-a8d2k
orders-api-6c57f7d6b9-g9p4m
orders-api-6c57f7d6b9-z1q7n
```

The names do not represent permanent identities.

## StatefulSet example

```yaml
apiVersion: v1
kind: Service
metadata:
  name: database
spec:
  clusterIP: None
  selector:
    app: database
  ports:
    - name: database
      port: 5432
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
spec:
  serviceName: database
  replicas: 3
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      containers:
        - name: database
          image: example/database:1.0.0
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: data
              mountPath: /var/lib/database
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes:
          - ReadWriteOnce
        storageClassName: gp3
        resources:
          requests:
            storage: 20Gi
```

Stable identities:

```text
database-0
database-1
database-2
```

Stable storage relationship:

```text
database-0 -> data-database-0
database-1 -> data-database-1
database-2 -> data-database-2
```

## StatefulSet does not create database replication

StatefulSet gives orchestration primitives. It does not automatically provide:

- Database replication
- Leader election
- Quorum
- Transaction consistency
- Backups
- Point-in-time recovery
- Split-brain protection
- Application-aware failover

Those responsibilities belong to the database, an operator, or another management system.

---

# 18. PersistentVolume, PersistentVolumeClaim, and StorageClass

## PersistentVolume

A PersistentVolume is a cluster storage resource representing actual storage capacity.

## PersistentVolumeClaim

A PersistentVolumeClaim is a workload's request for storage.

Example:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: application-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
  storageClassName: gp3
```

## StorageClass

A StorageClass defines how storage is dynamically provisioned.

Typical EKS examples include:

- EBS CSI-backed class for block storage
- EFS CSI-backed class for shared filesystem access

## `WaitForFirstConsumer`

Kubernetes supports `volumeBindingMode: WaitForFirstConsumer`, which delays provisioning and binding until a Pod using the claim exists. This permits topology-aware scheduling decisions.[30]

Example:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
parameters:
  type: gp3
```

This is especially relevant for zonal storage such as EBS.

---

# 19. EBS and EFS considerations in EKS

## EBS-backed persistent volumes

EBS is block storage and is normally associated with one Availability Zone. AWS EKS guidance states that Pods requiring an EBS persistent volume must be scheduled in the same Availability Zone as the volume.[31]

Potential failure scenario:

```text
EBS volume exists in eu-west-1a
Pod can run only on nodes in eu-west-1b
Result: Pod remains Pending because the volume cannot attach there
```

Useful checks:

```bash
kubectl get pod -o wide
kubectl describe pod <pod-name>
kubectl get pvc
kubectl describe pvc <claim-name>
kubectl get pv
kubectl get nodes --show-labels
```

Look for messages such as:

- Volume node affinity conflict
- FailedAttachVolume
- FailedMount
- FailedScheduling
- CSI authorization errors

## EFS-backed persistent volumes

EFS offers a shared NFS filesystem that can be mounted by multiple Pods and nodes.

Good uses:

- Shared user uploads
- Shared content
- Models or artifacts read by many Pods
- Applications requiring a common filesystem namespace

Cautions:

- Shared storage does not eliminate application-level locking requirements.
- Multiple writers can create race conditions.
- Database engines may require specific filesystem semantics and performance validation.
- A shared filesystem can become a broad failure or performance dependency.

## Choosing EBS vs. EFS

| Requirement | Usually consider |
|---|---|
| Block device for one stateful replica | EBS |
| Database volume with frequent block I/O | EBS |
| Same filesystem mounted by many Pods | EFS |
| Access across nodes and Availability Zones | EFS |
| Lowest-latency node-local scratch data | Ephemeral or instance storage, only if loss is acceptable |
| Object uploads and downloads | S3 rather than forcing object data into a filesystem |

---

# 20. Stateful distributed-system concepts

Stateful systems require concepts beyond simply attaching a disk.

## Replication

Replication creates multiple copies of data.

```text
Primary -> Replica A
        -> Replica B
```

Questions:

- Is replication synchronous or asynchronous?
- Can acknowledged data be lost during failover?
- How far behind can a replica be?
- How is a failed replica rebuilt?

## Leader election

Some systems allow one leader to coordinate writes.

```text
Node A = leader
Node B = follower
Node C = follower
```

If A fails, B or C may become leader.

The design must prevent two nodes from both believing they are leader.

## Split brain

Split brain happens when isolated parts of a system independently accept conflicting authority.

Possible causes:

- Network partition
- Incorrect health checks
- Slow storage
- Broken quorum design
- Manual failover while the old primary is still active

## Quorum

A quorum requires enough participants to agree before an operation is accepted.

In a three-member system, two members may be needed for a majority. Losing one may preserve availability; losing communication between members can stop writes to protect consistency.

## Partitioning and sharding

State is divided across nodes:

```text
Partition 0 -> Node A
Partition 1 -> Node B
Partition 2 -> Node C
```

Scaling requires moving or rebalancing partitions, not simply adding an empty server.

## Checkpointing

A long-running job periodically saves progress externally:

```text
Processed records: 8,000,000
Last committed offset: 7,999,500
Checkpoint stored in DynamoDB or S3
```

If the worker fails, another worker resumes from the checkpoint rather than starting from zero.

## Distributed locking

When multiple stateless replicas can execute the same operation, a shared lock or conditional-write mechanism may be necessary.

Examples:

- Only one scheduler runs a settlement job.
- Only one worker updates a shared resource.
- Only one deployment performs a migration.

Locks must include:

- Ownership
- Expiration or lease
- Renewal
- Fencing or stale-owner protection
- Failure handling

---

# 21. Retries, idempotency, and duplicate processing

Distributed systems retry operations because networks and processes fail.

A timeout does not prove that an operation failed. The operation may have succeeded while the response was lost.

## Payment example

```text
Client sends payment request
Payment succeeds
Response is lost
Client retries
```

Without protection, the customer may be charged twice.

## Idempotency key

```http
POST /payments
Idempotency-Key: order-123-payment-1
```

The service stores:

```text
order-123-payment-1 -> completed -> transaction-456
```

A retry returns the existing result.

## Idempotent operations

An operation is idempotent when repeating the same intended request does not create additional unintended effects.

Examples:

- Set a resource's desired value to `enabled`.
- Create an order only if an idempotency key does not already exist.
- Store an event result using a unique event ID and conditional write.

Non-idempotent example:

```text
Increment balance by 10
```

Retried twice, it increments by 20 unless deduplicated.

## SQS and duplicate-safe consumers

Standard SQS queues use at-least-once delivery behavior, so consumers should be able to handle duplicate delivery.[32]

A reliable worker pattern:

1. Read message with unique operation ID.
2. Check or conditionally record operation ID.
3. Perform the operation.
4. Store the result.
5. Delete the message only after successful completion.

Stateless workers still require stateful deduplication and progress tracking.

---

# 22. Scaling and failure recovery

## Stateless scale-out

```text
3 API replicas
   -> traffic increases
20 API replicas
   -> traffic decreases
4 API replicas
```

Requirements:

- Configuration is repeatable.
- No unique local data exists.
- Health checks reflect readiness.
- Shutdown drains in-flight work.
- Sessions and files are externalized.

## Stateful scale-out

Adding a stateful node can require:

1. Provision storage.
2. Join the cluster.
3. Copy or stream existing data.
4. Rebalance partitions.
5. Update membership.
6. Verify consistency.
7. Begin serving reads or writes.

## Stateless failure

```text
Pod A fails
Load balancer stops routing to A
Pod B and C continue
Kubernetes creates Pod D
```

Recovery is mainly compute replacement.

## Stateful failure

```text
Database primary fails
Detect failure
Confirm fencing of old primary
Select and promote replica
Redirect clients
Rebuild failed node
Resynchronize data
```

Recovery concerns both service availability and data correctness.

## Scaling down stateful systems

Before removing a stateful node, you may need to:

- Transfer leadership
- Drain client connections
- Move partitions
- Confirm replicas are synchronized
- Remove cluster membership
- Detach or snapshot storage
- Preserve backup requirements

A generic Auto Scaling termination is not sufficient for many stateful systems.

---

# 23. Reference architectures

## Architecture A: stateless three-tier web application

```text
Users
  ->
Route 53
  ->
CloudFront and AWS WAF
  ->
Application Load Balancer
  ->
EC2 Auto Scaling / ECS / EKS Deployment
  ->
RDS or DynamoDB
  ->
S3 for objects
  ->
ElastiCache for shared cache or sessions
```

State classification:

| Component | State role |
|---|---|
| Application replicas | Stateless |
| RDS/DynamoDB | Stateful source of business data |
| S3 | Stateful object storage |
| ElastiCache | Stateful shared cache/session tier |
| ALB | Connection/request handling; not primary business-session owner |

## Architecture B: asynchronous worker system

```text
Producer -> SQS -> ECS/Lambda/EKS workers -> DynamoDB/S3
```

State classification:

- SQS stores the work backlog.
- Workers are interchangeable.
- DynamoDB or S3 stores durable results.
- Deduplication state prevents duplicate effects.

Advantages:

- Backpressure through queue depth
- Independent producer and consumer scaling
- Failure retry
- Replaceable workers

## Architecture C: WebSocket chat

```text
Clients
  ->
API Gateway WebSocket
  ->
Lambda route handlers
  ->
DynamoDB connection and room registry
  ->
API Gateway Management API for callbacks
```

State classification:

- WebSocket connections are stateful.
- Lambda handlers remain stateless.
- Connection metadata is externalized.
- Chat history is stored in a database.

## Architecture D: EKS stateful database

```text
StatefulSet
 ├── database-0 + EBS volume 0
 ├── database-1 + EBS volume 1
 └── database-2 + EBS volume 2
```

Additional required design:

- Database-native replication
- Quorum
- Pod disruption budgets
- Anti-affinity or topology spread
- Correct EBS topology
- Backups outside the cluster
- Restore testing
- Operator or documented failover process

## Architecture E: stateful firewall inspection

```text
Workload VPC
   ->
Transit Gateway
   ->
Inspection VPC
   ->
GWLB / AWS Network Firewall
   ->
Destination
```

Required properties:

- Forward and return symmetry
- Appliance mode where appropriate
- Flow stickiness
- Multi-AZ route validation
- Failure-path testing
- Firewall logging

---

# 24. How to convert a stateful application tier into a stateless tier

Consider a legacy EC2 application that stores:

- Sessions in RAM
- Uploads in `/var/www/uploads`
- Configuration in local files
- Scheduled jobs in cron
- Logs in `/var/log/app`

## Step 1: inventory all state

Search for:

- Local files
- In-memory sessions
- Local database files
- Temporary files that are actually required
- Cron state
- Queue or job progress
- Generated reports
- Local secrets
- Manual configuration
- IP-based assumptions

Classify each item:

| State | Authoritative? | Must survive replacement? | Shared? | Destination |
|---|---:|---:|---:|---|
| User uploads | Yes | Yes | Yes | S3 or EFS |
| HTTP sessions | Temporary but required | Yes during session | Yes | DynamoDB/ElastiCache/MemoryDB |
| Application config | Yes | Yes | Yes | Parameter Store/AppConfig/image |
| Secrets | Yes | Yes | Yes | Secrets Manager |
| Logs | Operational | Yes for analysis | Yes | CloudWatch Logs/S3 |
| Scratch files | No | No | No | Local ephemeral disk |
| Job progress | Yes | Yes | Yes | DynamoDB/S3/queue/workflow |

## Step 2: externalize sessions

Move local memory sessions to a shared store.

Before:

```text
User -> Server A -> local session in A
```

After:

```text
User -> Any server -> shared session store
```

## Step 3: move user files

Use:

- S3 for object-oriented access
- EFS when a shared POSIX-like filesystem is required

Do not copy files manually among Auto Scaling instances.

## Step 4: make configuration reproducible

Use:

- AMI or container image
- Infrastructure as Code
- Systems Manager Parameter Store
- AWS AppConfig
- Secrets Manager

A new instance should not require manual SSH configuration.

## Step 5: centralize logs and metrics

Send logs and metrics to managed observability systems. Do not require access to a failed server's local filesystem to diagnose production.

## Step 6: externalize background work

Replace local cron assumptions with controlled scheduling and coordination:

- EventBridge Scheduler or rules
- SQS workers
- Step Functions
- Kubernetes CronJob with concurrency policy and external locking where needed

## Step 7: implement graceful shutdown

When a node is removed:

1. Stop receiving new work.
2. Finish or checkpoint in-flight work.
3. Close connections.
4. Flush telemetry.
5. Exit before the termination deadline.

## Step 8: prove replaceability

Test by intentionally terminating a healthy application node.

Success means:

- Users do not lose important sessions.
- No uploads disappear.
- No unfinished work is silently lost.
- A replacement becomes healthy automatically.
- Logs remain available.

---

# 25. Common mistakes and anti-patterns

## Mistake 1: “Stateless means no database”

Wrong. Stateless compute commonly uses a stateful database.

## Mistake 2: “EC2 is stateful”

Incomplete. EC2 can host either design. The application and storage choices determine the result.

## Mistake 3: “EBS makes the application highly available”

EBS provides persistent block storage. High availability also requires compute recovery, application failover, data consistency, and suitable architecture.

## Mistake 4: “A StatefulSet makes PostgreSQL highly available”

StatefulSet provides stable identity and storage orchestration. PostgreSQL replication, failover, fencing, backup, and recovery remain separate responsibilities.

## Mistake 5: “Sticky sessions solve state management”

Stickiness provides affinity. It does not protect local sessions from target failure.

## Mistake 6: storing customer uploads in a container layer

The data disappears when the container is replaced.

## Mistake 7: treating Lambda environment reuse as persistence

Reuse is not guaranteed. Important state must be external.

## Mistake 8: forgetting NACL return rules

Because NACLs are stateless, a permitted request can still fail if reverse-direction ephemeral-port traffic is denied.

## Mistake 9: asymmetric routing through a stateful firewall

The firewall sees only half of the conversation and drops or misclassifies traffic.

## Mistake 10: using local caches as authoritative data

If the cache is lost and no source of truth exists, it was not merely a cache.

## Mistake 11: scaling stateful nodes like stateless replicas

Blindly terminating a database or broker can lose leadership, quorum, partitions, or data.

## Mistake 12: assuming persistent means backed up

A persistent volume can still be deleted, corrupted, encrypted by an attacker, or contain application-level corruption. Backups must be separate and tested.

---

# 26. Troubleshooting guide

## Problem: inbound connection works, response does not

Check:

1. NACL outbound rule.
2. Client ephemeral-port range.
3. Route table in both directions.
4. Stateful firewall symmetry.
5. Host operating-system firewall.
6. VPC Flow Logs.

Security Groups automatically allow tracked response traffic, but NACLs do not.[3]

## Problem: intermittent login or cart loss behind ALB

Likely causes:

- Session stored in target RAM
- Requests reach different targets
- Sticky cookie expires
- Target was replaced
- Session store has inconsistent TTL

Preferred correction:

- Move session state to a shared store.
- Treat stickiness as a compatibility mechanism, not durable state management.

## Problem: EKS Pod remains Pending with PVC

Check:

```bash
kubectl describe pod <pod>
kubectl describe pvc <pvc>
kubectl get pv -o wide
kubectl get nodes -L topology.kubernetes.io/zone
```

Possible causes:

- EBS volume and node are in different Availability Zones.
- No nodes exist in the required zone.
- EBS CSI driver is absent or unhealthy.
- IAM permissions are missing.
- StorageClass provisioner is incorrect.
- Access mode is incompatible.
- Volume attachment limit is reached.

## Problem: stateful firewall drops established traffic

Check:

- Forward and return paths
- Transit Gateway appliance mode
- GWLB stickiness
- Multiple firewall endpoints across AZs
- Route-table differences
- Connection idle timeout
- SNAT/DNAT before and after inspection

## Problem: ECS data disappears after deployment

The application wrote to the container writable layer. Move required data to:

- EFS
- EBS where supported and appropriate
- S3
- Database

## Problem: Lambda occasionally loses cached value

This is expected if the value was stored only in global memory or `/tmp`. Treat those as optional caches, not authoritative state.

## Problem: duplicate job execution

Possible causes:

- Queue redelivery
- Timeout followed by retry
- Worker crashed after side effect but before acknowledgement
- Scheduler triggered more than once

Corrections:

- Idempotency keys
- Conditional database writes
- Deduplication table
- Transactional outbox pattern
- Correct visibility timeout
- External checkpoint

## VPC Flow Logs

VPC Flow Logs capture metadata about IP traffic for VPCs, subnets, or ENIs and can help diagnose overly restrictive Security Group or NACL rules.[33]

Remember that `ACCEPT` or `REJECT` shows the decision observed by VPC controls, but complete troubleshooting can still require:

- Route inspection
- Application logs
- Firewall logs
- Load-balancer access logs
- Packet capture on an instance where permitted
- DNS verification

---

# 27. Decision framework

Ask these questions for every component.

## State ownership

1. What exact state exists?
2. Where is it stored?
3. Is it local or shared?
4. Is it authoritative or rebuildable?
5. Who is allowed to modify it?

## Lifecycle

6. Must the state survive process restart?
7. Must it survive container replacement?
8. Must it survive instance termination?
9. Must it survive Availability Zone failure?
10. Must it survive Region failure?

## Scaling

11. Can any replica process any request?
12. Can a new replica start without copying data from an old replica?
13. Can a replica be removed without moving state?
14. Is session affinity required?
15. Is partition rebalancing required?

## Consistency

16. Can two nodes update the state simultaneously?
17. What consistency level is required?
18. How are duplicate operations prevented?
19. Is ordering required?
20. What happens during a network partition?

## Recovery

21. How is state backed up?
22. How is restore tested?
23. What are RPO and RTO?
24. How is failover triggered?
25. How is split brain prevented?

## Security

26. Is state encrypted at rest and in transit?
27. Are credentials externalized?
28. Is sensitive data written to ephemeral files or logs?
29. Do network controls require stateful symmetric routing?
30. Are state stores protected with least privilege?

## Classification result

Use this practical rule:

```text
If the component can be destroyed and recreated without losing required
information or continuity, it behaves as stateless compute.

If correct future behavior depends on information privately owned by that
specific component, it is stateful at that boundary.
```

---

# 28. AWS service classification table

The table uses “typical role” rather than claiming every service has only one possible design.

| AWS component or concept | Typical classification | Explanation |
|---|---|---|
| Security Group | Stateful network filter | Tracks permitted connections and recognizes response traffic |
| Network ACL | Stateless packet filter | Each direction must be explicitly permitted |
| AWS Network Firewall stateless rules | Stateless | Each packet inspected independently |
| AWS Network Firewall stateful rules | Stateful | Flow-aware Suricata-compatible inspection |
| NAT Gateway | Stateful flow translation | Maintains outbound translation and response mapping |
| Egress-only internet gateway | Stateful egress control | Allows initiated IPv6 traffic and associated responses |
| Transit Gateway | Routing service; appliance mode supports stateful paths | Appliance mode helps maintain flow path through appliances |
| Gateway Load Balancer | Flow-aware distribution | Uses flow stickiness for virtual appliances |
| Application Load Balancer | Connection/request-aware load balancing | Backend session design remains separate |
| ALB sticky session | Stateful affinity mechanism | Binds a client session to a target temporarily |
| REST/HTTP API server | Prefer stateless | Every request should be independently processable |
| API Gateway WebSocket | Stateful connection frontend | Maintains long-lived bidirectional connections |
| EC2 | Either | Depends on application and storage design |
| EC2 Auto Scaling application tier | Prefer stateless | Instances must be replaceable |
| Lambda normal invocation | Stateless compute model | Important state should be external |
| ECS/Fargate task | Ephemeral compute by default | Container writable layer disappears with container |
| EKS Deployment | Usually stateless workload | Replicas are intended to be interchangeable |
| EKS StatefulSet | Stateful workload orchestration | Stable identity, storage association, and ordering semantics |
| EC2 instance store | Ephemeral storage | Data does not survive stop, hibernate, or terminate |
| EBS | Persistent stateful block storage | Persists independently of running instance; zonal attachment constraints |
| EFS | Shared stateful file storage | Many clients can mount shared files |
| S3 | Stateful object storage | Retains objects independently of compute |
| RDS/Aurora | Stateful relational database | Retains relational and transactional state |
| DynamoDB | Stateful NoSQL database | Retains application records |
| ElastiCache | Stateful cache/session tier | Stores shared in-memory data; durability depends on design |
| MemoryDB | Stateful in-memory database | Durable Redis-compatible data role |
| SQS | Stateful message backlog | Retains queued work while workers can remain stateless |
| MSK/Kafka | Stateful event log | Retains partitions, replicas, and offsets |
| Step Functions | Stateful orchestration | Retains workflow state and execution history |
| CloudWatch Logs | Stateful observability storage | Logs survive compute replacement according to retention settings |
| Secrets Manager | Stateful secret store | Secrets and versions exist outside compute |
| Parameter Store | Stateful configuration store | Configuration can be retrieved by replaceable compute |

---

# 29. Interview and certification questions

## Question 1

**Why are Security Groups stateful?**

Because they use connection tracking. Return traffic for an allowed connection is recognized and permitted without requiring a reverse-direction rule that independently matches the response.

## Question 2

**Why are NACLs stateless?**

They do not remember previous packets. Inbound and outbound packets are evaluated independently against ordered rules.

## Question 3

**Does a stateless API have no data?**

No. It can use databases, S3, queues, caches, and other external state stores. Stateless refers to the API replica not privately depending on previous requests.

## Question 4

**Is EC2 stateful?**

EC2 can host either type of application. A manually configured server with local files is stateful; an immutable Auto Scaling instance using external data stores can be stateless.

## Question 5

**Is Lambda always stateless?**

Treat normal Lambda invocations as stateless. Execution environments may be reused, but applications must not depend on reuse for required state.

## Question 6

**What is the difference between a Deployment and StatefulSet?**

A Deployment manages interchangeable replicas. A StatefulSet provides stable identities, persistent storage association, and ordered semantics for stateful applications.

## Question 7

**Does StatefulSet replicate database data?**

No. Replication must be implemented by the database, an operator, or another management layer.

## Question 8

**Why can an EKS Pod with an EBS PVC remain Pending?**

The EBS volume may exist in a different Availability Zone from available nodes, or the CSI driver, IAM permissions, StorageClass, or attachment constraints may be incorrect.

## Question 9

**What problem do sticky sessions solve?**

They route a client's requests to the same target for a period. They do not make locally stored session state durable or highly available.

## Question 10

**Why do stateful firewalls need symmetric routing?**

They need to observe both directions of a connection to maintain and evaluate flow state correctly.

## Question 11

**Why is idempotency important for stateless workers?**

Retries and at-least-once delivery can execute the same operation multiple times. Idempotency prevents duplicate business effects.

## Question 12

**What is the preferred high-level AWS pattern?**

Use replaceable stateless compute for application processing and managed stateful services for durable data, sessions, files, messages, and workflows.

---

# 30. Final rules to remember

## Rule 1

```text
Stateful means the component remembers something from before.
```

## Rule 2

```text
Stateless does not mean no data.
It means the compute replica does not privately own required history.
```

## Rule 3

```text
Security Group = stateful
Network ACL = stateless
```

## Rule 4

```text
Persistent is not the same as highly available or backed up.
```

## Rule 5

```text
A StatefulSet provides identity and storage orchestration,
not automatic database correctness.
```

## Rule 6

```text
Sticky sessions provide affinity, not durable session management.
```

## Rule 7

```text
Stateful network inspection requires symmetric routing.
```

## Rule 8

```text
Normal Lambda, ECS, Auto Scaling, and Deployment workloads should
externalize important state.
```

## Rule 9

```text
Queues and workflows hold state so that workers can remain stateless.
```

## Rule 10

```text
The best test of stateless compute is safe replacement:
Can I terminate this replica right now without losing required information?
```

---

# 31. Official references

The following sources were used to verify and extend this guide. AWS and Kubernetes documentation can evolve, so consult the current version when implementing production infrastructure.

1. AWS Well-Architected Framework — Make systems stateless where possible  
   https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_stateless.html

2. Amazon VPC — Security Groups  
   https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html

3. Amazon VPC — Network ACLs  
   https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html

4. Amazon VPC — Custom Network ACLs and ephemeral ports  
   https://docs.aws.amazon.com/vpc/latest/userguide/custom-network-acl.html

5. Amazon VPC — Infrastructure security guidance  
   https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html

6. Amazon EC2 — Security Group connection tracking  
   https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-connection-tracking.html

7. Amazon VPC — NACL rule processing  
   https://docs.aws.amazon.com/vpc/latest/userguide/nacl-rules.html

8. Amazon VPC — NAT Gateway  
   https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html

9. Amazon VPC — Troubleshoot NAT Gateways  
   https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-troubleshooting.html

10. Amazon VPC — Egress-only internet gateway  
    https://docs.aws.amazon.com/vpc/latest/userguide/egress-only-internet-gateway.html

11. AWS Network Firewall — Stateless rule groups  
    https://docs.aws.amazon.com/network-firewall/latest/developerguide/stateless-rule-groups-standard.html

12. AWS Network Firewall — Stateful rule groups  
    https://docs.aws.amazon.com/network-firewall/latest/developerguide/stateful-rule-groups-ips.html

13. AWS Network Firewall — Symmetric-routing troubleshooting  
    https://docs.aws.amazon.com/network-firewall/latest/developerguide/troubleshooting-general-issues.html

14. AWS Transit Gateway — Appliance mode and flow behavior  
    https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html

15. Gateway Load Balancer — Target-group flow stickiness  
    https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/edit-target-group-attributes.html

16. Application Load Balancer — Sticky sessions  
    https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html

17. API Gateway — WebSocket API overview  
    https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-websocket-api-overview.html

18. AWS Lambda — Designing Lambda applications  
    https://docs.aws.amazon.com/lambda/latest/dg/concepts-application-design.html

19. AWS Lambda — Execution-environment lifecycle  
    https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html

20. AWS Lambda — Programming model  
    https://docs.aws.amazon.com/lambda/latest/dg/foundation-progmodel.html

21. Amazon ECS — Persistent-storage best practices and container writable layer  
    https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/storage.html

22. Amazon ECS — Storage options for tasks  
    https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_data_volumes.html

23. Amazon EC2 — Instance-store data persistence  
    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-store-lifetime.html

24. Amazon EBS — EBS volumes  
    https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes.html

25. Amazon EBS — Attaching a volume in the same Availability Zone  
    https://docs.aws.amazon.com/ebs/latest/userguide/ebs-attaching-volume.html

26. Amazon EFS — What is EFS?  
    https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html

27. Amazon SQS — What is SQS?  
    https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html

28. AWS Step Functions — What is Step Functions?  
    https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html

29. Kubernetes — StatefulSets  
    https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/

30. Kubernetes — StorageClasses and `WaitForFirstConsumer`  
    https://kubernetes.io/docs/concepts/storage/storage-classes/

31. Amazon EKS Best Practices — Data plane and EBS topology  
    https://docs.aws.amazon.com/eks/latest/best-practices/data-plane.html

32. Amazon SQS — At-least-once delivery  
    https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html

33. Amazon VPC — VPC Flow Logs  
    https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html

---

## One-sentence summary

> Design application compute so that it can be safely replaced, and place required state in systems deliberately designed to persist, replicate, secure, and recover that state.
