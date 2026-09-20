---
okf_version: "0.2"
---

# Engineering knowledge base

This directory is the canonical Open Knowledge Format v0.2 bundle for this
repository. Start with a subject area, then follow its index to focused
concepts, procedures, references, and learning paths.

## Start by goal

| Goal | Start here | Outcome |
| --- | --- | --- |
| Learn practical platform basics locally | [Start here](start-here.md) | Use Git, Kubernetes, and Terraform without a cloud account. |
| Recover safely from a Git mistake | [Git undo and recovery](git/troubleshooting/undo-and-recovery.md) | Inspect first, then choose the least-destructive recovery action. |
| Diagnose a Kubernetes workload | [Kubernetes troubleshooting](kubernetes/troubleshooting/index.md) | Move from symptom to safe diagnostics and recovery. |
| Learn Terraform safely | [Terraform local state lifecycle](terraform/examples/local-state-lifecycle/local-state-lifecycle.md) | Practice plan, state, change review, and destroy locally. |
| Design a Crossplane platform API | [Crossplane component model](kubernetes/crossplane/component-model.md) | Understand providers, managed resources, XRDs, compositions, and XRs. |
| Plan backup or migration work | [Velero](migrations/velero/index.md) | Choose backup, restore, migration, and disaster-recovery guidance. |

## Reading and trust signals

- `draft` means useful material that still needs a completed review cycle.
- `stable` means the concept has current recorded sources and a freshness deadline.
- `deprecated` means do not use the concept for new work; follow its replacement link.
- Source records and review deadlines appear in concept frontmatter. AI tools can use the generated [knowledge catalog](../generated/README.md) to filter and route concepts without treating the catalog as a second source of truth.

## Engineering topics

- [Cloud](cloud/index.md) - Provider-neutral cloud guidance and AWS, Azure, Google Cloud, edge, and solution patterns.
- [Kubernetes](kubernetes/index.md) - Kubernetes concepts, operations, applications, Crossplane, and troubleshooting.
- [Git](git/index.md) - Version control, recovery, GitHub Actions, and delivery workflows.
- [Terraform](terraform/index.md) - Infrastructure as code, state, commands, examples, and maintenance.
- [Databases](databases/index.md) - Database modeling, Kafka, MongoDB, and platform choices.
- [Migrations](migrations/index.md) - Backup, restore, disaster recovery, and migration practices.
- [Security](security/index.md) - Identity federation and cross-platform security guidance.
- [FinOps](finops/index.md) - Cost visibility, allocation, and accountability.
- [DevOps](devops/index.md) - Delivery, automation, reliability, and code quality.
- [Programming languages](programming-languages/index.md) - Language behavior, tooling, and practical examples.

## AI and architecture

- [AI](ai/index.md) - AI systems, tooling, MCP, knowledge bases, and safe engineering use.
- [AI agents](ai-agents/index.md) - Agent workflows, evaluation, and operational safety.
- [LLM](llm/index.md) - Prompting, retrieval, evaluation, and operations.
- [ML](ml/index.md) and [MLOps](mlops/index.md) - Machine learning and operational practices.
- [Solutions architect](solutions-architect/index.md) - Design trade-offs, proofs of concept, and architecture reviews.
- [Cross-topic guides](cross-topic-guides/index.md) - End-to-end workflows across technologies.

## Learning and reference material

- [Start here](start-here.md) - A beginner-friendly local learning route.
- [Glossary](glossary.md) - Shared terminology.
- [Decision records](decision-records/index.md) - Recorded repository and architecture decisions.
- [Templates](templates/index.md) - Diátaxis-aligned documentation starters.
- [Assets](assets/index.md) - Guidance for diagrams, images, and icons.
- [Bundle log](log.md) - Notable changes to this knowledge bundle.
