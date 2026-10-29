---
type: Explanation
title: RAG evaluation, security, and operations
description: Measure retrieval and answer quality independently and protect the full
  evidence path.
tags:
- llm
- rag
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: fts5
  resource: https://www.sqlite.org/fts5.html
  title: FTS5
- id: owasp-llm-prompt-injection
  resource: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  title: OWASP LLM prompt injection
---

# RAG evaluation, security, and operations

## Purpose

Measure retrieval and answer quality independently and protect the full evidence path.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Retrieval evaluation

Create golden questions with expected documents/sections, including exact identifiers, paraphrases, ambiguous terms, missing topics, and conflicting/stale evidence. Measure Recall@k, rank of the first useful hit, and context size. Separate ingestion failures from ranking failures.[^fts5][^owasp-llm-prompt-injection]

The sample tests core contracts and includes real-corpus golden checks for Istio and IRSA. Its small set is a smoke test, not evidence of production answer quality.

## Answer evaluation

Assess correctness, groundedness, citation support/completeness, conflict handling, and justified refusal. Test retrieval and generation separately so a good model does not hide weak retrieval. Track latency, returned bytes, generation cost, and retrieval revision.

## Security

Filter access before retrieval and maintain scope through reranking, caches, and citations. Review ingestion sources for poisoning and prompt injection. Never place credentials in chunks, telemetry, or test snapshots. Retrieved code is evidence to explain, not code to execute.

## Operations

Version source eligibility rules, chunker, query normalization, and index schema. Record a corpus content hash; HEAD plus uncommitted content requires additional identification. Rebuild indexes after deletion/permission changes and invalidate stale caches. Monitor zero-hit queries, stale results, latency, and authorization failures without collecting sensitive question text unnecessarily.

## Release criteria

A changed retriever should preserve expected evidence on the golden set within an agreed budget. A changed generator should preserve supported claims and citation quality. Evaluate model/version changes before replacing the deployed baseline. Reuse the repository's existing governance and evaluation guidance rather than defining conflicting standards here.

## Related links

- [FTS5](https://www.sqlite.org/fts5.html)
- [OWASP LLM prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [Evaluation and quality](../../ai/ai-tooling/knowledge-bases/evaluation-and-quality.md)
- [Security and governance](../../ai/ai-tooling/knowledge-bases/security-and-governance.md)
- [Freshness](../../ai/ai-tooling/knowledge-bases/provenance-trust-and-freshness.md)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^fts5]: [FTS5](https://www.sqlite.org/fts5.html).
[^owasp-llm-prompt-injection]: [OWASP LLM prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).
