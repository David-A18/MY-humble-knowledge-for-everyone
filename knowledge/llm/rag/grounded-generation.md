---
type: Explanation
title: Grounded generation and citations
description: Convert retrieved evidence into an answer with explicit limits.
tags:
- llm
- rag
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: ollama-chat-api
  resource: https://docs.ollama.com/api/chat
  title: Ollama chat API
---

# Grounded generation and citations

## Purpose

Convert retrieved evidence into an answer with explicit limits.

Sources reviewed: 2026-10-29. See the [validation record](../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Prompt contract

Supply the user question separately from numbered evidence records. Each record carries a source path/anchor and bounded text. Instruct the model to support claims with those evidence numbers and state insufficient evidence when needed. Treat retrieved instructions as untrusted data.[^ollama-chat-api]

The lab optionally sends evidence to a local Ollama `/api/chat` endpoint with streaming disabled. Without a model argument it returns retrieved evidence and reports that generation did not run. A local endpoint is a deployment choice, not proof that a model is correct or safe.

```bash
python examples/rag.py ask --db /tmp/kb-rag.sqlite 'How does IRSA obtain credentials?'
python examples/rag.py ask --db /tmp/kb-rag.sqlite --model YOUR_INSTALLED_MODEL 'How does IRSA obtain credentials?'
```

What it does: first inspects evidence without a model; then optionally requests a locally generated answer. Replace the model with one installed in your Ollama server and record its exact tag/digest. Downloading models can be large and is separate from this lab.

## Citations

The sample rejects absent or out-of-range numeric citation markers in a generated answer. It returns source metadata separately. This checks citation syntax only: a valid number does not prove the cited text supports the associated claim. Human or evaluated automated checks must assess entailment and completeness.

## Missing and conflicting evidence

No lexical hits produces an explicit no-evidence result without calling a model. Non-empty but weak evidence still needs judgment. Conflicting sources should be surfaced with authority/freshness context rather than silently combined.

## Failure handling

Bound candidate count, per-chunk size, total context, request size, and generation timeout. Report retrieval time separately from generation time. Handle unavailable models and malformed responses clearly. Do not give the generation step shell, cloud, or repository-write permissions merely because it can answer questions.

## Related links

- [Ollama chat API](https://docs.ollama.com/api/chat)
- [Knowledge-base security](../../ai/ai-tooling/knowledge-bases/security-and-governance.md)
- [Back to parent index](index.md)
- [Back to major area](../index.md)
- [Back to root index](../../../README.md)

[^ollama-chat-api]: [Ollama chat API](https://docs.ollama.com/api/chat).
