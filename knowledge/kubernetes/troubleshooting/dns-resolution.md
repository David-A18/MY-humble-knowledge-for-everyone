---
type: Troubleshooting Guide
title: DNS resolution failures
description: Separate namespace and resolver mistakes from cluster DNS, upstream resolution,
  and application connectivity failures.
tags:
- kubernetes
- troubleshooting
- dns
- coredns
status: draft
maturity: draft
audience: Platform engineers with basic kubectl knowledge
maintainer: unassigned
sources:
- id: dns-debugging
  title: Debugging DNS Resolution
  resource: https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/
- id: network-policies
  title: Network Policies
  resource: https://kubernetes.io/docs/concepts/services-networking/network-policies/
---

# DNS resolution failures

Use this guide when a Pod reports name-resolution errors. DNS maps names to addresses; it does not prove the destination application is healthy. Test inside the affected Pod's network context when possible. A diagnostic Pod with different labels, DNS settings, or namespace may follow different policies.

## Establish the resolver and name

You need permission to inspect the Pod and execute a diagnostic command in it. The selected container must already include `cat` and `nslookup`; otherwise use an approved debug image through your cluster's debugging procedure. Do not assume every minimal application image contains a shell.

```bash
kubectl get pod <pod> -n <namespace> -o yaml
kubectl exec <pod> -n <namespace> -c <container> -- cat /etc/resolv.conf
kubectl exec <pod> -n <namespace> -c <container> -- nslookup <service>.<service-namespace>
kubectl exec <pod> -n <namespace> -c <container> -- nslookup kubernetes.default
```

What it does: compares `dnsPolicy`/`dnsConfig`, the actual nameserver and search path, the application Service name, and a cluster control name. Short Service names depend on the client's namespace. Read the cluster suffix from the environment rather than assuming `cluster.local`.[^dns-debugging]

## Interpret the result before changing CoreDNS

| Result | Next question |
| --- | --- |
| Qualified Service name works; short name fails | Is the client in the expected namespace and using the expected search list? |
| `NXDOMAIN` | Does the Service/name exist in the intended namespace? Is this a headless Service awaiting endpoints? |
| Timeout | Can this Pod reach its configured resolver? Check DNS egress and the resolver's availability. |
| `SERVFAIL` | Inspect resolver errors, API access, upstream forwarding, and malformed zones. |
| Cluster name works; approved external name fails | Check upstream DNS and node/VPC forwarding instead of changing Service selectors. |
| DNS returns the intended address; HTTP fails | Continue with [Service connectivity](service-connectivity.md). |

For a standard CoreDNS installation, a cluster operator can inspect the following. Names and labels may differ with custom DNS or NodeLocal DNSCache; trace the actual nameserver instead of installing another DNS stack.

```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide
kubectl get service kube-dns -n kube-system
kubectl get endpointslices.discovery.k8s.io -n kube-system -l kubernetes.io/service-name=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=100 --prefix
```

What it does: checks DNS Pod readiness, the resolver Service, its backend slices, and recent resolver logs. Expect reachable ready backends; no log entries for successful queries is normal when query logging is disabled.

If DNS egress is restricted, validate the permitted resolver destination and both UDP/TCP 53 as required by your DNS path. NodeLocal DNS and address translation can affect which destination the network implementation sees.[^network-policies]

## Recover, verify, and clean up

Fix a wrong name or Pod DNS setting in its workload source. Escalate resolver outages to the cluster operator with namespace, node, query, response code, and time. Enabling query logging or editing the Corefile is a cluster-wide change: review it first, bound the capture time, and restore the previous configuration afterward. Query logs can expose internal names.

Re-test the same application name from the original Pod, another affected node, and a permitted external name if upstream DNS was affected. Remove temporary debug Pods if you created them; this guide's commands create none.

## Evidence and scope

Source review: 2026-10-29. Commands are adaptable diagnostic examples; replace angle-bracket placeholders before running. No live cluster walkthrough was executed for this revision. Record client/server and controller versions during reproduction. Keep diagnostic logs private and redact credentials, customer data, and internal addresses before sharing.

## Related routes

- [Pending Pods](pending-pods-and-scheduling.md) — a DNS test Pod must first be scheduled and running.
- [Back to troubleshooting](index.md)
- [Back to Kubernetes](../index.md)

[^dns-debugging]: [Debugging DNS Resolution](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/)
[^network-policies]: [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
