---
type: Explanation
title: RAG retrieval and reranking
description: Choose retrieval techniques from measured failure cases.
tags:
- llm
- rag
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: fts5-bm25
  resource: https://www.sqlite.org/fts5.html#the_bm25_function
  title: FTS5 BM25
- id: original-retrieval-grounded-generation-research
  resource: https://arxiv.org/abs/2005.11401
  title: Original retrieval-grounded generation research
---

# RAG retrieval and reranking

## Purpose

Choose retrieval techniques from measured failure cases.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Retrieval methods

| Method | Strength | Weakness |
| --- | --- | --- |
| Lexical/BM25 | Exact names, commands, error strings | Vocabulary mismatch. |
| Vector similarity | Semantic paraphrases | Exact identifiers and relevance can be unreliable. |
| Hybrid | Combines lexical and semantic candidates | Fusion, filtering, and tuning add complexity. |
| Reranking | Reorders a bounded candidate set | Cannot recover evidence absent from candidates. |

Embeddings encode text into vectors; similarity finds nearby representations. A vector store is an index, not the source of truth, and is not required for RAG. BM25 is a strong inspectable baseline for a Markdown engineering corpus.

## Query flow

Normalize cautiously, preserve exact identifiers, apply authorization/freshness filters, retrieve candidates, deduplicate, optionally rerank, and select a bounded evidence set. Hybrid systems may use rank fusion rather than comparing unrelated raw scores.

```bash
python examples/rag.py search --db /tmp/kb-rag.sqlite 'PeerAuthentication missing JWT'
```

What it does: executes the lab's safely quoted OR query over FTS5 and returns bounded ranked sections. BM25 scores rank results within the query; they are not calibrated answer-confidence probabilities.

## Tuning sequence

Build representative questions with expected source sections. Inspect misses: was the source absent, chunk malformed, query vocabulary different, or rank too low? Fix the responsible stage. Add semantic candidates/reranking only when the baseline's measured misses justify cost and latency.

The sample removes common English question words and uses bounded lexical terms. It has no semantic fallback or calibrated relevance threshold; related-word matches can still be weak. Production systems need an evaluated evidence-sufficiency policy, not only a non-empty result list.

Source references: [^fts5-bm25][^original-retrieval-grounded-generation-research]

## Related links

- [FTS5 BM25](https://www.sqlite.org/fts5.html#the_bm25_function)
- [Original retrieval-grounded generation research](https://arxiv.org/abs/2005.11401)
- [Context efficiency](../../ai/ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^fts5-bm25]: [FTS5 BM25](https://www.sqlite.org/fts5.html#the_bm25_function).
[^original-retrieval-grounded-generation-research]: [Original retrieval-grounded generation research](https://arxiv.org/abs/2005.11401).
