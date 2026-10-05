---
type: "Playbook"
title: "Source schema extraction"
description: "Shows why software should parse API schemas before an assistant explains them."
tags: [ai, ai-tooling, knowledge-bases]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
sources:
  - id: openapi-3-2
    resource: ../references/sources/openapi-3-2.md
    title: OpenAPI Specification v3.2.0
  - id: json-schema-2020-12
    resource: ../references/sources/json-schema-2020-12.md
    title: JSON Schema Draft 2020-12
---

# Source schema extraction

When an API already has a machine-readable description, a parser can copy
exact paths and field constraints. An assistant can then explain **why** a
reader would use an operation. This divides exact extraction from teaching:
the assistant should not guess a field the parser can read.

OpenAPI describes HTTP operations, while JSON Schema defines validation
rules for JSON data.[^openapi-3-2][^json-schema-2020-12] Imagine a made-up
`POST /lessons` endpoint: a parser finds its required `title` field and
response code; a writer explains how a learner creates a lesson. The
endpoint and its schema are illustrative and do not exist in this bundle.

## Machine-owned region

```text
producer: public-example-api
source: openapi.yaml
renderer: schema-summary-renderer/1.0.0
generated_region_policy: renderer-only
```

What it does: illustrates a boundary that would be regenerated from source
instead of edited by a model. `public-example-api`, `openapi.yaml`, and the
renderer name are invented placeholders, not a working pipeline.

## Agent-owned explanation

An agent may explain when an endpoint should be used, how it relates to adjacent workflows, or what operational checks matter. It should not invent request fields or response fields that the parser can read exactly.

## Validation

- Re-run the renderer with the same source revision and renderer version.
- Compare the machine-owned region byte-for-byte or by structured output.
- Reject hand edits inside protected generated regions.
- Require citations for claims that depend on external specifications.

Check your understanding: If an API description changes a required field,
which part should be regenerated? Which part still needs an explanation for
the learner?

[^openapi-3-2]: OpenAPI Specification v3.2.0.
[^json-schema-2020-12]: JSON Schema Draft 2020-12.

## Related links

- [Retrieval budget](retrieval-budget.md)
- [OpenAPI source reference](../references/sources/openapi-3-2.md)
- [JSON Schema source reference](../references/sources/json-schema-2020-12.md)
- [Back to bundle index](../index.md)
