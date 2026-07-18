# AI agent router

Use this file as the first routing guide for AI agents improving this knowledge base. It turns the repository links into an execution path: find the right area, choose the right template, update the right indexes, validate the result, and leave the repository ready for the next agent or human.

> [!IMPORTANT]
> Before changing documentation, read [context.md](context.md), [instructions.md](instructions.md), and [CONTRIBUTING.md](CONTRIBUTING.md). They define the repository map, writing standard, and contribution expectations.

## Operating contract

- Improve navigation, accuracy, maintainability, or practical usefulness.
- Keep changes scoped to the requested topic or the smallest coherent documentation improvement.
- Use lowercase kebab-case for documentation files and directories.
- Use relative links for all internal repository links.
- Prefer official external documentation for product behavior, command references, service limits, and security guidance.
- Never add secrets, customer-specific data, private infrastructure details, or unverified claims.
- Update indexes, route maps, glossary entries, and changelog notes when the change affects them.
- Validate before finishing, then commit and push only when the task, repository instructions, branch state, and credentials allow it.

## First-read sequence

1. [README.md](README.md): human-facing entry point and top-level navigation.
2. [context.md](context.md): complete AI operating map and route table.
3. [instructions.md](instructions.md): Markdown structure, examples, risk notes, and validation standard.
4. [CONTRIBUTING.md](CONTRIBUTING.md): contributor checklist and review expectations.
5. [ROADMAP.md](ROADMAP.md): priority areas for useful expansion.
6. [GLOSSARY.md](GLOSSARY.md): shared terms and acronyms.
7. [CHANGELOG.md](CHANGELOG.md): notable changes that need an `Unreleased` entry.
8. [templates/README.md](templates/README.md): reusable page structures.
9. [sources/README.md](sources/README.md): raw Markdown intake area for unprocessed notes.

## Route by request

| User need | Start here | Add or edit here | Also update |
| --- | --- | --- | --- |
| Top-level navigation, major areas, repository entry text | [README.md](README.md) | Root-level files | [context.md](context.md), [CHANGELOG.md](CHANGELOG.md) |
| AI operating rules or routing | [AGENTS.md](AGENTS.md) and [context.md](context.md) | Root-level agent guides | [README.md](README.md), [CHANGELOG.md](CHANGELOG.md) |
| Writing format, examples, tables, risk notes | [instructions.md](instructions.md) | [instructions.md](instructions.md), [templates](templates/README.md) | [context.md](context.md), [CHANGELOG.md](CHANGELOG.md) |
| Contribution or review process | [CONTRIBUTING.md](CONTRIBUTING.md) | [CONTRIBUTING.md](CONTRIBUTING.md), [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) | [context.md](context.md), [CHANGELOG.md](CHANGELOG.md) |
| Planned work or priorities | [ROADMAP.md](ROADMAP.md) | [ROADMAP.md](ROADMAP.md) | [README.md](README.md) if navigation changes |
| Shared terms or acronyms | [GLOSSARY.md](GLOSSARY.md) | [GLOSSARY.md](GLOSSARY.md) | Related articles that use the term |
| Architecture or repository decisions | [decision-records/README.md](decision-records/README.md) | New ADR from [ADR template](templates/architecture-decision-record-template.md) | [decision-records/README.md](decision-records/README.md), [CHANGELOG.md](CHANGELOG.md) |
| Visual references | [assets/README.md](assets/README.md) | [assets/diagrams](assets/diagrams/README.md), [assets/images](assets/images/README.md), [assets/icons](assets/icons/README.md) | Article that uses the asset |
| Raw Markdown topic notes | [sources/README.md](sources/README.md) | [sources/incoming](sources/incoming/README.md), then the classified destination route | [sources/processed](sources/processed/README.md), destination indexes, [CHANGELOG.md](CHANGELOG.md) |

## Route by knowledge area

