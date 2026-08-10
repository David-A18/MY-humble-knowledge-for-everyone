---
type: Playbook
title: Source schema extraction
description: Deterministic extraction pattern for turning machine-readable source schemas into machine-owned knowledge regions.
tags: [knowledge-base, deterministic-extraction, schemas]
status: stable
generated: { by: process:example-renderer, at: 2026-08-08T10:00:00Z }
verified:
  - { by: human:kb-reviewer, at: 2026-08-08T10:30:00Z }
stale_after: 2026-11-08
usage_window: 2026-08
sources:
  - id: openapi-3-2
    resource: references/sources/openapi-3-2.md
    title: OpenAPI Specification v3.2.0
    author: process:openapi-initiative
    usage_count: 12
    last_modified: 2025-09-19
  - id: json-schema-2020-12
    resource: references/sources/json-schema-2020-12.md
    title: JSON Schema Draft 2020-12
    author: process:json-schema-project
    usage_count: 9
    last_modified: 2022-06-16
---

# Source schema extraction

Use deterministic parsers for machine-readable facts. HTTP API operations should come from OpenAPI descriptions, and JSON shape constraints should come from JSON Schema where those producers exist.[^openapi-3-2][^json-schema-2020-12]

## Machine-owned region

```text
producer: public-example-api
source: openapi.yaml
renderer: schema-summary-renderer/1.0.0
generated_region_policy: renderer-only
```

What it does: records the boundary that must be regenerated from source instead of edited by a model.

## Agent-owned explanation

An agent may explain when an endpoint should be used, how it relates to adjacent workflows, or what operational checks matter. It should not invent request fields or response fields that the parser can read exactly.

## Validation

- Re-run the renderer with the same source revision and renderer version.
- Compare the machine-owned region byte-for-byte or by structured output.
- Reject hand edits inside protected generated regions.
- Require citations for claims that depend on external specifications.

[^openapi-3-2]: OpenAPI Specification v3.2.0.
[^json-schema-2020-12]: JSON Schema Draft 2020-12.

## Related links

- [Retrieval budget](retrieval-budget.md)
- [OpenAPI source reference](../references/sources/openapi-3-2.md)
- [JSON Schema source reference](../references/sources/json-schema-2020-12.md)
- [Back to bundle index](../index.md)
