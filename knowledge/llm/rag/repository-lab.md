---
type: Tutorial
title: Repository-based RAG lab
description: Retrieve cited evidence from this Markdown knowledge base without a vector
  service.
tags:
- llm
- rag
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: python-sqlite3
  resource: https://docs.python.org/3.13/library/sqlite3.html
  title: Python sqlite3
- id: sqlite-fts5
  resource: https://www.sqlite.org/fts5.html
  title: SQLite FTS5
- id: ollama-api
  resource: https://docs.ollama.com/api/chat
  title: Ollama API
---

# Repository-based RAG lab

## Purpose

Retrieve cited evidence from this Markdown knowledge base without a vector service.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Prerequisites and versions

Use Python **3.13** with SQLite FTS5 enabled. The retrieval path uses only the standard library. Check `python -c 'import sqlite3; print(sqlite3.sqlite_version)'` and run the tests before indexing. Optional generation uses your installed Ollama model; no model was downloaded or used during authoring.[^python-sqlite3][^sqlite-fts5][^ollama-api]

## Build and query

Run from the repository root:

```bash
python knowledge/llm/rag/examples/rag.py ingest --root . --db /tmp/kb-rag.sqlite
python knowledge/llm/rag/examples/rag.py search --db /tmp/kb-rag.sqlite 'PeerAuthentication'
python knowledge/llm/rag/examples/rag.py ask --db /tmp/kb-rag.sqlite 'AssumeRoleWithWebIdentity'
python knowledge/llm/rag/examples/rag.py search --db /tmp/kb-rag.sqlite "$(python -c 'import secrets; print(secrets.token_hex(16))')"
python knowledge/llm/rag/examples/test_rag.py
```

What it does: builds a disposable index, returns ranked evidence with Markdown paths/anchors, shows evidence without generation, tests a freshly generated random query, and exercises exclusion/query/citation contracts. The query-generation syntax works in Bash and PowerShell. On Windows use a dedicated temporary-directory database path in place of `/tmp`.

## Expected results

Istio authentication sections should appear among the top five `PeerAuthentication` hits. IRSA/OIDC material should appear for the STS operation. A fresh random query should return no hits; `ask` with that same query returns `NO_EVIDENCE`. A fixed nonsense string printed in this tutorial can match the tutorial itself after ingestion, so generate it at runtime. Query timing and context size are measured separately from optional generation.

## Optional local generation

Start an Ollama server with a model you selected and installed. Use `ask --model YOUR_INSTALLED_MODEL`; the default endpoint is loopback. The model receives only selected public-corpus excerpts and the question. Inspect both answer and evidence. The sample's citation-number check does not prove factual grounding.

The current index schema includes lifecycle fields. Rebuild the disposable database when upgrading this example; the ingestion transaction replaces only its lab-owned index tables.

## Cleanup and limitations

Remove only your disposable SQLite database after closing clients. Do not commit indexes or model outputs. This teaching implementation has no tenant authentication, semantic retrieval, background ingestion, production service, or automatic source-trust assessment. It remains useful as a measurable baseline before adding those features.

## Related links

- [Python sqlite3](https://docs.python.org/3.13/library/sqlite3.html)
- [SQLite FTS5](https://www.sqlite.org/fts5.html)
- [Ollama API](https://docs.ollama.com/api/chat)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^python-sqlite3]: [Python sqlite3](https://docs.python.org/3.13/library/sqlite3.html).
[^sqlite-fts5]: [SQLite FTS5](https://www.sqlite.org/fts5.html).
[^ollama-api]: [Ollama API](https://docs.ollama.com/api/chat).
