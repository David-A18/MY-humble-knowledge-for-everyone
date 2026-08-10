# Security and governance

## Purpose

This guide defines the security model for AI knowledge bases, retrieval systems, MCP serving, and agent-assisted maintenance.

## Core security rule

Retrieved knowledge is untrusted input. It is evidence for the model to reason over, not executable instruction text.

Treat every document, snippet, source page, MCP response, Markdown block, URL, and metadata field as potentially malicious until validated and authorized.

## Threats and controls

| Threat | Control |
| --- | --- |
| Prompt injection through documents | Strip or label instructions in retrieved content, keep system policy separate, and train agents to treat documents as evidence. |
| Indirect prompt injection | Apply the same controls to web pages, tickets, emails, comments, and source files loaded through tools. |
| RAG or data poisoning | Require source allowlists, review, provenance, validation, and rollback. |
| Vector or embedding poisoning | Rebuild indexes from reviewed Git corpus, validate metadata, and monitor retrieval anomalies. |
| Cross-tenant or cross-context leakage | Enforce authorization before retrieval and again before fetch. |
| Metadata or ACL bypass | Filter by ACL at index time or query planning time, not only after results are returned. |
| Secret leakage | Run secret detection during ingestion, validation, and PR review. |
| Malicious Markdown or unsafe URLs | Sanitize rendered Markdown, block dangerous HTML, and classify external links. |
| Path traversal or symlink abuse | Canonicalize paths, enforce allowlists, and reject links escaping the corpus root. |
| SSRF in source ingestion | Fetch only from allowed domains and networks with sandboxed fetchers. |
| Compromised external sources | Pin revisions or snapshots where possible and surface source authority and freshness. |
| Supply-chain attack | Pin parser, renderer, MCP server, and indexer dependencies. |
| Malicious MCP responses | Validate output schemas and treat tool output as untrusted input. |
| Agent privilege escalation | Separate read-only serving credentials from maintenance credentials. |
| Write-path abuse | Use propose-only tools, branches, PRs, validation, and human review. |
| Stale but trusted content | Combine trust tiers with freshness and reconciliation lag. |
| Fabricated citations | Validate citation IDs against source metadata and fetched evidence. |

## Retrieval-time authorization

Filtering after retrieval is not equivalent to preventing unauthorized retrieval.

Good authorization sequence:

1. Authenticate the caller.
2. Resolve authorization scope.
3. Limit candidate indexes or shards to authorized content.
4. Search and rank only authorized candidates.
5. Fetch only authorized documents or sections.
6. Log the corpus revision, query, result IDs, denied IDs, and authorization decision.

If unauthorized content reaches the ranker or model and is then filtered out, the system may still leak through timing, logs, embeddings, summaries, or side effects.

## Serving and maintenance boundary

| Boundary | Credentials | Allowed behavior |
| --- | --- | --- |
| Read-only serving | Least-privilege search and fetch identity | Search, fetch, cite, and report metadata. |
| Maintenance proposal | Limited branch or patch identity | Generate diffs, run validation, and open review artifacts. |
| Merge or publication | Human or protected automation | Merge reviewed changes and rebuild serving artifacts. |

Do not expose normal MCP tools that silently mutate the production corpus. If privileged maintenance tools exist, give them separate names, scopes, audit logs, and approval requirements.

## Governance mapping

NIST AI RMF 1.0 and the NIST Generative AI Profile are governance and risk-management guidance, not knowledge formats. OWASP GenAI guidance is security guidance, not a corpus representation.

Knowledge-base architecture supports governance through:

- Provenance.
- Auditability.
- Human review.
- Access control.
- Evaluation.
- Incident traceability.
- Freshness controls.
- Reproducible corpus revisions.
- Separation of read and write credentials.

## Secure ingestion checklist

- Use source allowlists.
- Sandbox parsers and renderers.
- Reject private URLs, credentials, and customer-specific identifiers.
- Canonicalize paths and reject escapes.
- Validate frontmatter and generated regions.
- Preserve source references.
- Run secret detection.
- Require review for new producers.
- Record parser and renderer versions.
- Store only public-safe or approved source snapshots.

## Related links

- Official guidance: [OWASP GenAI Security Project](https://genai.owasp.org/)
- Official guidance: [OWASP Top 10 for LLM and GenAI Apps 2025](https://genai.owasp.org/llm-top-10/)
- Official guidance: [NIST AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
- Official guidance: [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [Reference architecture](reference-architecture.md)
- [Retrieval and context efficiency](retrieval-and-context-efficiency.md)
- [Back to agent knowledge bases](README.md)
- [Back to AI tooling](../README.md)
- [Back to root index](../../../README.md)
