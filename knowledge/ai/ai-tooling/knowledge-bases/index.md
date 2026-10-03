# Agent knowledge bases

## Purpose

This section is an engineering reference for building, operating, serving, securing, evaluating, and maintaining knowledge bases for AI agents and LLM systems.

The reference architecture is:

```text
authoritative producers
  -> deterministic extraction
  -> normalized knowledge representation
  -> provenance, trust, and freshness metadata
  -> Git-backed knowledge corpus
  -> disposable retrieval artifacts
  -> retrieval layer
  -> read-only serving layer
  -> optional MCP adapter
  -> agents and humans
```

The maintenance loop is separate:

```text
producer changes
  -> reconciliation
  -> affected knowledge detection
  -> deterministic regeneration where possible
  -> agent reasoning or enrichment where needed
  -> validation
  -> proposed Git diff or PR
  -> human review
  -> merge
  -> new authoritative corpus state
```

## Core principles

| Principle | Engineering rule |
| --- | --- |
| Git is the knowledge source of truth | Indexes, embeddings, graph indexes, caches, and retrieval artifacts are disposable and rebuildable from Git. |
| Facts are deterministic | Parse machine-readable producers with code; do not ask an LLM to invent exact facts. |
| Meaning may be reasoned | Use agents for explanation, relationships, decision guidance, troubleshooting, and summarization. |
| Every write is reviewable | The serving path is read-only; maintenance produces patches or PRs behind a separate boundary. |
| Freshness comes from reconciliation | Missed events should increase latency, not permanently hide stale knowledge. |
| Guarantees live in code | Required metadata, path constraints, source links, ACLs, and generated-region rules need validation and policy. |
| Retrieval is a budget | Return enough context to answer, not the largest possible context. |
| Strict producer, tolerant consumer | Enforce strong internal rules while remaining compatible with conformant third-party OKF bundles. |

## Failure modes

| Failure | What happens | Design response |
| --- | --- | --- |
| Discovery failure | The answer exists but the agent cannot find it and reconstructs a weaker answer. | Complete indexes, aliases, metadata, search tests, and parent navigation. |
| Retrieval and token-cost failure | Finding evidence costs more time, tokens, and tool calls than answering. | Progressive disclosure, small search results, section fetches, and retrieval budgets. |
| Silent staleness | Documentation looks valid but its producer changed or disappeared. | Revision tracking, hashing, stale-after metadata, and scheduled reconciliation. |

## Reference guides

| Guide | Use it for |
| --- | --- |
| [Reference architecture](reference-architecture.md) | Follow an official source into a curated article, a Git revision, reader views, and a later correction. |
| [OKF v0.2](okf-v0.2.md) | Specification-level OKF audit, conformance rules, lifecycle, actors, sources, trust, freshness, and Attested Computation. |
| [Knowledge standards landscape](knowledge-standards-landscape.md) | Choose a format or tool by its job: describe a system, teach a concept, connect knowledge, find it, or serve it to an assistant. |
| [Retrieval and context efficiency](retrieval-and-context-efficiency.md) | Understand the search-to-fetch path, result trust signals, measured budgets, and when another ranking method is justified. |
| [Provenance, trust, and freshness](provenance-trust-and-freshness.md) | Tell where a claim came from, how much review supports it, and whether its source may have changed; follow an invented schema change from detection to review and see why unresolved conflicts are surfaced. |
| [Security and governance](security-and-governance.md) | Understand why retrieved text cannot grant authority, how document access is checked, and why edits take a separate reviewed path. |
| [Evaluation and quality](evaluation-and-quality.md) | Design a small golden-question test that scores content, ranking, answer grounding, freshness, and efficiency separately, with a worked hit@k and reciprocal-rank example. |
| [Knowledge-base examples](examples/index.md) | Public-safe OKF and agent-knowledge-base examples. |
| [Knowledge-base upgrade hub](../../../../knowledge-base-upgrade/README.md) | Repository-specific feature, tool, skill, MCP, and instruction scaffold for upgrading this knowledge base. |

## How everything fits together

| Layer | Role in the architecture |
| --- | --- |
| OpenAPI, AsyncAPI, JSON Schema, Terraform, Kubernetes manifests, SQL schemas | Authoritative machine-readable system descriptions. |
| Deterministic renderers | Convert source facts into machine-owned knowledge regions. |
| OKF | Portable curated knowledge representation and package. |
| Git | Versioned knowledge source of truth for the derived corpus. |
| RDF, JSON-LD, SKOS, OWL, PROV, SHACL | Optional richer semantic, provenance, taxonomy, ontology, and validation layer. |
| Search, BM25, embeddings, vector indexes, graph indexes | Derived retrieval mechanisms. |
| MCP | Optional agent-facing access protocol for read-only search and fetch operations. |
| LLM or agent | Consumer, reasoner, explainer, and maintenance assistant. |
| PR workflow | Controlled write path for authoritative corpus changes. |

## Related links

- [Knowledge-base creation, management, and optimization](../knowledge-bases-creation-management-and-optimization.md)
- [Model Context Protocol](../model-context-protocol.md)
- [Back to AI tooling](../index.md)
- [Back to AI index](../../index.md)
- [Back to LLM index](../../../llm/index.md)
- [Back to root index](../../../../README.md)