| Area | Start here | Use it for |
| --- | --- | --- |
| [Git](git/README.md) | [git/README.md](git/README.md) | Git concepts, commands, recovery, troubleshooting, tricks, and best practices. |
| [Git commands](git/commands/README.md) | [git/commands/README.md](git/commands/README.md) | Daily commands, use cases, issue solving, diagnostics, advanced workflows, and command catalogs. |
| [GitHub Actions](git/github-actions/README.md) | [git/github-actions/README.md](git/github-actions/README.md) | Workflow syntax, commands, `uses:` actions, examples, common failures, security, secrets, OIDC, and permissions. |
| [Terraform](terraform/README.md) | [terraform/README.md](terraform/README.md) | Terraform fundamentals, state, command workflow, language, project structure, troubleshooting, best practices, and examples. |
| [Kubernetes](kubernetes/README.md) | [kubernetes/README.md](kubernetes/README.md) | Kubernetes concepts, objects, `kubectl`, operational workflows, troubleshooting, best practices, tricks, and examples. |
| [Kubernetes commands](kubernetes/commands/README.md) | [kubernetes/commands/README.md](kubernetes/commands/README.md) | Daily `kubectl`, common commands, advanced commands, operational sequences, `eksctl`, and basics. |
| [Cloud](cloud/README.md) | [cloud/README.md](cloud/README.md) | Provider-neutral cloud guidance and provider sections for AWS, Azure, and Google Cloud. |
| [AWS](cloud/aws/README.md) | [cloud/aws/README.md](cloud/aws/README.md) | AWS fundamentals, networking, compute, storage, databases, security, governance, FinOps, architecture, and troubleshooting. |
| [Security](security/README.md) | [security/README.md](security/README.md) | Security across cloud, identity, applications, supply chain, and operations. |
| [FinOps](finops/README.md) | [finops/README.md](finops/README.md) | Cost visibility, allocation, optimization, budgets, and accountability. |
| [DevOps](devops/README.md) | [devops/README.md](devops/README.md) | Delivery workflows, automation, reliability practices, and platform operations. |
| [Programming languages](programming-languages/README.md) | [programming-languages/README.md](programming-languages/README.md) | Language notes, tooling, runtime behavior, and practical examples. |
| [MLOps](mlops/README.md) | [mlops/README.md](mlops/README.md) | ML delivery, deployment, monitoring, governance, and operations. |
| [AI](ai/README.md) | [ai/README.md](ai/README.md) | AI concepts, workflows, systems, safety, and engineering use. |
| [AI agents](ai-agents/README.md) | [ai-agents/README.md](ai-agents/README.md) | Agent workflows, tool use, routing, evaluation, and operational safety. |
| [LLM](llm/README.md) | [llm/README.md](llm/README.md) | Large language model prompting, retrieval, evaluation, deployment, and operations. |
| [ML](ml/README.md) | [ml/README.md](ml/README.md) | Machine learning fundamentals, datasets, training, evaluation, and model risks. |
| [Solutions architect](solutions-architect/README.md) | [solutions-architect/README.md](solutions-architect/README.md) | Design trade-offs, architecture reviews, reliability, security, cost, and certification notes. |
| [Cross-topic guides](cross-topic-guides/README.md) | [cross-topic-guides/README.md](cross-topic-guides/README.md) | Workflows that combine GitHub Actions, Terraform, Kubernetes, AWS, EKS, deployment, and observability. |

## Route by article type

| Article type | Template | Required shape |
| --- | --- | --- |
| Concept or procedure | [Knowledge article](templates/knowledge-article-template.md) | Purpose, when to use it, prerequisites, key ideas, procedure, troubleshooting, related links. |
| Command reference | [Command reference](templates/command-reference-template.md) | Short task tables, command examples outside tables, expected output where useful, risk notes near risky commands. |
| Troubleshooting guide | [Troubleshooting](templates/troubleshooting-template.md) | Symptoms, first checks, decision sequence, diagnostics, safe recovery, prevention. |
| Architecture decision | [Architecture decision record](templates/architecture-decision-record-template.md) | Context, decision, consequences, related links. |
| Hands-on walkthrough | [Practical example](templates/practical-example-template.md) | Goal, prerequisites, files, steps, validation, cleanup, related links. |

