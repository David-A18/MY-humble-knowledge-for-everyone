---
type: "Explanation"
title: "Retrieval budget"
description: "A simple guide to limiting how many documents an assistant fetches while still finding enough evidence."
tags: [ai, ai-tooling, knowledge-bases]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
sources:
  - id: mcp-2026-07-28
    resource: ../references/sources/mcp-2026-07-28.md
    title: Model Context Protocol 2026-07-28 tools
---

# Retrieval budget

A **retrieval budget** limits how much source material an assistant searches
and fetches for one question. Think of a library visit: first look at a short
catalog result, then open the few books likely to answer the question. This
analogy stops at trust: a document can be easy to find and still be outdated
or wrong.

For the question “How do I inspect a restarting Pod?”, an assistant could
search for `CrashLoopBackOff`, fetch the focused troubleshooting page and its
official Kubernetes source, then answer with those references. Fetching every
Kubernetes article would add noise and cost without necessarily improving
the answer. This is an illustrative path, not a measured retrieval test.

## Budget dimensions

| Budget | Example control |
| --- | --- |
| Search hits | Return a short ranked result list, such as five candidates. |
| Snippet size | Return summaries and short snippets first. |
| Fetch depth | Require a reason before following additional links. |
| Returned bytes | Cap total bytes per operation. |
| Reranker calls | Limit model-assisted reranking by measured value. |

## Validation

Use **golden questions**: small test questions with a known expected page.
Record whether the right page appears early enough to fetch, whether the
answer cites it correctly, and whether the budget hides needed evidence.
Increase a limit only when a test shows that the current limit loses useful
material.

An MCP server can expose tools you choose to name `search_knowledge` and
`fetch_knowledge_entry`. The protocol defines tool exposure, not those
particular names or a retrieval budget.[^mcp-2026-07-28]

Check your understanding: If the correct page is the sixth search result but
the assistant sees only five, which limit would you examine first? What
would you measure before increasing it?

[^mcp-2026-07-28]: Model Context Protocol 2026-07-28 tool specification.

## Related links

- [Source schema extraction](source-schema-extraction.md)
- [Pod restarts in a time window](pod-restart-rate.md)
- [MCP source reference](../references/sources/mcp-2026-07-28.md)
- [Back to bundle index](../index.md)
