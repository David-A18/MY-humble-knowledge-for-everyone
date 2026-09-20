---
type: "Explanation"
title: "Knowledge standards landscape"
description: "This guide classifies the standards, specifications, conventions, protocols, and implementation technologies that appear around AI knowledge bases. The goal is to avoid treating every useful file format or retrieval tool as the same kind of \"standard.\""
tags: [ai, ai-tooling, knowledge-bases]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# Knowledge standards landscape

## Purpose

This guide classifies the standards, specifications, conventions, protocols, and implementation technologies that appear around AI knowledge bases. The goal is to avoid treating every useful file format or retrieval tool as the same kind of "standard."

## Landscape summary

| Layer | Technology | Current status as of 2026-08-08 | Steward | Relationship to an AI knowledge base |
| --- | --- | --- | --- | --- |
| Knowledge packaging | OKF v0.2 | Open specification | GoogleCloudPlatform `open-knowledge-format` | Portable Markdown and YAML-frontmatter bundle for humans and agents. |
| Graph data model | RDF 1.1 | W3C Recommendation, 25 February 2014 | W3C | Machine-interpretable triples, graphs, datasets, and identifiers. |
| Graph data model draft | RDF 1.2 | W3C Candidate Recommendation Snapshot, 7 April 2026 | W3C | Upcoming RDF update; do not present as final Recommendation until W3C advances it. |
| Linked Data JSON serialization | JSON-LD 1.1 | W3C Recommendation, 16 July 2020 | W3C | JSON serialization for Linked Data and RDF-compatible data. |
| RDF vocabulary schema | RDF Schema 1.1 | W3C Recommendation, 25 February 2014 | W3C | Lightweight classes and properties for RDF vocabularies. |
| Ontology | OWL 2 | W3C Recommendation, second edition 11 December 2012 | W3C | Formal ontologies and reasoning over classes, properties, and constraints. |
| Taxonomy and thesaurus | SKOS | W3C Recommendation, 18 August 2009 | W3C | Controlled vocabularies, broader/narrower/related relationships, and labels. |
| RDF validation | SHACL | W3C Recommendation, 20 July 2017 | W3C | Deterministic validation of RDF graphs against shapes. |
| Provenance model | PROV and PROV-O | W3C Recommendations, 30 April 2013 | W3C | Interoperable provenance entities, activities, and agents. |
| HTTP API description | OpenAPI 3.2.0 | Specification, 19 September 2025 | OpenAPI Initiative, Linux Foundation | Authoritative machine-readable HTTP API descriptions for deterministic extraction. |
| Event API description | AsyncAPI 3.1.0 | Specification, 31 January 2026 | AsyncAPI Initiative | Authoritative machine-readable async API and event-channel descriptions. |
| JSON validation | JSON Schema 2020-12 | Specification draft family, published 16 June 2022 | JSON Schema project | Deterministic schema validation for JSON documents and API payloads. |
| Agent runtime access | MCP 2026-07-28 | Protocol specification | Model Context Protocol project | Agent-facing protocol for tools, resources, prompts, and read-only knowledge serving. |
| Agent repository instructions | AGENTS.md | Community convention | agents.md project and tool vendors | Project instructions for coding agents; not a knowledge representation standard. |
| LLM source map | `llms.txt` | Community proposal | Answer.AI and community | Optional website source map for LLM-oriented content; not access control or a formal web standard. |
| Retrieval implementation | BM25, SQLite FTS, OpenSearch, pgvector, FAISS, graph indexes | Implementations | Varies | Disposable indexes built from the corpus; not authoritative knowledge. |

## OKF and semantic-web standards

OKF occupies the packaging and curated-knowledge layer. RDF, JSON-LD, RDFS, OWL, SKOS, SHACL, and PROV occupy semantic representation, ontology, taxonomy, validation, and provenance layers.

Use OKF to package human-readable Markdown with structured trust metadata. Add semantic-web technologies only when the system needs machine-interpretable relationships, exchange with graph-based consumers, formal reasoning, controlled vocabularies, RDF validation, or interoperable provenance beyond OKF frontmatter.

OKF complements semantic-web standards because it can reference or embed semantic artifacts, but it does not replace them.

## Domain schemas are producers

OpenAPI, AsyncAPI, JSON Schema, Terraform, Kubernetes manifests, SQL schemas, and repository metadata should be treated as authoritative producers for machine-readable facts.

Do not rewrite those facts with an LLM. Parse them, normalize them, and generate machine-owned knowledge regions. Then let agents write explanation and operational guidance around those deterministic regions.

## MCP is a serving adapter

MCP exposes runtime capabilities. It does not define the internal knowledge representation.

```text
Git or OKF corpus
  -> retrieval service
  -> read-only knowledge operations
  -> MCP server
  -> agent
```

The agent should not need to know whether retrieval uses BM25, OpenSearch, SQLite FTS, pgvector, FAISS, a graph index, or a hybrid pipeline.

## AGENTS.md and llms.txt

`AGENTS.md` is useful for repository instructions to agents. It should not be confused with a knowledge corpus format. Put operating rules, build commands, path boundaries, and validation expectations there.

`llms.txt` is useful as a curated website source map for LLM consumers. It is not a W3C or IETF standard, not an access-control mechanism, and not a replacement for sitemaps, authentication, robots controls, or structured corpus metadata.

## Choosing the right layer

| Problem | Use | Do not use |
| --- | --- | --- |
| Package curated Markdown with provenance and freshness | OKF | RDF as a document authoring format unless semantic graph exchange is required. |
| Represent typed relationships across systems | RDF or JSON-LD | Plain Markdown links as the only machine-readable relationship model. |
| Maintain controlled vocabulary labels and hierarchy | SKOS | Ad hoc tag lists when cross-system taxonomy matters. |
| Enforce graph constraints | SHACL | Prompt instructions. |
| Define formal ontology reasoning | OWL | OKF `type` strings. |
| Describe HTTP API facts | OpenAPI | Agent-written endpoint summaries as authoritative facts. |
| Describe event channels and messages | AsyncAPI | Unstructured prose as the source of truth. |
| Expose knowledge to agents at runtime | MCP | Direct filesystem access when authorization and audit are required. |
| Improve retrieval after manual navigation fails | Lexical search, then measured semantic reranking | A vector database by default. |

## Related links

- Official specification: [OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)
- Official specification: [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/)
- Candidate Recommendation: [RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/)
- Official specification: [JSON-LD 1.1](https://www.w3.org/TR/json-ld/)
- Official specification: [OpenAPI 3.2.0](https://spec.openapis.org/oas/v3.2.0.html)
- Official specification: [AsyncAPI 3.1.0](https://www.asyncapi.com/docs/reference/specification/v3.1.0)
- Official specification: [MCP 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/index)
- [OKF v0.2](okf-v0.2.md)
- [Reference architecture](reference-architecture.md)
- [Back to agent knowledge bases](index.md)
- [Back to AI tooling](../index.md)
- [Back to root index](../../../../README.md)
