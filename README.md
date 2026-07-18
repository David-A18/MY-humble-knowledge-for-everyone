# engineering-knowledge-base

A practical, long-term engineering knowledge base for cloud, Git, GitHub Actions, Terraform, Kubernetes, security, FinOps, DevOps, programming languages, MLOps, AI, LLMs, ML, solutions architecture, troubleshooting, and engineering best practices.

> [!NOTE]
> This repository is organized for fast navigation: start here, choose a major area, open a subcategory, then read a focused article or starter outline.

## Knowledge areas

| Area | Use it for |
| --- | --- |
| [Git](git/README.md) | Daily commands, repository hygiene, branching, recovery, and GitHub Actions. |
| [Terraform](terraform/README.md) | IaC fundamentals, state, module structure, commands, troubleshooting, and examples. |
| [Kubernetes](kubernetes/README.md) | Cluster objects, kubectl workflows, application tooling, troubleshooting, and operational practices. |
| [Cloud](cloud/README.md) | Provider-neutral cloud guidance and provider sections for AWS, Azure, and Google Cloud. |
| [AWS](cloud/aws/README.md) | AWS fundamentals, networking, compute, storage, security, FinOps, architecture, and certification notes. |
| [Databases](databases/README.md) | Database modeling, Kafka, MongoDB, operations, and cloud data-platform choices. |
| [Security](security/README.md) | Security guidance across cloud, identity, applications, supply chain, and operations. |
| [FinOps](finops/README.md) | Cost visibility, allocation, optimization, budgets, and financial accountability. |
| [DevOps](devops/README.md) | Delivery workflows, automation, reliability practices, and platform operations. |
| [Programming languages](programming-languages/README.md) | Language notes, tooling, runtime behavior, and practical examples. |
| [MLOps](mlops/README.md) | ML delivery, deployment, monitoring, governance, and operational practices. |
| [AI](ai/README.md) | AI concepts, workflows, systems, safety, and engineering use. |
| [AI agents](ai-agents/README.md) | Agent workflows, tool use, routing, evaluation, and operational safety. |
| [LLM](llm/README.md) | Large language model prompting, retrieval, evaluation, deployment, and operations. |
| [ML](ml/README.md) | Machine learning fundamentals, datasets, training, evaluation, and model risks. |
| [Solutions architect](solutions-architect/README.md) | Design trade-offs, architecture reviews, reliability, security, cost, and certification notes. |
| [Cross-topic guides](cross-topic-guides/README.md) | Practical workflows that combine multiple technologies. |
| [Decision records](decision-records/README.md) | Architecture and repository decisions with context and trade-offs. |

## Repository resources

| Resource | Purpose |
| --- | --- |
| [Sources](sources/README.md) | Raw Markdown intake area for topic notes before agent ingestion. |
| [Templates](templates/README.md) | Reusable Markdown templates for articles, commands, troubleshooting guides, ADRs, and examples. |
| [AI agent router](AGENTS.md) | Explicit routing and deployment workflow for AI agents improving the knowledge base. |
| [AI agent context](context.md) | Operating map for AI agents, including routes, editing rules, and validation expectations. |
| [AI documentation instructions](instructions.md) | Structure and readability standards for AI agents creating or refactoring documentation. |
| [Glossary](GLOSSARY.md) | Shared terms and acronyms used across the knowledge base. |
| [Roadmap](ROADMAP.md) | Planned expansion areas and prioritization. |
| [Contributing](CONTRIBUTING.md) | Writing standards, review checklist, and contribution flow. |
| [Changelog](CHANGELOG.md) | Notable repository changes. |

## Navigation pattern

Each documentation directory has a `README.md` index with links to its subcategories or articles. Focused articles include navigation links back to their parent index and the root index.

## Writing standards

- Use GitHub Flavored Markdown.
- Prefer focused articles over large catch-all pages.
- Keep tables small and place examples outside table cells with plain-language explanations below them.
- Include commands, expected outputs, failure symptoms, and decision sequences where useful.
- Use official documentation links when external references are needed.
- Mark early-stage pages with `Status: Initial outline` and enough structure to make future expansion clear.

## Official documentation shortcuts

- [Git documentation](https://git-scm.com/docs)
- [GitHub Actions documentation](https://docs.github.com/actions)
- [Terraform documentation](https://developer.hashicorp.com/terraform/docs)
- [Kubernetes documentation](https://kubernetes.io/docs/)
- [AWS documentation](https://docs.aws.amazon.com/)
- [Azure documentation](https://learn.microsoft.com/azure/)
- [Google Cloud documentation](https://cloud.google.com/docs)

## License

This repository is licensed under the [MIT License](LICENSE).
