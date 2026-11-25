---
type: Troubleshooting Guide
title: Diagnose hybrid DNS failures with Route 53 Resolver
description: Trace a failed private DNS query between an AWS VPC and an on-premises network to the failing resolver or network hop.
tags: [aws, networking, dns, route-53]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: inbound
    resource: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-overview-forward-network-to-vpc.html
    title: Route 53 inbound forwarding
  - id: outbound
    resource: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-overview-forward-vpc-to-network.html
    title: Route 53 outbound forwarding
  - id: rule-selection
    resource: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-overview-forward-vpc-to-network-where-to-forward-queries.html
    title: Route 53 forwarding rule selection
  - id: query-logs
    resource: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-query-logs.html
    title: Route 53 Resolver query logging
---

# Diagnose hybrid DNS failures with Route 53 Resolver

Start with one failing name and follow its exact path. If a name resolves
inside AWS and times out from your network, compare the answer from your
normal corporate resolver with a query sent from that resolver to the Route 53
inbound endpoint. Use the same name and record type at each hop.

## Establish the expected answer

Record the fully qualified name, record type, expected answer, client source,
and the time of the test. Ask the team that owns the record to confirm which
resolver should answer. A valid answer from one network can differ from the
answer in another when they use different private DNS zones.

Use the DNS resolver your client actually uses. These addresses and names
are placeholders. Run direct probes only from hosts allowed to use the
selected resolver.

```bash
dig @192.0.2.53 app.aws.example. A +time=2 +tries=1
dig @192.0.2.53 app.aws.example. A +tcp +time=2 +tries=1
```

What it does: compares the same lookup first over UDP and then over TCP.
Keep the response status and answer section. If the UDP response is
truncated, the first command may retry over TCP. Add `+ignore` to the UDP
probe when you need to inspect the original truncated response.

## Queries from your network into AWS

The normal path is client → corporate resolver → inbound endpoint IP →
VPC Resolver. Check that the corporate resolver forwards the intended suffix
to the endpoint IPs. From the corporate resolver or an equivalent authorized
test source, query each endpoint IP using both transports.[^inbound]

- If a direct endpoint query returns the right answer but the resolver does
  not, inspect the conditional forwarder, its cache, and its resolver logs.
- If one endpoint IP times out, compare routes, endpoint subnet network ACLs,
  and return paths for that IP. Check TCP and UDP port 53 ingress on the
  endpoint security group from the real forwarding resolver addresses.
- If the endpoint responds with the wrong DNS view, confirm that the intended
  private hosted zone is associated with the endpoint's VPC and has the
  queried record or alias.

## Queries from AWS into your network

The normal path is workload → VPC Resolver → matching forwarding rule →
outbound endpoint → on-premises resolver. Check the workload's actual
resolver and the forwarding rule association on the **workload's VPC**.
Confirm which suffix wins and which target IPs and ports the rule uses.
Trace routes from the outbound endpoint subnets and confirm the target
resolver allows the endpoint source addresses.[^outbound][^rule-selection]

Compare a query from the workload with the result from the intended target
resolver, using an authorized test source for the latter. A direct probe from
the workload checks that workload's network path. Use the target resolver's
query logs to confirm receipt from the outbound endpoint.

## Interpret the result and verify recovery

| Observation | Next check |
| --- | --- |
| Timeout | Check paths in both directions, TCP/UDP rules, and resolver reachability. A timeout alone does not identify the dropping hop. |
| NXDOMAIN | Confirm the expected DNS view, suffix, record, and negative-cache lifetime. A resolver responded that the name does not exist in its view. |
| SERVFAIL | Compare target resolver results and logs, and check for forwarding loops or upstream failures. |
| NOERROR with no answer | Verify the requested record type exists and check any aliases in the chain. |
| Correct record but application still fails | Check whether the application can reach the returned address over the required protocol. |

After a targeted fix, rerun the original client query, check each intended
endpoint path, and confirm an unrelated name still resolves. If query
logging is enabled, correlate by timestamp, name, and response code. A cached
reply may produce no new event in Resolver query logs.[^query-logs]

## Evidence and limits

Reviewed against AWS documentation on 25 November 2026. No AWS account,
VPN, Direct Connect, or Resolver endpoint was used to execute these
examples.

## Related links

- [VPC endpoints and private DNS](vpc-endpoints-and-private-dns.md)
- [Diagnose AWS network connectivity failures](network-connectivity-troubleshooting.md)
- [AWS networking](index.md)
- [AWS index](../index.md)
- [Knowledge home](../../../index.md)

[^inbound]: [Route 53 inbound forwarding](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-overview-forward-network-to-vpc.html)
[^outbound]: [Route 53 outbound forwarding](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-overview-forward-vpc-to-network.html)
[^rule-selection]: [Route 53 forwarding rule selection](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-overview-forward-vpc-to-network-where-to-forward-queries.html)
[^query-logs]: [Route 53 Resolver query logging](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-query-logs.html)