## Improvement workflow

1. Understand the requested outcome and identify the closest existing page with `rg -n "term|related-term" -g "*.md"`.
2. Read the parent index and nearby related articles before editing.
3. Decide whether to update an existing page, add a focused article, add a cross-topic guide, or update a template/standard.
4. If adding a page, copy the nearest template structure and name the file in lowercase kebab-case.
5. Add practical substance: purpose, decision criteria, commands, expected outputs, failure symptoms, safety notes, and official references where relevant.
6. Add links from the parent `README.md`, the major area index when appropriate, and related articles that readers would naturally traverse.
7. Add bottom navigation links back to the parent index, major area index when different, and root index.
8. Update [GLOSSARY.md](GLOSSARY.md) for important new terms.
9. Update [context.md](context.md) when routes, conventions, directories, templates, or validation behavior change.
10. Update [CHANGELOG.md](CHANGELOG.md) for meaningful content, structure, navigation, or workflow additions.

## Raw source ingestion

Use [sources/AGENTS.md](sources/AGENTS.md) when converting raw `.md` notes from [sources/incoming](sources/incoming/README.md).

- Classify each source by `principal_topic`, `provider`, and `target_section` when metadata is present.
- Infer missing metadata from the raw content and verify the destination against existing indexes.
- Route AWS, Azure, and Google Cloud material through [cloud](cloud/README.md).
- Route multi-technology workflows to [cross-topic guides](cross-topic-guides/README.md).
- Move successfully ingested raw files to [sources/processed](sources/processed/README.md).

## How to make information better

- Replace broad placeholders with operational details: exact checks, commands, examples, decision sequences, and failure modes.
- Split large mixed topics into focused articles when a reader would search for them separately.
- Convert long prose lists into small tables only when scanning becomes easier.
- Keep examples outside tables and explain each with `What it does:`.
- Put `[!WARNING]`, `[!IMPORTANT]`, `[!TIP]`, or `[!NOTE]` close to the command or decision they affect.
- Cross-link related material instead of duplicating whole sections.
- For current product behavior, verify against official documentation before changing technical claims.
- Preserve existing page purpose; move unrelated additions to a better route.

## Link rules

- Internal links must be relative and must resolve locally.
- Focused articles should end with `Related links`.
- Parent indexes must link to every focused article in their directory.
- Major area indexes should link to subcategory indexes and important cross-topic routes.
- Cross-topic guides should link back to every major area they combine, such as [Cloud](cloud/README.md), [AWS](cloud/aws/README.md), [Kubernetes](kubernetes/README.md), [Terraform](terraform/README.md), or [GitHub Actions](git/github-actions/README.md).
- Do not leave placeholder links, empty anchors, or links to files that do not exist.

## Validation and deployment workflow

Run these checks before finishing:

```bash
git status --short --branch
npx markdownlint-cli2 "**/*.md"
```

If Node tooling is unavailable, still inspect the Markdown manually and report the missing tool.

Check internal links with a repository-aware script or link checker. A simple search-based preflight is:

```bash
rg -n "\[[^\]]+\]\([^)]+\)" -g "*.md"
```

Deployment for this repository means landing a validated documentation change in the correct files, with indexes and metadata updated. After validation, commit and push only when credentials, branch policy, and the user request allow it. Never stage unrelated work, never force-push unless explicitly requested, and report blockers plainly.

## Final handoff checklist

- [ ] The changed content is in the correct route.
- [ ] The nearest parent index links to new or moved pages.
- [ ] Related pages link to the new content when it helps navigation.
- [ ] New concepts are reflected in [GLOSSARY.md](GLOSSARY.md) when useful.
- [ ] [CHANGELOG.md](CHANGELOG.md) records meaningful additions.
- [ ] [context.md](context.md) is updated for route or convention changes.
- [ ] Markdown examples use fenced code blocks with language identifiers.
- [ ] Risky commands or infrastructure changes include nearby warnings.
- [ ] Internal links are relative and verified.
- [ ] `git status --short --branch` shows only intended changes before staging.

[Back to root index](README.md)
