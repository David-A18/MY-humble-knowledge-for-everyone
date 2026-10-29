---
type: Explanation
title: RAG ingestion and chunking
description: Turn reviewed source documents into reproducible evidence units.
tags:
- llm
- rag
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: sqlite-fts5-indexing
  resource: https://www.sqlite.org/fts5.html
  title: SQLite FTS5 indexing
- id: git-revision-identifiers
  resource: https://git-scm.com/docs/git-rev-parse
  title: Git revision identifiers
---

# RAG ingestion and chunking

## Purpose

Turn reviewed source documents into reproducible evidence units.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Ingestion flow

Select approved sources -> parse -> preserve identity and provenance -> split into chunks -> index -> evaluate -> publish the index revision. The index is derived/disposable; the reviewed source remains authoritative.[^sqlite-fts5-indexing][^git-revision-identifiers]

Store path, document title, heading/anchor, content hash, source revision, access scope, and freshness information when the serving environment needs them. Rebuild or invalidate records when documents change or are deleted.

## Chunk boundaries

Prefer meaningful headings and paragraphs. Keep a command with its explanation and warning where possible. Fixed-size overlap is a tool, not a universal rule: excessive overlap duplicates evidence and consumes context. Large tables, code fences, and repeated boilerplate need special handling.

The supplied lab detects headings outside fenced code, preserves section anchors, limits chunks to 3,000 characters, and splits unusually long sections. Its bounded splitting is educational; production ingestion should preserve code/table structure more carefully.

## Source lifecycle

The lab accepts a repository root or the `knowledge/` bundle. It preserves repository-relative citation paths, carries simple OKF `status` and `maturity` values into results/prompts, and excludes deprecated concepts. Draft and unclassified sources remain explicitly labeled; a valid citation number does not promote their trust. The two lifecycle fields are read as bounded scalar values, not as a general YAML parser.

## Source boundaries

Use an explicit allowlist of curated areas. The lab excludes raw incoming notes, processed-source archives, `work/`, templates, Git internals, and symlinked content. Public source eligibility is different from user-specific authorization in a private deployment.

```bash
python examples/rag.py ingest --root ../.. --db /tmp/kb-rag.sqlite
```

What it does: rebuilds the lab index from curated repository content when run from `knowledge/llm/rag`. The database must be a dedicated disposable lab database. Its content hash includes the actual files, including uncommitted edits; HEAD alone cannot identify that state.

## Failure modes

PDF extraction errors, missing headings, old deleted chunks, duplicated sources, and encoding mistakes can look like model failures. Inspect retrieved text before tuning prompts. Indexing private material requires access filtering before candidate retrieval, including caches and rerankers.

## Related links

- [SQLite FTS5 indexing](https://www.sqlite.org/fts5.html)
- [Git revision identifiers](https://git-scm.com/docs/git-rev-parse)
- [Provenance and freshness](../../ai/ai-tooling/knowledge-bases/provenance-trust-and-freshness.md)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^sqlite-fts5-indexing]: [SQLite FTS5 indexing](https://www.sqlite.org/fts5.html).
[^git-revision-identifiers]: [Git revision identifiers](https://git-scm.com/docs/git-rev-parse).
