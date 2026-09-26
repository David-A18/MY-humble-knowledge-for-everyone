# Source ingestion router

## Purpose

Use this skill when converting raw Markdown notes into curated knowledge-base pages.

## Workflow

1. Read [source ingestion instructions](../../../sources/AGENTS.md), the target area index, and the repository writing standard.
2. Inspect source metadata for `principal_topic`, `provider`, and `target_section`.
3. Infer missing metadata from content, then verify the destination against existing routes.
4. Prefer updating a focused existing page when the topic already has a home.
5. Create a new page only when readers would search for the topic separately.
6. Preserve provenance by updating [ingestion register](../../../sources/processed/ingestion-register.md) when raw notes move to processed storage.
7. Update destination indexes and related links.
8. Record open questions instead of inventing missing facts.

## Routing hints

| Source signal | Preferred route |
| --- | --- |
| AWS, Azure, or Google Cloud | [Cloud](../../../knowledge/cloud/index.md) and provider subsection. |
| Crossplane concepts or providers | [Kubernetes Crossplane](../../../knowledge/kubernetes/crossplane/index.md). |
| Multi-technology platform workflow | [Cross-topic guides](../../../knowledge/cross-topic-guides/index.md). |
| Kafka, MongoDB, or data modeling | [Databases](../../../knowledge/databases/index.md). |
| AI tools, MCP, skills, or knowledge-base operations | [AI tooling](../../../knowledge/ai/ai-tooling/index.md) or [knowledge-base upgrade hub](../../README.md). |

## Related links

- [Skill index](../README.md)
- [Sources](../../../sources/README.md)
- [Knowledge-base upgrade hub](../../README.md)
- [Back to root index](../../../README.md)
