# ADR-0002: Source ingestion and topic taxonomy

Status: Accepted

## Context

The knowledge base needs a clear place for raw Markdown notes before they are converted into curated documentation. It also needs explicit routes for topics that are expected to grow beyond the initial Git, Terraform, Kubernetes, and AWS sections.

## Decision

Create a root-level [sources](../sources/README.md) area with incoming and processed folders. Agents will classify raw files, transform them into the correct article structure, update indexes and links, then archive processed raw files.

Create a cloud parent route at [cloud](../cloud/README.md), move existing AWS documentation under [cloud/aws](../cloud/aws/README.md), and reserve provider routes for Azure and Google Cloud. Add initial top-level route indexes for security, FinOps, DevOps, programming languages, MLOps, AI, AI agents, LLM, ML, and solutions architect content.

## Consequences

- Raw notes have a safe staging area before becoming curated documentation.
- AWS content becomes part of a provider hierarchy instead of a standalone top-level area.
- Future agents can place new material using a consistent topic taxonomy.
- Internal links must be updated when moving provider-specific content under `cloud/`.

## Related links

- [Sources](../sources/README.md)
- [Source ingestion instructions](../sources/AGENTS.md)
- [Cloud](../cloud/README.md)
- [AI agent router](../AGENTS.md)
- [Back to decision records](README.md)
- [Back to root index](../README.md)
