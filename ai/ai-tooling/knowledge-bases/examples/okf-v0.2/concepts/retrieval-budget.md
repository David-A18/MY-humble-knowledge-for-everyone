---
type: Reference
title: Retrieval budget
description: Context-efficiency model for bounded search and fetch operations.
tags: [retrieval, context, evaluation]
status: stable
generated: { by: process:example-renderer, at: 2026-08-08T10:05:00Z }
verified:
  - { by: human:kb-reviewer, at: 2026-08-08T10:35:00Z }
stale_after: 2026-11-08
usage_window: 2026-08
sources:
  - id: mcp-2026-07-28
    resource: references/sources/mcp-2026-07-28.md
    title: Model Context Protocol 2026-07-28 overview
    author: process:mcp-docs
    usage_count: 7
    last_modified: 2026-07-28
---

# Retrieval budget

Retrieval should return enough evidence to answer the question, not every potentially related document. A small read-only serving layer can expose search and fetch capabilities while hiding whether the implementation uses lexical search, semantic reranking, or another derived index.[^mcp-2026-07-28]

## Budget dimensions

| Budget | Example control |
| --- | --- |
| Search hits | Return a bounded result list. |
| Snippet size | Return summaries and short snippets first. |
| Fetch depth | Require a reason before following additional links. |
| Returned bytes | Cap total bytes per operation. |
| Reranker calls | Limit model-assisted reranking by measured value. |

## Validation

Use golden questions. The expected authoritative concept should appear high enough that the agent can fetch it without expensive exploration.

[^mcp-2026-07-28]: Model Context Protocol 2026-07-28 overview.

## Related links

- [Source schema extraction](source-schema-extraction.md)
- [Pod restart rate](pod-restart-rate.md)
- [MCP source reference](../references/sources/mcp-2026-07-28.md)
- [Back to bundle index](../index.md)
