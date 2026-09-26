---
type: "Explanation"
title: "Evaluation and quality"
description: "This guide defines how to measure whether an AI knowledge base works. A corpus is not good because it contains many files. It is good when agents can find the right evidence quickly, trust it appropriately, cite it correctly, and keep it current."
tags: [ai, ai-tooling, knowledge-bases]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# Evaluation and quality

## Purpose

This guide defines how to measure whether an AI knowledge base works. A corpus is not good because it contains many files. It is good when agents can find the right evidence quickly, trust it appropriately, cite it correctly, and keep it current.

## Retrieval evaluation

Use a golden question dataset. For each question, define:

- Expected relevant concepts.
- Expected source IDs.
- Acceptable stale or deprecated behavior.
- Required authority tier.
- Expected top-k result behavior.
- Whether the answer needs a section, whole document, or source evidence.

Useful metrics:

| Metric | What it shows |
| --- | --- |
| Recall@k | Whether expected evidence appears in the first `k` results. |
| Precision@k | How much of the first `k` results is relevant. |
| MRR | How high the first relevant result appears. |
| nDCG@k | Whether highly relevant results rank above weaker results. |
| Top-k hit rate | Whether at least one expected concept appears in the first `k` results. |

For the example architecture, a practical target is that the expected authoritative concept appears within the top 3 retrieval results for golden-set questions. This is not universal; calibrate by domain risk, corpus size, and tool cost.

## Answer evaluation

Evaluate answer generation separately from retrieval.

| Dimension | Check |
| --- | --- |
| Correctness | The answer matches authoritative evidence. |
| Groundedness | Claims are supported by retrieved sources. |
| Citation correctness | Citations point to the source that supports the claim. |
| Citation completeness | Material claims have enough evidence. |
| Source authority | The answer prefers appropriate authority levels. |
| Freshness awareness | The answer surfaces stale or unreconciled evidence. |
| Conflict handling | The answer reports unresolved authoritative conflicts. |
| Hallucination rate | Unsupported claims are detected and reduced. |

Classify failures as retrieval failures, generation failures, freshness failures, citation failures, or authority failures. Fixing the wrong layer wastes effort.

## Efficiency evaluation

Measure the cost to find the answer separately from the cost to generate the answer.

Useful efficiency signals:

- Tokens retrieved.
- Tokens consumed before reaching evidence.
- Bytes returned.
- Number of tool calls.
- Retrieval latency.
- p50 and p95 end-to-end latency.
- Number of documents fetched.
- Cache hit ratio.
- Reranker or model calls.

## Freshness evaluation

Track:

| Metric | Meaning |
| --- | --- |
| Producer-to-detection delay | Time from producer change to detected drift. |
| Detection-to-PR delay | Time from drift detection to proposed knowledge change. |
| PR backlog | Number and age of proposed knowledge updates. |
| Stale concepts | Concepts past `stale_after`. |
| Unreconciled producers | Producers outside the agreed reconciliation window. |
| Reconciliation failures | Failed producer checks or renderer runs. |
| Age of pinned revisions | How far accepted knowledge trails current producers. |

A useful target property is that no producer remains unreconciled beyond the agreed reconciliation window.

## Determinism tests

For deterministic regions:

```text
same source input
+ same renderer version
= same machine-owned output
```

A no-change reconciliation must not create a PR. Test this by re-running extractors over the same source revision and comparing generated hashes or byte output.

## Trust and machine-owned-region tests

Useful invariant:

```text
zero model-authored claims inside deterministic machine-owned regions
```

Test it by:

- Marking machine-owned regions.
- Re-rendering them from source.
- Comparing output exactly or by structured AST.
- Rejecting edits inside protected regions unless they came from the renderer.
- Requiring source IDs for machine-owned claims.

## Observability

Metric names are implementation-specific, but the system should expose these signals:

| Signal | Question it answers |
| --- | --- |
| Search request count and latency | How much retrieval traffic exists and how fast it is. |
| Fetch request count and latency | How often agents need full evidence. |
| Results returned and bytes or tokens returned | Whether retrieval budgets are respected. |
| Cache hits | Whether derived serving state is effective. |
| Stale results | Whether agents see stale concepts. |
| Reconciliation lag and failures | Whether freshness maintenance works. |
| Drift detected | Whether producers changed. |
| PRs created | Whether reconciliation produces reviewable changes. |
| Validation failures | Whether generated output violates policy. |
| Access denied | Whether authorization is active and visible. |
| Source conflicts | Whether the corpus contains unresolved contradictions. |

Tracing should answer:

- What did the agent search?
- What documents were returned?
- Which source supported the answer?
- How old was the source?
- How much context was consumed?
- Which corpus version was queried?
- Which authorization scope was applied?

## Cache design

Safe cache keys may include:

- Knowledge Git SHA.
- Query normalization version.
- Filters.
- Retrieval algorithm version.
- Embedding model version when used.
- Authorization scope.

When the corpus SHA changes, derived cache state should be invalidatable or rebuildable. Never let caching bypass authorization or freshness controls.

## Related links

- [Retrieval and context efficiency](retrieval-and-context-efficiency.md)
- [Provenance, trust, and freshness](provenance-trust-and-freshness.md)
- [Security and governance](security-and-governance.md)
- [Reference architecture](reference-architecture.md)
- [Back to agent knowledge bases](index.md)
- [Back to AI tooling](../index.md)
- [Back to root index](../../../../README.md)
