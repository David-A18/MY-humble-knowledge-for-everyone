# engineering-knowledge-base

A practical, long-term engineering knowledge base for cloud, Git, GitHub Actions, Terraform, Kubernetes, migrations, security, FinOps, DevOps, programming languages, MLOps, AI, LLMs, ML, solutions architecture, troubleshooting, and engineering best practices.

> [!NOTE]
> This repository is organized for fast navigation: start here, choose a major area, open a subcategory, then read a focused article or starter outline.

Coverage labels:

- **Developed:** contains multiple focused guides or operational procedures.
- **Partial:** contains useful material but is still missing a complete beginner path or important subareas.
- **Outline:** marks planned coverage or an early index with limited supporting articles.

## Knowledge areas

| Principal area | Coverage | Current subtopics | Use it for |
| --- | --- | --- |
| [Cloud](cloud/README.md) | Partial | [Cloud solutions](cloud/solutions/README.md), [AWS](cloud/aws/README.md), [Azure](cloud/azure/README.md), [Google Cloud](cloud/gcloud/README.md), [edge and CDN](cloud/edge/README.md) | Provider-neutral cloud guidance plus provider-specific architecture, networking, security, API management, operations, and cost notes. |
| [Kubernetes](kubernetes/README.md) | Developed | [Core objects](kubernetes/core-objects/README.md), [commands](kubernetes/commands/README.md), [Crossplane](kubernetes/crossplane/README.md), [applications and tools](kubernetes/applications-and-tools/README.md), [best practices](kubernetes/best-practices/README.md), [troubleshooting](kubernetes/troubleshooting/README.md) | Cluster objects, `kubectl` workflows, Kubernetes-native control planes, application tooling, troubleshooting, and operational practices. |
| [Git](git/README.md) | Developed | [Commands](git/commands/README.md), [GitHub Actions](git/github-actions/README.md) | Daily commands, repository hygiene, branching, recovery, automation, workflow security, and CI/CD examples. |
| [Terraform](terraform/README.md) | Partial | [Commands](terraform/commands/README.md), [examples](terraform/examples/README.md), [best practices](terraform/best-practices/README.md), [troubleshooting](terraform/troubleshooting/README.md) | IaC fundamentals, state, module structure, command workflows, troubleshooting, and reusable examples. |
| [Databases](databases/README.md) | Developed | [Kafka](databases/kafka/README.md), [MongoDB](databases/mongodb/README.md), [relational vs document databases](databases/relational-vs-document-databases.md) | Database modeling, event streaming, document databases, operations, and cloud data-platform choices. |
| [Migrations](migrations/README.md) | Developed | [Velero](migrations/velero/README.md) | Infrastructure, platform, workload, Kubernetes backup, restore, disaster recovery, and migration guidance. |
| [Security](security/README.md) | Partial | [Identity federation](security/identity-federation/README.md) | Security guidance across cloud, identity, applications, supply chain, and operations. |
| [FinOps](finops/README.md) | Outline | Cost allocation, budgets, optimization, accountability | Cost visibility, allocation, optimization, budgets, and financial accountability. |
| [DevOps](devops/README.md) | Partial | [Code quality](devops/code-quality/README.md), delivery workflows, automation, reliability, platform operations | Delivery workflows, automation, static analysis, reliability practices, and platform operations. |
| [Programming languages](programming-languages/README.md) | Outline | Language notes, tooling, runtimes, practical examples | Language behavior, tooling, runtime notes, and examples. |
| [AI](ai/README.md) | Developed | [AI tooling](ai/ai-tooling/README.md), [agent knowledge bases](ai/ai-tooling/knowledge-bases/README.md), AI systems, MCP, custom tools, knowledge-base patterns, safety, engineering use | AI concepts, workflows, tool integrations, Markdown knowledge bases, systems, safety, and engineering use. |
| [AI agents](ai-agents/README.md) | Outline | Agent workflows, tool use, routing, evaluation, operational safety | Agent design, routing, knowledge-base improvement workflows, and operational safety. |
| [LLM](llm/README.md) | Outline | Prompting, retrieval, evaluation, deployment, operations | Large language model prompting, retrieval, evaluation, deployment, and operations. |
| [ML](ml/README.md) | Outline | Datasets, training, evaluation, model risks | Machine learning fundamentals, datasets, training, evaluation, and model risks. |
| [MLOps](mlops/README.md) | Outline | Delivery, deployment, monitoring, governance, operations | ML delivery, deployment, monitoring, governance, and operational practices. |
| [Solutions architect](solutions-architect/README.md) | Partial | Design trade-offs, architecture reviews, reliability, security, cost | Architecture decisions, design reviews, reliability, security, cost, and certification notes. |
| [Cross-topic guides](cross-topic-guides/README.md) | Partial | EKS, AWS, Terraform, GitOps, OIDC, APISIX, CloudFront, MSK, Crossplane | Practical workflows that combine multiple technologies. |
| [Decision records](decision-records/README.md) | Partial | Repository and architecture decisions | Architecture and repository decisions with context and trade-offs. |

## Fast topic paths

Use these shortcuts when you already know the topic name and do not want to browse through the full area hierarchy.

