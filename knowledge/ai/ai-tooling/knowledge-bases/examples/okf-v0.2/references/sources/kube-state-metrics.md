---
type: "Source Reference"
title: "kube-state-metrics Pod metrics"
description: "Locate the official Pod metric name and labels before writing a PromQL example."
tags: [ai, ai-tooling, knowledge-bases]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
resource: https://github.com/kubernetes/kube-state-metrics/blob/4057c6d6f3fce76ae122dc9dfa44000abc164968/docs/metrics/workload/pod-metrics.md
---

# kube-state-metrics Pod metrics

This project documents the `kube_pod_container_status_restarts_total`
counter and its `namespace`, `pod`, `container`, and `uid` labels. It tells
you what the metric represents; it does not prove that a particular cluster
scrapes the metric or that a sample query ran.

## Use in this bundle

- Supports [Pod restarts in a time window](../../concepts/pod-restart-rate.md).

## Related links

- External source: [official Pod metrics list, pinned revision](https://github.com/kubernetes/kube-state-metrics/blob/4057c6d6f3fce76ae122dc9dfa44000abc164968/docs/metrics/workload/pod-metrics.md)
- [Back to source references](index.md)
