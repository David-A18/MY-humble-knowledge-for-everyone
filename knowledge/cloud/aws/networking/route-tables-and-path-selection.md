---
type: How-to Guide
title: Find the effective subnet route and next hop
description: Resolve explicit versus main route-table associations and select the
  destination-specific path before changing networking.
tags:
- aws
- networking
- routes
- diagnostics
status: draft
maturity: draft
audience: Cloud and platform engineering learners
maintainer: unassigned
sources:
- id: route-tables
  title: Subnet route tables
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/subnet-route-tables.html
---

# Find the effective subnet route and next hop

Use this guide when you know a workload subnet and destination IP and need to explain the next hop. It is a read-only procedure. Have the VPC/subnet IDs, address family, account, Region, and permission to describe route tables. Resolve the hostname from the actual client first; a public and private DNS answer can produce different paths.

## 1. Find explicit and implicit associations

```bash
aws ec2 describe-route-tables --filters Name=association.subnet-id,Values=<subnet-id> --profile <profile> --region <region> --no-cli-pager
aws ec2 describe-route-tables --filters Name=vpc-id,Values=<vpc-id> Name=association.main,Values=true --profile <profile> --region <region> --no-cli-pager
```

What it does: looks for an explicit subnet association and separately locates the VPC's main table. If there is no explicit association, the subnet uses the main table. It does not use every table in the VPC; subnet names and resource tags do not select routes.[^route-tables]

Record the effective table ID. Read its `Routes`, destination fields, target fields, and state. Targets can include `GatewayId`, `NatGatewayId`, `TransitGatewayId`, `VpcPeeringConnectionId`, or an ENI; do not read only one field and assume every route is an internet route.

## 2. Match the destination

AWS selects the most specific matching destination prefix. IPv4 and IPv6 routes are separate; `0.0.0.0/0` does not cover IPv6.[^route-tables] For prefix-list destinations, inspect the list's current entries rather than trying to compare the list identifier as an IP network.

Illustrative IPv4 table:

| Destination | Target | Meaning for this exercise |
| --- | --- | --- |
| `10.40.0.0/16` | local | VPC-local address path. |
| `10.80.0.0/16` | transit gateway | Connected network path. |
| `0.0.0.0/0` | NAT gateway | Remaining IPv4 destinations. |

For `10.80.7.10`, choose the transit-gateway route; for `198.51.100.20`, choose the default route. These are documentation addresses and a paper exercise, not live endpoints to probe. For equal-prefix/static/propagated route interactions, inspect the applicable service's route-priority rules rather than extending this simple example into a full routing simulator.

## 3. Follow the target and return path

An active next hop is necessary but does not prove that a packet reaches a listener. For a zonal public NAT, inspect its subnet's internet-gateway route; for regional NAT, inspect its own managed route-table model. For connected VPCs, inspect the target network's return route and any transit route tables. A missing return path can resemble a destination firewall drop.

If the chosen route is `blackhole`, investigate the target's lifecycle and intended owner before changing it. Do not point a production subnet to another gateway simply because that gateway is available. A main-table change may affect every subnet without an explicit association.

## Verify and retain evidence

Produce a compact record: source ENI/subnet, resolved destination, effective table, matching route/target, return route, and outstanding security/listener checks. Use [connectivity troubleshooting](network-connectivity-troubleshooting.md) for the remaining layers. Any later route change needs a reviewed before/after plan, scope, and rollback; this procedure itself changes no cloud state and requires no cloud cleanup.

## Evidence and operating boundary

Official sources reviewed on 2026-10-29. AWS services evolve independently of the CLI. AWS CLI v2.38.5 validated the EC2 command examples using offline output skeletons. Those checks cover command inputs and the sample query, not account permissions, resource state, DNS, or packet delivery. No AWS account calls or infrastructure provisioning were executed for this revision. Replace angle-bracket placeholders before use, confirm account/Region, and keep network inventories private.

## Related routes

- [Internet and NAT egress](internet-and-nat-egress.md).
- [VPC connectivity choices](vpc-connectivity-options.md).
- [Back to AWS networking](index.md)
- [Back to AWS](../index.md)

[^route-tables]: [Subnet route tables](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-route-tables.html)
