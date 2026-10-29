---
type: Explanation
title: Internet gateways and NAT egress
description: Choose direct internet, zonal or regional NAT, IPv6 egress, or service
  endpoints with explicit availability and cost trade-offs.
tags:
- aws
- networking
- nat
- egress
- ipv6
status: draft
maturity: draft
audience: Cloud and platform engineering learners
maintainer: unassigned
sources:
- id: internet-gateway
  title: Internet gateway access
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html
- id: nat-types
  title: NAT gateways
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html
- id: regional-nat
  title: Regional NAT gateways
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html
- id: nat-example
  title: Private subnets and zonal NAT example
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-example-private-subnets-nat.html
---

# Internet gateways and NAT egress

Outbound connectivity is a deliberate path from a workload to a dependency. An internet gateway (IGW) provides internet routing for a VPC; a NAT gateway translates connections initiated by workloads. Neither choice replaces workload authorization or application security.

## Choose a path for the requirement

| Need | Candidate | Important boundary |
| --- | --- | --- |
| Direct public service or instance access | IGW plus appropriate addresses/routes | IPv4 instances need a public IPv4 mapping; filters and listeners still apply. |
| Private IPv4 workload accessing public destinations | Public NAT gateway | Permits return traffic for initiated flows; not an inbound publishing mechanism. |
| Private address translation toward another network | Private zonal NAT | Routes to the private network; routing it to an IGW does not provide internet access. |
| Outbound-only native IPv6 internet traffic | Egress-only IGW | Native IPv6 does not require IPv4 NAT. |
| IPv6 client needing IPv4 destinations | Supported DNS64/NAT64 design | Different from native IPv6 egress; validate resolver and destination behavior. |
| Supported AWS API access | Gateway/interface endpoint | Service-specific, not a generic internet proxy. |

An IGW must be attached and routing configured. An instance's public address alone does not compensate for a missing route.[^internet-gateway] A public NAT uses an Elastic IP on its internet path; private NAT has different connectivity semantics.[^nat-types]

## Zonal and regional NAT are distinct designs

In the zonal pattern, a public NAT lives in a public subnet. Private-subnet routes target it, and its subnet routes to the IGW. A multi-AZ design commonly uses one zonal NAT per workload AZ to limit a zonal failure's impact and avoid an unnecessary cross-AZ path.[^nat-example]

Regional NAT is a newer availability mode. It does not need a customer public subnet to host it; its routing model includes its own route table. Automatic mode expands with workload presence across AZs, while manual mode requires operator management. Expansion is not instantaneous, so inspect readiness and current per-AZ state rather than assuming a new AZ is immediately local. Regional NAT does not support private NAT connectivity.[^regional-nat]

Check current Region/AZ support and CLI/API fields before choosing a mode. Converting modes or redirecting routes can reset established connections: plan a maintenance window, stable source-IP requirements, and recovery with the network owner. Do not silently apply a zonal diagram to regional NAT.

## Inspect before choosing recovery

```bash
aws ec2 describe-nat-gateways --filter Name=vpc-id,Values=<vpc-id> --profile <profile> --region <region> --no-cli-pager
aws ec2 describe-internet-gateways --filters Name=attachment.vpc-id,Values=<vpc-id> --profile <profile> --region <region> --no-cli-pager
```

What it does: inventories NAT state, mode-specific details, address/placement information, and the attached IGW. Compare this with the source subnet's effective table. An available NAT is not proof that the workload uses it; inspect [routes](route-tables-and-path-selection.md) and use a permitted application request to verify delivery.

## Cost, failure, and cleanup decisions

Estimate NAT provisioned time, processed bytes, public IPv4 usage, transfer paths, and the number of active AZs using current regional pricing. Compare interface-endpoint hourly/data costs with actual dependency traffic rather than assuming either option is always cheaper. Gateway endpoints can remove relevant S3/DynamoDB traffic from the NAT path; other external dependencies may still require egress.

When diagnosing timeouts, inspect NAT error/port-allocation metrics, connection reuse, routes, and destination behavior. Creating another gateway is not the first diagnostic. This page's commands create nothing. A separate sandbox deployment must remove its test routes/dependencies, delete its gateways/endpoints, and release only unused task-owned public IP allocations after confirming they are no longer referenced.

## Evidence and operating boundary

Official sources reviewed on 2026-10-29. AWS services evolve independently of the CLI. AWS CLI v2.38.5 validated the EC2 command examples using offline output skeletons. Those checks cover command inputs and the sample query, not account permissions, resource state, DNS, or packet delivery. No AWS account calls or infrastructure provisioning were executed for this revision. Replace angle-bracket placeholders before use, confirm account/Region, and keep network inventories private.

## Related routes

- [VPC endpoints and private DNS](vpc-endpoints-and-private-dns.md).
- [Stateful networking](stateful-networking.md).
- [Back to AWS networking](index.md)
- [Back to AWS](../index.md)

[^internet-gateway]: [Internet gateway access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)
[^nat-types]: [NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
[^regional-nat]: [Regional NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html)
[^nat-example]: [Private subnets and zonal NAT example](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-example-private-subnets-nat.html)
