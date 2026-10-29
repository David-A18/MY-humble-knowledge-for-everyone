---
type: Explanation
title: Security groups
description: Understand ENI security-group rules, references, connection tracking,
  and a least-privilege verification sequence.
tags:
- aws
- networking
- security-groups
- security
status: draft
maturity: draft
audience: Cloud and platform engineering learners
maintainer: unassigned
sources:
- id: sg-rules
  title: Security group rules
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html
- id: connection-tracking
  title: Security group connection tracking
  resource: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-connection-tracking.html
---

# Security groups

A security group is a stateful network allow-list attached to supported resources' network interfaces. It controls permitted traffic, not which IAM identity may call an application. Use it to express intended source/destination and protocol boundaries alongside routing, subnet controls, and application authentication.

## Rules and relationships

Rules allow traffic; they do not contain explicit denies. Rules from multiple groups attached to the same resource are combined, so a restrictive group does not cancel a broad allow in another group. New custom groups start without inbound permission and normally include an outbound allow-all rule; inspect actual rules instead of assuming defaults survived provisioning.[^sg-rules]

A reference to another security group identifies eligible resources associated with that group in a supported topology. It does not copy its rules, create a route, authorize an IAM principal, or automatically preserve identity through a proxy/NAT/middlebox. Establish the source address and relationship the destination actually sees.

Illustrative intent for a private web backend:

| Relationship | Intended permission | Verification |
| --- | --- | --- |
| ALB → application | App port from the ALB's group | Correct listener/target-group port and healthy targets. |
| Application → database | Database port to the intended database group | Real connection from an authorized application instance. |
| Unrelated workload → database | No matching allow | New connection from a controlled unrelated client fails. |

These are design intents, not complete deployable rules. Health checks, DNS, monitoring, and other genuine dependencies need explicit consideration; adding all-port access to pass a probe defeats the boundary.

## Stateful does not mean every existing session closes on rule removal

Return traffic for an allowed tracked connection is admitted without a separate reverse-direction allow. Tracked connections can persist after rule changes until their tracking state expires; some broad permitted flows are untracked and behave differently.[^connection-tracking] Verify a security change using new connections as well as any affected long-lived sessions. Do not claim immediate revocation solely because a rule was removed.

## Inspect and verify the actual ENI

Use a read-only profile and the ENI/group IDs from the affected resource.

```bash
aws ec2 describe-network-interfaces --network-interface-ids <eni-id> --profile <profile> --region <region> --no-cli-pager
aws ec2 describe-security-group-rules --filters Name=group-id,Values=<security-group-id> --profile <profile> --region <region> --no-cli-pager
```

What it does: confirms the attached groups, addresses, and individual rule IDs, directions, protocols, ports, and referenced peers. Check every attached group's rules, not only the group with the most familiar name.

If the network remains blocked, inspect the effective routes, NACLs, host firewall, listener, and target health. Security groups do not filter Amazon-provided Route 53 Resolver traffic; use the relevant DNS controls for that resolver path.[^sg-rules]

Before a live rule change, capture the current rule and affected consumers, preserve an approved management path, and stage the smallest intended permission. Test one allowed and one denied client using the real destination/protocol. Revert temporary task-owned rules after a sandbox test; do not remove shared groups during cleanup. The read-only examples above change nothing.

## Evidence and operating boundary

Official sources reviewed on 2026-10-29. AWS services evolve independently of the CLI. AWS CLI v2.38.5 validated the EC2 command examples using offline output skeletons. Those checks cover command inputs and the sample query, not account permissions, resource state, DNS, or packet delivery. No AWS account calls or infrastructure provisioning were executed for this revision. Replace angle-bracket placeholders before use, confirm account/Region, and keep network inventories private.

## Related routes

- [Stateful controls and stateless ACLs](stateful-networking.md).
- [Connectivity troubleshooting](network-connectivity-troubleshooting.md).
- [Back to AWS networking](index.md)
- [Back to AWS](../index.md)

[^sg-rules]: [Security group rules](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)
[^connection-tracking]: [Security group connection tracking](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-connection-tracking.html)
