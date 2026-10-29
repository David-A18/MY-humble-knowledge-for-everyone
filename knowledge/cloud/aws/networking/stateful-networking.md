---
type: Explanation
title: Stateful networking and stateless subnet controls
description: Explain why return traffic and symmetric paths matter when security groups,
  NACLs, NAT, and appliances interact.
tags:
- aws
- networking
- connection-tracking
- network-acls
status: draft
maturity: draft
audience: Cloud and platform engineering learners
maintainer: unassigned
sources:
- id: network-acls
  title: Network ACLs
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html
- id: connection-tracking
  title: Security group connection tracking
  resource: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-connection-tracking.html
- id: nat-types
  title: NAT gateways
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html
- id: network-firewall
  title: AWS Network Firewall
  resource: https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html
- id: gateway-load-balancer
  title: Gateway Load Balancer
  resource: https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html
---

# Stateful networking

Connection state records a relationship between packets, allowing a control to recognize replies. Stateless filtering evaluates each packet independently. The difference explains why an allowed request can still have a blocked response and why a route change can disrupt an established session.

## Distinguish the components

| Component | Scope / behavior | Operational implication |
| --- | --- | --- |
| Security group | Stateful allow rules on supported resource interfaces | Reply behavior depends on tracking; inspect every attached group. |
| Network ACL (NACL) | Ordered allow/deny rules at subnet boundaries | Both directions need matching permission; first matching rule wins. |
| NAT gateway | Address/port translation for initiated flows | Tracks mappings; is not a substitute for application or identity policy. |
| Stateful inspection appliance | Evaluates flows through the configured inspection path | Forward and reverse traffic must meet that appliance's routing/state requirements. |

AWS Network Firewall provides managed inspection with stateless and stateful rule groups.[^network-firewall] Gateway Load Balancer inserts and distributes flows across virtual appliances; its flow stickiness and endpoint routing are part of the path design.[^gateway-load-balancer] These are distinct components, not additional names for a security group. Application data persistence is a separate meaning of state; see [stateful versus stateless architecture](../architecture/stateful-vs-stateless.md).

A NACL belongs to a subnet association, rather than to an application identity. A subnet has one NACL, and one NACL can cover multiple subnets. Its rules apply as traffic crosses subnet boundaries, not to traffic routed within that same subnet.[^network-acls]

## Trace a request and its reply

Suppose client `10.40.1.10:49160` opens TCP to server `10.40.2.20:443`. The server replies from port 443 to client port 49160. Those are illustrative private addresses, not probe targets.

| Boundary | Forward packet | Reply packet |
| --- | --- | --- |
| Client subnet NACL | Outbound to server destination port 443 | Inbound to client destination port 49160 |
| Server subnet NACL | Inbound to server destination port 443 | Outbound to client destination port 49160 |

Allowing only port 443 in both directions is not sufficient for that reply. Select the required ephemeral-port range from the actual client/load-balancer/NAT behavior; do not copy one OS's range into every network policy. Lowest-numbered matching NACL rules determine the result, so a later allow cannot override an earlier deny.[^network-acls]

Security-group tracking handles replies differently. Removing a group's rule does not necessarily terminate every already-tracked flow immediately.[^connection-tracking] A NACL change can affect established traffic at a shared subnet boundary. Incident containment therefore needs a deliberate scope and impact decision, not an improvised broad deny applied during routine diagnosis.

## Asymmetry and translated identities

A public or private NAT maps source addresses on the appropriate path. A downstream filter may see the translated address, and the reverse path must return through the appropriate mapping.[^nat-types] Middlebox insertion adds its own requirements; a return route around an appliance can bypass its state or inspection.

Before changing an asymmetric path, document source/destination addresses at each boundary, both route-table decisions, and whether sessions can drain. A successful outbound SYN alone does not establish a working TCP exchange.

## Inspect subnet filtering

```bash
aws ec2 describe-network-acls --filters Name=association.subnet-id,Values=<subnet-id> --profile <profile> --region <region> --no-cli-pager
```

What it does: reads the NACL actually associated with the subnet, including inbound/outbound direction and rule order. Compare the complete request/reply tuples with the intended rules; do not sort by a tag or description.

Validate with new permitted and deliberately disallowed connections in an approved environment. Check existing long-lived flows after reviewed changes. These read-only commands need no cloud cleanup; revert temporary sandbox rules through the owner/source of truth, preserving the evidence before removal.

## Evidence and operating boundary

Official sources reviewed on 2026-10-29. AWS services evolve independently of the CLI. AWS CLI v2.38.5 validated the EC2 command examples using offline output skeletons. Those checks cover command inputs and the sample query, not account permissions, resource state, DNS, or packet delivery. No AWS account calls or infrastructure provisioning were executed for this revision. Replace angle-bracket placeholders before use, confirm account/Region, and keep network inventories private.

## Related routes

- [Security groups](security-groups.md).
- [Effective route selection](route-tables-and-path-selection.md).
- [Back to AWS networking](index.md)
- [Back to AWS](../index.md)

[^network-acls]: [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
[^connection-tracking]: [Security group connection tracking](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-connection-tracking.html)
[^nat-types]: [NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)

[^network-firewall]: [AWS Network Firewall](https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html)

[^gateway-load-balancer]: [Gateway Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html)
