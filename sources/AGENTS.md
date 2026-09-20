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
| `principal_topic` | `cloud`, `databases`, `kubernetes`, `git`, `terraform`, `migrations`, `security`, `finops`, `devops`, `programming-languages`, `mlops`, `ai`, `ai-agents`, `llm`, `ml`, `solutions-architect` |
| `provider` | `aws`, `azure`, `gcloud` for provider-specific cloud content |
| `target_section` | Relative path to the preferred destination section or article |

## Classification routes

| Raw topic | Destination |
| --- | --- |
| AWS-specific cloud content | [cloud/aws](../knowledge/cloud/aws/index.md) |
| Azure-specific cloud content | [cloud/azure](../knowledge/cloud/azure/index.md) |
| Google Cloud content | [cloud/gcloud](../knowledge/cloud/gcloud/index.md) |
| Provider-neutral cloud content | [cloud](../knowledge/cloud/index.md) |
| Database and data-platform content | [databases](../knowledge/databases/index.md) |
| Kubernetes content | [kubernetes](../knowledge/kubernetes/index.md) |
| Crossplane content | [kubernetes/crossplane](../knowledge/kubernetes/crossplane/index.md) |
| Git content | [git](../knowledge/git/index.md) |
| Terraform content | [terraform](../knowledge/terraform/index.md) |
| Migration, backup, restore, or disaster-recovery content | [migrations](../knowledge/migrations/index.md) |
| Security content | [security](../knowledge/security/index.md) |
| FinOps content | [finops](../knowledge/finops/index.md) |
| DevOps content | [devops](../knowledge/devops/index.md) |
| Programming language content | [programming-languages](../knowledge/programming-languages/index.md) |
| MLOps content | [mlops](../knowledge/mlops/index.md) |
| AI content | [ai](../knowledge/ai/index.md) |
| AI agent content | [ai-agents](../knowledge/ai-agents/index.md) |
| LLM content | [llm](../knowledge/llm/index.md) |
| ML content | [ml](../knowledge/ml/index.md) |
| Solutions architect content | [solutions-architect](../knowledge/solutions-architect/index.md) |
| Multi-technology workflow | [cross-topic guides](../knowledge/cross-topic-guides/index.md) |

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
3. Use the closest template from [templates](../knowledge/templates/index.md).
4. Convert rough notes into practical guidance with purpose, context, examples, decision points, risks, and related links.
5. Verify current product behavior against official documentation before adding technical claims.
6. Add or update parent indexes and related cross-links.
7. Update [GLOSSARY.md](../knowledge/glossary.md) when important new terms appear.
8. Update [CHANGELOG.md](../CHANGELOG.md) for meaningful additions.
9. Move completed raw files to [processed](processed/README.md), preserving filenames unless a conflict requires a suffix.
10. Add or update the processed source's row in the [ingestion register](processed/ingestion-register.md), linking every curated destination and recording verification status or `Unknown` where historical evidence is missing.

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