| Topic | Start here | Then read |
| --- | --- | --- |
| Apigee API management | [Apigee API management](cloud/gcloud/apigee.md) | API proxies, policies, API products, developer apps, environments, hybrid runtime placement, automation, and troubleshooting. |
| APISIX on Kubernetes or EKS | [Apache APISIX](kubernetes/applications-and-tools/apache-apisix.md) | [Architecture and deployment](kubernetes/applications-and-tools/apisix-architecture-and-deployment.md), [security and observability](kubernetes/applications-and-tools/apisix-security-traffic-and-observability.md), [APISIX on EKS](cross-topic-guides/apisix-on-eks.md), [APISIX troubleshooting](kubernetes/troubleshooting/apisix.md). |
| Crossplane platform APIs | [Crossplane](kubernetes/crossplane/README.md) | [XRDs, Compositions, and XR calls](kubernetes/crossplane/xrd-composition-and-xr-calls.md), [Component model](kubernetes/crossplane/component-model.md), [Compositions](kubernetes/crossplane/compositions.md), [Terraform vs Crossplane](kubernetes/crossplane/terraform-vs-crossplane.md), [AWS VPC platform API](kubernetes/crossplane/aws-vpc-platform-api.md), [deployment patterns](kubernetes/crossplane/deployment-patterns-and-references.md), [Crossplane on AWS](cross-topic-guides/crossplane-on-aws.md). |
| Flux and GitOps | [Flux](kubernetes/applications-and-tools/flux.md) | [Flux reconciliation and Helm releases](kubernetes/applications-and-tools/flux-reconciliation-and-helm.md), [GitOps security and multi-tenancy](kubernetes/applications-and-tools/gitops-security-and-multitenancy.md), [GitOps on EKS](cross-topic-guides/gitops-on-eks.md). |
| K9s Kubernetes terminal UI | [K9s](kubernetes/applications-and-tools/k9s.md) | Navigate views, inspect Pods, read logs, filter resources, use aliases and hotkeys, and run safely in read-only mode. |
| Kafka event streaming | [Kafka](databases/kafka/README.md) | [Fundamentals](databases/kafka/fundamentals.md), [topic and event design](databases/kafka/topic-and-event-design.md), [consumer lag and replay](databases/kafka/consumer-groups-lag-and-replay.md), [delivery guarantees](databases/kafka/delivery-guarantees-and-failure-handling.md), [operations](databases/kafka/operations.md), [Amazon MSK](cloud/aws/databases/amazon-msk.md). |
| SonarQube code quality | [SonarQube](devops/code-quality/sonarqube.md) | [SonarQube GitHub integration](devops/code-quality/sonarqube-github-integration.md), [GitHub Actions](git/github-actions/README.md). |
| Akamai, CloudFront, and CDN edge | [Akamai vs. CloudFront](cloud/edge/akamai-vs-cloudfront.md) | [CDN fundamentals](cloud/edge/cdn-and-edge-fundamentals.md), [caching and origin protection](cloud/edge/cdn-caching-and-origin-protection.md), [multi-CDN operations](cloud/edge/multi-cdn-operations.md), [CDN in front of EKS](cross-topic-guides/cdn-in-front-of-eks.md). |
| Blue-green deployment | [Blue-green deployment](cloud/solutions/blue-green-deployment.md) | [End-to-end deployment](cross-topic-guides/end-to-end-deployment.md), [GitHub Actions with Kubernetes](cross-topic-guides/github-actions-with-kubernetes.md). |
| Velero Kubernetes migration and recovery | [Velero](migrations/velero/README.md) | [Storage and volume backups](migrations/velero/storage-and-volume-backups.md), [backup and restore workflows](migrations/velero/backup-restore-workflows.md), [possible integrations](migrations/velero/possible-integrations.md), [real use cases and runbooks](migrations/velero/real-use-cases-and-runbooks.md). |

## Repository resources

| Resource | Purpose |
| --- | --- |
| [Sources](sources/README.md) | Raw Markdown intake area for topic notes before agent ingestion. |
| [Start here](start-here.md) | First local learning route for Git, Kubernetes, troubleshooting, cleanup, and Terraform basics. |
| [Templates](templates/README.md) | Reusable Markdown templates for articles, commands, troubleshooting guides, ADRs, and examples. |
| [AI agent router](AGENTS.md) | Explicit routing and deployment workflow for AI agents improving the knowledge base. |
| [AI agent context](context.md) | Operating map for AI agents, including routes, editing rules, and validation expectations. |
| [AI documentation instructions](instructions.md) | Structure and readability standards for AI agents creating or refactoring documentation. |
| [Glossary](GLOSSARY.md) | Shared terms and acronyms used across the knowledge base. |
| [Roadmap](ROADMAP.md) | Planned expansion areas and prioritization. |
| [Knowledge-base review](knowledge-base-review.md) | Repository assessment, evidence, and prioritized improvements reviewed on 2026-09-18. |
| [Knowledge-base improvement plan](knowledge-base-improvement-plan.md) | Ordered work packages, contributor instructions, acceptance criteria, and maintenance measures based on the review. |
| [Maintenance review queue](maintenance-review-queue.md) | Priority guide review queue, reader-task testing protocol, and blocked validation follow-ups. |
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
- [Crossplane documentation](https://docs.crossplane.io/latest/)
- [Kubernetes documentation](https://kubernetes.io/docs/)
- [AWS documentation](https://docs.aws.amazon.com/)
- [Azure documentation](https://learn.microsoft.com/azure/)
- [Google Cloud documentation](https://cloud.google.com/docs)

## License

This repository is licensed under the [MIT License](LICENSE).
