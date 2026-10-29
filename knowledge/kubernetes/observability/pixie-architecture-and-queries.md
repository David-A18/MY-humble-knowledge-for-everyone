---
type: Explanation
title: Pixie architecture and queries
description: Use automatically collected telemetry for focused Kubernetes debugging.
tags:
- kubernetes
- observability
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: pixie-overview
  resource: https://docs.px.dev/about-pixie/what-is-pixie/
  title: Pixie overview
- id: pixie-faq
  resource: https://docs.px.dev/about-pixie/faq/
  title: Pixie FAQ
- id: pxl-tutorial
  resource: https://docs.px.dev/tutorials/pxl-scripts/write-pxl-scripts/
  title: PxL tutorial
---

# Pixie architecture and queries

## Purpose

Use automatically collected telemetry for focused Kubernetes debugging.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## What Pixie is

Pixie is an open-source Kubernetes observability/debugging project. It uses eBPF and other sources to collect supported application, network, and resource data. Coverage depends on protocols, runtimes, privileges, and component versions.[^pixie-overview][^pixie-faq][^pxl-tutorial]

PEMs (Pixie Edge Modules) collect/store data on nodes. Vizier coordinates in-cluster deployment and query execution. Pixie Cloud provides functions such as authentication, metadata, and query access/proxying through hosted or self-hosted options. In-cluster storage does not mean no query results traverse a proxy.

## Query model

PxL is Pixie's Python-like query language, executed by Pixie rather than a standard Python interpreter. Start with short time ranges and only needed columns.

```python
import px

df = px.DataFrame(table='http_events', start_time='-5m')
px.display(df, 'http_events')
```

What it does: displays recent captured HTTP events in Pixie. Schema and records depend on traffic and deployed components. Use the matching table reference before selecting status, latency, and service fields.

## Investigations

Find a slow service, narrow to namespace/Pod, inspect supported requests, compare errors, and correlate with resource pressure. Start with prebuilt cluster/service views, then add custom queries.

## Coverage and privacy

Observed spans do not necessarily form a complete end-to-end trace with application propagation. Check release-specific FAQ/data sources for logs, events, tracing, and protocol limits; a particular installation may expose less than a product summary describes.

Request bodies and database queries may contain private data or credentials. Restrict access, review retention/redaction, and begin with synthetic traffic. Export to durable backends only through a reviewed integration.

## Related links

- [Pixie overview](https://docs.px.dev/about-pixie/what-is-pixie/)
- [Pixie FAQ](https://docs.px.dev/about-pixie/faq/)
- [PxL tutorial](https://docs.px.dev/tutorials/pxl-scripts/write-pxl-scripts/)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^pixie-overview]: [Pixie overview](https://docs.px.dev/about-pixie/what-is-pixie/).
[^pixie-faq]: [Pixie FAQ](https://docs.px.dev/about-pixie/faq/).
[^pxl-tutorial]: [PxL tutorial](https://docs.px.dev/tutorials/pxl-scripts/write-pxl-scripts/).
