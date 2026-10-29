---
type: Troubleshooting Guide
title: Diagnose AWS network connectivity failures
description: Move from a failing DNS, TCP, TLS, or API request to the responsible
  VPC path or policy without broad firewall changes.
tags:
- aws
- networking
- diagnostics
- flow-logs
status: draft
maturity: draft
audience: Cloud and platform engineering learners
maintainer: unassigned
sources:
- id: flow-logs
  title: VPC Flow Logs
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html
- id: flow-records
  title: Flow log record examples
  resource: https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html
- id: reachability
  title: How Reachability Analyzer works
  resource: https://docs.aws.amazon.com/vpc/latest/reachability/how-reachability-analyzer-works.html
- id: reachability-cost
  title: Reachability Analyzer and pricing
  resource: https://docs.aws.amazon.com/vpc/latest/reachability/what-is-reachability-analyzer.html
---

# Diagnose AWS network connectivity failures

Use this guide when a specific AWS workload cannot reach a dependency. Record the time, client resource/ENI/subnet, hostname and resolved IP, protocol, destination port, observed error, and last relevant change. Confirm account and Region before inspecting resources.

## Separate the failing layers

| Observation | Investigate next |
| --- | --- |
| Name fails or resolves to the wrong network | Actual client resolver, private DNS, forwarding, and service hostname. |
| TCP timeout | Effective routes, address family, security groups, NACLs, target state, and return path. |
| Connection refused | Listener/port and application or proxy behavior; not every refusal is a cloud firewall problem. |
| TLS certificate/name error | SNI, hostname, trust chain, validity, and TLS termination layer. |
| API returns access denied | Actual caller plus IAM/resource/endpoint/organization policy; a responding service is different from an unreachable one. |
| EKS Service fails internally | Kubernetes [Service](../../../kubernetes/troubleshooting/service-connectivity.md), [DNS](../../../kubernetes/troubleshooting/dns-resolution.md), CNI, and policy routes. |

For an external load-balancer path, inspect listener, target group, health checks, target port, and target identity. For private endpoints, inspect endpoint type, state, DNS answer, ENI filtering or gateway route association. Preserve the actual request's network context; a working laptop request is not a control test for a private Pod.

## Trace configuration before changing rules

1. Use [route selection](route-tables-and-path-selection.md) to identify the effective table and target for the resolved destination.
2. Trace the return route, NAT/inspection state, and any transit-gateway decisions.
3. Inspect all groups attached to the relevant ENIs and both subnet NACL directions.
4. Check endpoint/gateway/load-balancer health and the actual listener.
5. Correlate available flow/application logs with the time and packet tuple.

Do not open all ports, replace a main route, disable certificate validation, or remove an endpoint policy just to see whether the symptom changes. Escalate the smallest concrete discrepancy to its owner.

## Use the right evidence tool

VPC Flow Logs describe observed IP traffic associated with network interfaces and can be delivered to CloudWatch Logs, S3, or Firehose. Ingestion/storage can incur charges; retention, scope, and sensitive-address handling need planning.[^flow-logs] Inspect already-configured delivery before proposing another capture:

```bash
aws ec2 describe-flow-logs --filter Name=resource-id,Values=<eni-id> --profile <profile> --region <region> --no-cli-pager
```

What it does: lists flow-log subscriptions configured for that ENI ID. An empty response does not exclude a VPC- or subnet-level flow log covering the ENI; inspect those scopes too. This command reads configuration, not traffic records.

In records, `ACCEPT` or `REJECT` concerns the recorded network handling, not application authentication or successful response delivery. `NODATA` and `SKIPDATA` require care; missing records do not prove a particular packet was never sent.[^flow-records] Use the record's actual schema and network-interface scope before interpreting a translated flow.

Reachability Analyzer builds a configuration model; it does not send packets or inspect the live data plane. A modeled reachable path does not prove DNS, TLS, a healthy application, or every unsupported component works.[^reachability] Analyses are billed per run, so use a scoped, approved source/destination/protocol and retain the result.[^reachability-cost]

## Close and verify

Capture the evidenced blocker, relevant owner, smallest correction, and rollback before a reviewed change. Re-test the original application request from the original client, a deliberately denied peer, and any impacted long-lived flow. A configuration fix should preserve the intended isolation.

Remove temporary probes, forwarding sessions, analysis resources, or task-owned capture only when no longer needed. Preserve incident evidence under its retention policy; do not delete shared logs, routes, or groups as cleanup. The read-only command here creates no resources.

## Evidence and operating boundary

Official sources reviewed on 2026-10-29. AWS services evolve independently of the CLI. AWS CLI v2.38.5 validated the EC2 command examples using offline output skeletons. Those checks cover command inputs and the sample query, not account permissions, resource state, DNS, or packet delivery. No AWS account calls or infrastructure provisioning were executed for this revision. Replace angle-bracket placeholders before use, confirm account/Region, and keep network inventories private.

## Related routes

- [Read-only network inspection lab](network-inspection-lab.md).
- [Security groups](security-groups.md) and [stateful controls](stateful-networking.md).
- [Back to AWS networking](index.md)
- [Back to AWS](../index.md)

[^flow-logs]: [VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)
[^flow-records]: [Flow log record examples](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html)
[^reachability]: [How Reachability Analyzer works](https://docs.aws.amazon.com/vpc/latest/reachability/how-reachability-analyzer-works.html)
[^reachability-cost]: [Reachability Analyzer and pricing](https://docs.aws.amazon.com/vpc/latest/reachability/what-is-reachability-analyzer.html)
