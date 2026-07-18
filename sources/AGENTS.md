# Source ingestion instructions

Use these instructions when processing raw Markdown files from [incoming](incoming/README.md). The goal is to turn rough notes into useful, linked, validated knowledge-base content without losing source traceability.

> [!IMPORTANT]
> Read the root [AI agent router](../AGENTS.md), [AI agent context](../context.md), [AI documentation instructions](../instructions.md), and [Contributing](../CONTRIBUTING.md) before ingesting source files.

## Source metadata

Raw files may include this optional front matter:

```yaml
---
principal_topic:
provider:
target_section:
status: raw
---
```

Use these values when present, but verify them against the actual content.

| Field | Accepted values |
| --- | --- |
| `principal_topic` | `cloud`, `kubernetes`, `git`, `security`, `finops`, `devops`, `programming-languages`, `mlops`, `ai`, `ai-agents`, `llm`, `ml`, `solutions-architect` |
| `provider` | `aws`, `azure`, `gcloud` for provider-specific cloud content |
| `target_section` | Relative path to the preferred destination section or article |

## Classification routes

| Raw topic | Destination |
| --- | --- |
| AWS-specific cloud content | [cloud/aws](../cloud/aws/README.md) |
| Azure-specific cloud content | [cloud/azure](../cloud/azure/README.md) |
| Google Cloud content | [cloud/gcloud](../cloud/gcloud/README.md) |
| Provider-neutral cloud content | [cloud](../cloud/README.md) |
| Kubernetes content | [kubernetes](../kubernetes/README.md) |
| Git content | [git](../git/README.md) |
| Security content | [security](../security/README.md) |
| FinOps content | [finops](../finops/README.md) |
| DevOps content | [devops](../devops/README.md) |
| Programming language content | [programming-languages](../programming-languages/README.md) |
| MLOps content | [mlops](../mlops/README.md) |
| AI content | [ai](../ai/README.md) |
| AI agent content | [ai-agents](../ai-agents/README.md) |
| LLM content | [llm](../llm/README.md) |
| ML content | [ml](../ml/README.md) |
| Solutions architect content | [solutions-architect](../solutions-architect/README.md) |
| Multi-technology workflow | [cross-topic guides](../cross-topic-guides/README.md) |

## Ingestion workflow

1. Read every raw file selected for ingestion.
2. Identify the principal topic, provider, audience, and likely destination.
3. Search the repository for related content before creating a new page:

```bash
rg -n "topic|related-term" -g "*.md"
```

What it does: finds existing pages that may already cover the raw source.

1. Update the closest existing article when the raw source improves an existing page.
2. Create a new focused article only when the raw source is distinct enough to stand alone.
3. Use the closest template from [templates](../templates/README.md).
4. Convert rough notes into practical guidance with purpose, context, examples, decision points, risks, and related links.
5. Verify current product behavior against official documentation before adding technical claims.
6. Add or update parent indexes and related cross-links.
7. Update [GLOSSARY.md](../GLOSSARY.md) when important new terms appear.
8. Update [CHANGELOG.md](../CHANGELOG.md) for meaningful additions.
9. Move completed raw files to [processed](processed/README.md), preserving filenames unless a conflict requires a suffix.

## Quality rules

- Do not copy raw notes blindly; reorganize them into the repository writing standard.
- Do not keep unsupported claims from the raw source.
- Prefer one focused article over a broad mixed page.
- Keep command examples outside tables and explain them with `What it does:`.
- Add warnings near destructive, expensive, security-sensitive, or production-impacting actions.
- Preserve useful source links by moving them into `Related links` or an appropriate reference section.
- Leave unfinished or ambiguous raw files in [incoming](incoming/README.md) and document the blocker in the handoff.

## Validation

Run these checks before finishing an ingestion task:

```bash
git status --short --branch
npx markdownlint-cli2 "**/*.md"
```

What it does: confirms the branch state and validates Markdown formatting.

Check internal links with a repository-aware link checker or script before staging.

[Back to sources index](README.md) | [Back to root index](../README.md)
