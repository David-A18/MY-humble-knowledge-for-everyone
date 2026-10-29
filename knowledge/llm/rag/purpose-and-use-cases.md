---
type: Explanation
title: RAG purpose and use cases
description: Understand retrieval-augmented generation before choosing a vector database.
tags:
- llm
- rag
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: original-rag-paper
  resource: https://arxiv.org/abs/2005.11401
  title: Original RAG paper
- id: sqlite-fts5
  resource: https://www.sqlite.org/fts5.html
  title: SQLite FTS5
---

# RAG purpose and use cases

## Purpose

Understand retrieval-augmented generation before choosing a vector database.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## What RAG means

Retrieval-augmented generation retrieves relevant source material and supplies it to a language model as context for an answer. It combines a retriever with a generator. The original research explored retrieval alongside parametric generation; modern engineering uses the term for several retrieval-grounded architectures.[^original-rag-paper][^sqlite-fts5]

```mermaid
flowchart LR
  D[Approved documents] --> I[Derived index]
  Q[User question] --> R[Retriever]
  I --> R
  R --> E[Bounded evidence with citations]
  E --> G[Language model]
  Q --> G
  G --> A[Answer or insufficient evidence]
```

## Why add retrieval

RAG helps answer questions over changing, specialized, or organization-specific information without retraining model weights for each document update. It can expose supporting evidence and apply access restrictions during retrieval. It does not guarantee factual answers or remove the need for evaluation.

| Situation | Start with | Reason |
| --- | --- | --- |
| Exact command/error/file lookup | Search | The reader may only need the source. |
| Small set of supplied documents | Direct context | Indexing may add unnecessary complexity. |
| Large/changing corpus and sourced synthesis | RAG | Retrieve a relevant subset for the answer. |
| Style, behavior, or task adaptation | Prompting or fine-tuning | Weight adaptation solves a different problem. |
| Exact live system state | Authorized tool/API query | Static retrieved notes can be stale. |

## Example for this knowledge base

For “Why does Istio allow a request with no JWT?”, retrieval should find the distinction between RequestAuthentication and AuthorizationPolicy. Generation should explain the distinction and cite that section. If no evidence exists for a requested feature, the system should say so instead of filling the gap confidently.

## Limitations

Wrong retrieval, outdated sources, contradictory documents, prompt injection, and unsupported synthesis all produce failure. A retrieved statement is evidence to assess, not an instruction to obey or proof of truth. Start with a small measured baseline before adding agents, graph traversal, or multiple model stages.

## Related links

- [Original RAG paper](https://arxiv.org/abs/2005.11401)
- [SQLite FTS5](https://www.sqlite.org/fts5.html)
- [Agent knowledge-base architecture](../../ai/ai-tooling/knowledge-bases/reference-architecture.md)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^original-rag-paper]: [Original RAG paper](https://arxiv.org/abs/2005.11401).
[^sqlite-fts5]: [SQLite FTS5](https://www.sqlite.org/fts5.html).
