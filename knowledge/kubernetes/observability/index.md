# Kubernetes observability

Understand signals and collection before selecting a backend or eBPF product. o11y abbreviates observability: eleven letters sit between o and y.

## Learning path

Read in order, or choose a task from the table.

| Guide | Use it for |
| --- | --- |
| [Fundamentals and signals](fundamentals-and-signals.md) | Connect metrics, logs, traces, profiles, and SLOs. |
| [Instrumentation and tool selection](instrumentation-and-tool-selection.md) | Choose SDKs, collectors, backends, and network visibility. |
| [eBPF architecture and uses](ebpf.md) | Understand hooks, verification, maps, and constraints. |
| [Pixie architecture and queries](pixie-architecture-and-queries.md) | Understand automatic telemetry and PxL. |
| [Pixie lab and troubleshooting](pixie-lab-and-troubleshooting.md) | Check compatibility and debug synthetic traffic. |
| [Telemetry collection and aggregation](telemetry-aggregation.md) | Design OTel, Fluent Bit, and Vector pipelines. |
| [OpenTelemetry collector lab](collector-lab.md) | Observe delivery and failure. |

## Cost allocation connection

Use [Kubernetes cost allocation](../../finops/kubernetes-cost-allocation.md) to connect workload labels and metrics with bills, shared/idle pools, and operational headroom. Cost attribution and resource utilization are different signals.

## Related links

- [Runnable example files](examples/index.md)

- [Back to parent index](../index.md)
- [Back to root index](../../../README.md)
