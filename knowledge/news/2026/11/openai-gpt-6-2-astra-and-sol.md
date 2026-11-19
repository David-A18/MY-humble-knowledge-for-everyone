---
type: News Brief
title: OpenAI releases GPT-6.2 Astra and Sol
description: OpenAI's November 17 release adds a top-tier and an everyday model to ChatGPT Work, Codex, and the API, with tighter cybersecurity safeguards.
tags: [news, ai, llm]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
published: 2026-11-19
stale_after: 2027-02-19
sources:
  - id: openai-announcement
    resource: https://openai.com/index/introducing-gpt-6-2-astra-sol/
    title: Introducing GPT-6.2 Astra and Sol
  - id: openai-model-page
    resource: https://developers.openai.com/api/docs/models/gpt-6.2-astra
    title: GPT-6.2 Astra model documentation
  - id: openai-system-card
    resource: https://deploymentsafety.openai.com/gpt-6-2-astra-sol
    title: GPT-6.2 Astra and Sol system card
---

# OpenAI releases GPT-6.2 Astra and Sol

## What happened

On 17 November 2026, OpenAI released two models: **GPT-6.2 Astra**, its
top-tier model for complex professional work, and **GPT-6.2 Sol**, a cheaper
model for everyday tasks. Both are available in ChatGPT Work, Codex, and the
API for paid plans.[^openai-announcement] OpenAI's system card says both models
launch with tighter safeguards for cybersecurity use.[^openai-system-card]

## Why it matters

New models change the cost, speed, and quality of anything built on them:
coding assistants, chat tools, and retrieval-augmented generation (RAG)
systems. A newer model is not automatically better for your task, and an
application that silently switches models can change its answers overnight.

## What to do

- If you call the API, pin an exact model ID and switch on purpose, not by
  default.
- Before switching, re-run your own evaluation questions and compare quality,
  latency, and cost. The [RAG evaluation guide](../../../llm/rag/evaluation-security-and-operations.md)
  shows how to separate retrieval quality from answer quality.
- Check current prices and limits on the model page before estimating
  costs.[^openai-model-page]

## Related links

- [November 2026 roundup](index.md)
- [News](../../index.md)
- [News editorial policy](../../../../governance/news-editorial-policy.md)

[^openai-announcement]: [Introducing GPT-6.2 Astra and Sol](https://openai.com/index/introducing-gpt-6-2-astra-sol/)
[^openai-model-page]: [GPT-6.2 Astra model documentation](https://developers.openai.com/api/docs/models/gpt-6.2-astra)
[^openai-system-card]: [GPT-6.2 Astra and Sol system card](https://deploymentsafety.openai.com/gpt-6-2-astra-sol)
