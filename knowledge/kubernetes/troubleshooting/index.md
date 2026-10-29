# Kubernetes troubleshooting

Start with [common solutions](common-solutions.md) to identify the failing layer, then choose a focused runbook. Confirm the cluster and namespace before every investigation.

## Diagnostic routes

| Guide | Outcome |
| --- | --- |
| [Kubernetes common solutions](common-solutions.md) | Choose a diagnostic route and collect evidence. |
| [CrashLoopBackOff](crashloopbackoff.md) | Find container exit, memory, initialization, and probe failures. |
| [Pending Pods and scheduling failures](pending-pods-and-scheduling.md) | Distinguish admission, scheduling, and post-assignment waits. |
| [Image pull failures](image-pull-failures.md) | Identify image, credential, registry, and cache failures. |
| [Service connectivity failures](service-connectivity.md) | Trace selectors, EndpointSlices, application ports, and policy. |
| [DNS resolution failures](dns-resolution.md) | Separate names/search paths, DNS service, and upstream failures. |
| [Persistent-volume binding and mount failures](persistent-volume-failures.md) | Trace provisioning, topology, attachment, mount, and filesystem access. |
| [Gateway route and TLS failures](gateway-route-and-tls.md) | Check Gateway API conditions, reference permissions, and certificates. |
| [Deployment rollout stalls](rollout-stalls.md) | Diagnose a Deployment revision and choose compatible recovery. |
| [APISIX troubleshooting](apisix.md) | Inspect APISIX controller and gateway behavior. |
| [kind troubleshooting](kind.md) | Diagnose the local runtime, context, image cache, and host path. |

## Practice and evidence

Use the [local learning path](../../cross-topic-guides/local-deployment-learning-path.md) for prerequisites and the [manifest regression lab](../applications-and-tools/manifest-validation/regression-lab-and-ci.md) for a bounded Service-routing failure. These source-reviewed runbooks remain drafts; this section refresh did not execute a live cluster walkthrough. Each page states its evidence boundary.

- [Kubernetes command workflows](../commands/workflows.md)
- [Back to Kubernetes](../index.md)
- [Back to knowledge bundle](../../index.md)
