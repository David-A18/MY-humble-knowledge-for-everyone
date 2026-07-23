# engineering-knowledge-base

A practical, long-term engineering knowledge base for cloud, Git, GitHub Actions, Terraform, Kubernetes, migrations, security, FinOps, DevOps, programming languages, MLOps, AI, LLMs, ML, solutions architecture, troubleshooting, and engineering best practices.

> [!NOTE]
> This repository is organized for fast navigation: start here, choose a major area, open a subcategory, then read a focused article or starter outline.

## Knowledge areas

| Principal area | Current subtopics | Use it for |
| --- | --- | --- |
| [Cloud](cloud/README.md) | [AWS](cloud/aws/README.md), [Azure](cloud/azure/README.md), [Google Cloud](cloud/gcloud/README.md), [edge and CDN](cloud/edge/README.md) | Provider-neutral cloud guidance plus provider-specific architecture, networking, security, operations, and cost notes. |
| [Kubernetes](kubernetes/README.md) | [Core objects](kubernetes/core-objects/README.md), [commands](kubernetes/commands/README.md), [Crossplane](kubernetes/crossplane/README.md), [applications and tools](kubernetes/applications-and-tools/README.md), [best practices](kubernetes/best-practices/README.md), [troubleshooting](kubernetes/troubleshooting/README.md) | Cluster objects, `kubectl` workflows, Kubernetes-native control planes, application tooling, troubleshooting, and operational practices. |
| [Git](git/README.md) | [Commands](git/commands/README.md), [GitHub Actions](git/github-actions/README.md) | Daily commands, repository hygiene, branching, recovery, automation, workflow security, and CI/CD examples. |
| [Terraform](terraform/README.md) | [Commands](terraform/commands/README.md), [examples](terraform/examples/README.md), [best practices](terraform/best-practices/README.md), [troubleshooting](terraform/troubleshooting/README.md) | IaC fundamentals, state, module structure, command workflows, troubleshooting, and reusable examples. |
| [Databases](databases/README.md) | [Kafka](databases/kafka/README.md), [MongoDB](databases/mongodb/README.md), [relational vs document databases](databases/relational-vs-document-databases.md) | Database modeling, event streaming, document databases, operations, and cloud data-platform choices. |
| [Migrations](migrations/README.md) | [Velero](migrations/velero/README.md) | Infrastructure, platform, workload, Kubernetes backup, restore, disaster recovery, and migration guidance. |
| [Security](security/README.md) | [Identity federation](security/identity-federation/README.md) | Security guidance across cloud, identity, applications, supply chain, and operations. |
| [FinOps](finops/README.md) | Cost allocation, budgets, optimization, accountability | Cost visibility, allocation, optimization, budgets, and financial accountability. |
| [DevOps](devops/README.md) | Delivery workflows, automation, reliability, platform operations | Delivery workflows, automation, reliability practices, and platform operations. |
| [Programming languages](programming-languages/README.md) | Language notes, tooling, runtimes, practical examples | Language behavior, tooling, runtime notes, and examples. |
| [AI](ai/README.md) | AI systems, workflows, safety, engineering use | AI concepts, workflows, systems, safety, and engineering use. |
| [AI agents](ai-agents/README.md) | Agent workflows, tool use, routing, evaluation, operational safety | Agent design, routing, knowledge-base improvement workflows, and operational safety. |
| [LLM](llm/README.md) | Prompting, retrieval, evaluation, deployment, operations | Large language model prompting, retrieval, evaluation, deployment, and operations. |
| [ML](ml/README.md) | Datasets, training, evaluation, model risks | Machine learning fundamentals, datasets, training, evaluation, and model risks. |
| [MLOps](mlops/README.md) | Delivery, deployment, monitoring, governance, operations | ML delivery, deployment, monitoring, governance, and operational practices. |
| [Solutions architect](solutions-architect/README.md) | Design trade-offs, architecture reviews, reliability, security, cost | Architecture decisions, design reviews, reliability, security, cost, and certification notes. |
| [Cross-topic guides](cross-topic-guides/README.md) | EKS, AWS, Terraform, GitOps, OIDC, APISIX, CloudFront, MSK, Crossplane | Practical workflows that combine multiple technologies. |
| [Decision records](decision-records/README.md) | Repository and architecture decisions | Architecture and repository decisions with context and trade-offs. |

## Fast topic paths

Use these shortcuts when you already know the topic name and do not want to browse through the full area hierarchy.

| Topic | Start here | Then read |
| --- | --- | --- |
| APISIX on Kubernetes or EKS | [Apache APISIX](kubernetes/applications-and-tools/apache-apisix.md) | [Architecture and deployment](kubernetes/applications-and-tools/apisix-architecture-and-deployment.md), [security and observability](kubernetes/applications-and-tools/apisix-security-traffic-and-observability.md), [APISIX on EKS](cross-topic-guides/apisix-on-eks.md), [APISIX troubleshooting](kubernetes/troubleshooting/apisix.md). |
| Flux and GitOps | [Flux](kubernetes/applications-and-tools/flux.md) | [Flux reconciliation and Helm releases](kubernetes/applications-and-tools/flux-reconciliation-and-helm.md), [GitOps security and multi-tenancy](kubernetes/applications-and-tools/gitops-security-and-multitenancy.md), [GitOps on EKS](cross-topic-guides/gitops-on-eks.md). |
| Akamai, CloudFront, and CDN edge | [Akamai vs. CloudFront](cloud/edge/akamai-vs-cloudfront.md) | [CDN fundamentals](cloud/edge/cdn-and-edge-fundamentals.md), [caching and origin protection](cloud/edge/cdn-caching-and-origin-protection.md), [multi-CDN operations](cloud/edge/multi-cdn-operations.md), [CDN in front of EKS](cross-topic-guides/cdn-in-front-of-eks.md). |
| Velero Kubernetes migration and recovery | [Velero](migrations/velero/README.md) | [Storage and volume backups](migrations/velero/storage-and-volume-backups.md), [AWS S3 and EBS installation](migrations/velero/aws-s3-ebs-installation.md), [cluster migration and disaster recovery](migrations/velero/cluster-migration-and-disaster-recovery.md). |

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
