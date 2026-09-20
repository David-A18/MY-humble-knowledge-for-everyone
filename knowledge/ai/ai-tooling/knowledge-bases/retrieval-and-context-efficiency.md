---
type: "Explanation"
title: "Retrieval and context efficiency"
description: "This guide explains how to design retrieval for agent knowledge bases as a measurable context budget rather than a race to return more text."
tags: [ai, ai-tooling, knowledge-bases]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# Retrieval and context efficiency

## Purpose

This guide explains how to design retrieval for agent knowledge bases as a measurable context budget rather than a race to return more text.

## Retrieval principle

Retrieval should minimize:

- Context tokens.
- Bytes returned.
- Irrelevant documents.
- Model calls.
- Retrieval latency.
- Repeated source loading.

Returning more information than required is an efficiency defect when a smaller, more authoritative result would answer the question.

## Progressive disclosure

| Level | Returned content | Use |
| --- | --- | --- |
| 1 | Navigation and index metadata | Let the agent choose the right area without loading articles. |
| 2 | Search results with titles, IDs, snippets, summaries, authority, trust, freshness, and tags | Let the agent pick candidate concepts. |
| 3 | Specific document or section | Provide enough evidence to answer. |
| 4 | Related evidence, source snapshots, or full source | Use only for high-stakes answers, conflicts, or verification. |

The serving layer should make each level explicit. A search call should not return whole documents by default.

## Lexical-first retrieval

Start with lexical search when the corpus is Markdown in Git. BM25, ripgrep-backed local search, SQLite FTS, OpenSearch, or similar lexical systems are easier to inspect, debug, and tune than semantic-only retrieval.

Add semantic reranking when measured failures show vocabulary mismatch. Examples:

- The golden question uses "identity federation" but the relevant page says "OIDC trust".
- Readers search "stale docs" but the concept uses "producer reconciliation".
- Product names and abbreviations vary across producers.

Use a vector database only when measured retrieval requirements justify persistent vector infrastructure. Embeddings are optional derived artifacts, not authoritative knowledge.

## Result shape

Search results should include enough metadata for an agent to decide what to fetch:

```json
{
  "id": "knowledge-bases/provenance-trust-and-freshness",
  "title": "Provenance, trust, and freshness",
  "path": "ai/ai-tooling/knowledge-bases/provenance-trust-and-freshness.md",
  "section": "Reconciliation state",
  "summary": "Tracks producer revisions, hashes, renderer versions, affected concepts, and reconciliation status.",
  "status": "stable",
  "trust_tier": "human-reviewed",
  "stale_after": "2026-11-08",
  "source_authority": "reviewed internal decision",
  "byte_size": 1840
}
```

What it does: lets the agent choose a bounded fetch based on relevance, authority, trust, freshness, and size.

## Retrieval budgets

Define budgets per deployment. Do not invent universal numeric limits.

Useful budgets include:

| Budget | What to measure |
| --- | --- |
| Maximum search hits | Number of candidate results returned. |
| Maximum snippet size | Bytes or approximate tokens per result snippet. |
| Maximum returned bytes | Total bytes returned per search or fetch. |
| Approximate token budget | Tokens consumed before the model starts answering. |
| Maximum follow-up fetch depth | Number of additional linked sections an agent may fetch without a new reason. |
| Maximum reranker calls | Cost and latency ceiling for semantic reranking. |

Calibrate budgets empirically with golden questions. Raise budgets only when failures show the expected evidence is outside the current boundary.

## Chunking guidance

- Chunk by Markdown heading when possible.
- Preserve path, title, heading, concept ID, source IDs, trust, freshness, and lifecycle metadata on every chunk.
- Keep command examples outside tables so chunks include runnable context.
- Avoid giant tables with long cells.
- Add aliases and common search terms to summaries or frontmatter, not as hidden prompt instructions.
- Use stable section IDs or heading anchors where the serving layer supports them.

## Anti-patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Search returns full documents | Wastes tokens and hides ranking errors. |
| Semantic-only retrieval with no lexical fallback | Fails exact identifiers, commands, filenames, and error strings. |
| Filtering after retrieval | May retrieve unauthorized content before dropping it. |
| Embeddings treated as source of truth | Embeddings cannot be reviewed as authoritative knowledge. |
| No search-miss tracking | The corpus never learns what users and agents cannot find. |
| No corpus revision in results | Answers cannot be reproduced against a known knowledge state. |

## Validation

Test retrieval with a golden question dataset. Each question should define:

- Expected relevant concept IDs.
- Expected source IDs when applicable.
- Required authority or freshness constraints.
- Whether section-level retrieval is enough.
- Maximum acceptable search and fetch cost for the deployment.

A useful target for this repository's example architecture is that the expected authoritative concept appears within the top 3 retrieval results for golden-set questions. This is an architecture target, not a universal sufficiency claim.

## Related links

- [Reference architecture](reference-architecture.md)
- [Evaluation and quality](evaluation-and-quality.md)
- [Security and governance](security-and-governance.md)
- [Back to agent knowledge bases](index.md)
- [Back to AI tooling](../index.md)
- [Back to root index](../../../../README.md)
