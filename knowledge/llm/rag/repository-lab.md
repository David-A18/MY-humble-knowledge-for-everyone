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

Use Python **3.13 or newer** with SQLite FTS5 enabled. The retrieval path uses only the standard library. Check `python -c 'import sqlite3; print(sqlite3.sqlite_version)'` and run the tests before indexing. Optional generation uses your installed Ollama model; no model was downloaded or used during authoring.[^python-sqlite3][^sqlite-fts5][^ollama-api]

## Build and query

Run from the repository root:

```bash
python knowledge/llm/rag/examples/rag.py ingest --root . --db /tmp/kb-rag.sqlite
python knowledge/llm/rag/examples/rag.py search --db /tmp/kb-rag.sqlite 'PeerAuthentication'
python knowledge/llm/rag/examples/rag.py ask --db /tmp/kb-rag.sqlite 'AssumeRoleWithWebIdentity'
python knowledge/llm/rag/examples/rag.py search --db /tmp/kb-rag.sqlite "$(python -c 'import secrets; print(secrets.token_hex(16))')"
python knowledge/llm/rag/examples/test_rag.py
python scripts/evaluate-retrieval.py --unanswerable tests/unanswerable-questions.yaml --show-misses
```

What it does: builds a disposable index, returns ranked evidence with Markdown paths/anchors, shows evidence without generation, tests a freshly generated random query, exercises exclusion/query/citation contracts, and scores the golden questions. The query-generation syntax works in Bash and PowerShell. On Windows use a dedicated temporary-directory database path in place of `/tmp`.

## Expected results

Istio authentication sections should appear among the top five `PeerAuthentication` hits. IRSA/OIDC material should appear for the STS operation. A fresh random query should return no hits; `ask` with that same query returns `NO_EVIDENCE`. A fixed nonsense string printed in this tutorial can match the tutorial itself after ingestion, so generate it at runtime. Query timing and context size are measured separately from optional generation.

Each hit carries the concept's `status`, `maturity`, `type`, `tags`, `source_ids`, and `stale_after`, plus a `trust_tier` and `stale` flag derived as OKF sections 5.3 and 5.5 define them. These signals are shown, not used to rank: almost every concept is an unverified draft, so a trust boost would carry no information today.

`search` also reports `best_coverage`, the share of the question's rare-word weight found in the best concept, and `sufficient`, which is true at 0.5 or above. `search` always returns its hits so a person or agent can inspect weak matches. `ask` refuses with `NO_EVIDENCE` when evidence is not sufficient, without calling a model. Word overlap cannot tell whether a page truly answers a question, so a coverage pass is a screen and not proof of grounding.

## Connect an AI host

[`scripts/kb-mcp-server.py`](../../../scripts/kb-mcp-server.py) serves `search_knowledge`, `fetch_page`, and `list_routes` over MCP stdio. It builds a disposable index at startup and has no write tools. It reads only indexed concepts. The repository's `.mcp.json` registers it for hosts that read project configuration, and `python scripts/test-kb-mcp-server.py` exercises it over stdio.

## Optional local generation

Start an Ollama server with a model you selected and installed. Use `ask --model YOUR_INSTALLED_MODEL`; the default endpoint is loopback. The model receives only selected public-corpus excerpts and the question. Inspect both answer and evidence. `ask` rejects an answer with no citation or an invented one, and reports `uncited_paragraphs` without rejecting it. Neither check proves factual grounding.

Add `--timeout 300` on a CPU-only machine. On 2026-11-02, `qwen3:4b` (`359d7dd4bcda`) ran ten questions on CPU, keeping about 3.9 GB in memory. Two answerable questions hit a 280-second limit. Five completed answers matched their retrieved evidence on reading, and the model refused both off-topic questions that passed the coverage check. This is a small spot check, not a measured answer-quality score. The model ignored `think: false`, so `ask` also sends `/no_think` and removes any text before `</think>`.

The current index schema includes lifecycle fields. Rebuild the disposable database when upgrading this example; the ingestion transaction replaces only its lab-owned index tables.

## Cleanup and limitations

Remove only your disposable SQLite database after closing clients. Do not commit indexes or model outputs. This implementation has no tenant authentication, semantic retrieval, background ingestion, or automatic source-trust assessment. Measure with the golden cases before adding those features.

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
