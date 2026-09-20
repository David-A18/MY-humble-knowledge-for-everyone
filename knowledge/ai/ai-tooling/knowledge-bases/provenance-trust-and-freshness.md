---
type: "Explanation"
title: "Provenance, trust, and freshness"
description: "This guide explains how an agent knowledge base records where knowledge came from, how it was verified, whether it is still fresh, and what to do when sources disagree."
tags: [ai, ai-tooling, knowledge-bases]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# Provenance, trust, and freshness

## Purpose

This guide explains how an agent knowledge base records where knowledge came from, how it was verified, whether it is still fresh, and what to do when sources disagree.

## Authority model

Authority is domain-specific. Configure the hierarchy for the corpus instead of hard-coding one universal order.

A common starting point is:

| Authority level | Example |
| --- | --- |
| Canonical machine-readable producer | OpenAPI, AsyncAPI, JSON Schema, Terraform, Kubernetes manifests, SQL schemas. |
| Reviewed internal decision or runbook | ADR, operational runbook, architecture decision. |
| Official vendor or project documentation | Kubernetes, AWS, W3C, NIST, OWASP, OpenAPI Initiative. |
| Reviewed curated explanation | Human-reviewed knowledge article. |
| Generated or unverified note | Agent-authored draft without verification. |
| Historical or deprecated material | Retained for context only. |

Never resolve conflicting authoritative sources silently. The retrieval layer should expose enough metadata for an agent to recognize authority, verification, freshness, conflicts, and deprecation.

## Provenance fields

At minimum, record:

| Field | Why it matters |
| --- | --- |
| Source resource | Lets humans and agents inspect evidence. |
| Source ID | Stable citation key. |
| Source title | Human-readable label. |
| Source author or producer | Authority signal. |
| Source last modified | Recency signal. |
| Generation actor and time | Shows who or what produced the current content. |
| Verification actor and time | Shows who or what confirmed the current content. |
| Stale-after date | Signals when the concept needs review. |
| Corpus Git SHA | Makes answers reproducible. |

OKF v0.2 provides a portable frontmatter model for many of these fields. Plain Markdown repositories can still use frontmatter or structured body sections when full OKF conformance is not required.

## Reconciliation state

For each producer, maintain conceptual state like:

```yaml
producer_id: public-kubernetes-docs
pinned_revision: "2026-07-01"
observed_revision: "2026-08-01"
source_path: docs/concepts/workloads/pods
source_hash: sha256:example
renderer_version: docs-renderer/1.2.0
knowledge_concepts:
  - ai/ai-tooling/knowledge-bases/examples/okf-v0.2/concepts/source-schema-extraction
generated_hash: sha256:example-output
last_reconciled_at: 2026-08-08T10:00:00Z
status: active
```

What it does: separates producer state from corpus state and makes drift detection independent of webhooks.

## Reconciliation procedure

1. Discover current producer state.
2. Compare pinned revision, observed revision, source paths, and content hashes.
3. Identify changed source scopes.
4. Map source scopes to dependent knowledge concepts.
5. Regenerate deterministic machine-owned regions.
6. Ask an agent to reconsider reasoning-owned regions when source changes affect explanation or guidance.
7. Validate metadata, links, generated regions, source references, and security policy.
8. Compare byte or content hashes.
9. Create a proposed Git change only if a meaningful diff exists.
10. Send the change through human review.
11. Update pinned producer state after merge.

A second reconciliation over unchanged inputs should produce byte-identical outputs and no PR.

## Freshness signals

| Signal | Use |
| --- | --- |
| Producer revision age | Indicates how long the corpus trails the producer. |
| Source hash drift | Indicates source content changed even if revision labels are weak. |
| `stale_after` | Indicates concept review deadline. |
| Last successful reconciliation | Indicates whether the maintenance loop is healthy. |
| Reconciliation failures | Indicates unknown freshness for affected scopes. |
| Source retirement | Indicates a source moved, disappeared, or is no longer authoritative. |

Freshness should come from state reconciliation, not only events. Webhooks are useful latency reducers, not the correctness model.

## Conflict handling

When sources disagree, an agent should:

1. Identify the conflicting claims.
2. Compare source authority, recency, verification, and lifecycle state.
3. Prefer deterministic producers for exact machine-readable facts.
4. Surface unresolved conflicts in the answer.
5. Propose a knowledge update or issue when the corpus needs a decision.

Do not average, merge, or hide conflicting authoritative claims.

## Versioning

Track versioning at multiple levels:

- Producer revision.
- Knowledge corpus Git commit.
- OKF version when using OKF.
- Renderer version.
- Retrieval index version.
- Embedding model version when embeddings are used.
- MCP protocol version when MCP is used.
- Knowledge concept lifecycle state.

A response should ideally be reproducible against a known corpus revision and retrieval configuration.

## Related links

- [OKF v0.2](okf-v0.2.md)
- [Reference architecture](reference-architecture.md)
- [Retrieval and context efficiency](retrieval-and-context-efficiency.md)
- [Evaluation and quality](evaluation-and-quality.md)
- [Back to agent knowledge bases](index.md)
- [Back to AI tooling](../index.md)
- [Back to root index](../../../../README.md)
