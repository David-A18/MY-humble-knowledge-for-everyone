---
okf_version: "0.2"
---

# Engineering knowledge base

This directory is the canonical Open Knowledge Format v0.2 bundle for this
repository. Start with a subject area, then follow its index to focused
concepts, procedures, references, and learning paths.

## Expanded learning paths

| Learning path | Outcome |
| --- | --- |
| [Istio authentication and authorization](kubernetes/applications-and-tools/istio/index.md) | Workload identities, mTLS, JWTs, sidecar/ambient policy, and access tests. |
| [Kubernetes platform tooling](kubernetes/applications-and-tools/platform-tooling/index.md) | Secrets, certificates, storage, DNS, policy, scaling, and tool selection. |
| [Manifest validation and regressions](kubernetes/applications-and-tools/manifest-validation/index.md) | Semantic YAML differences, live drift, schemas, policy, and behavior tests. |
| [IRSA](cloud/aws/security/irsa-fundamentals.md) | EKS credential flow, IAM trust, least privilege, and S3 access tests. |
| [kro](kubernetes/applications-and-tools/kro/index.md) | Resource graphs, CEL, generated APIs, and lifecycle. |
| [Observability, eBPF, and Pixie](kubernetes/observability/index.md) | Signals, kernel visibility, telemetry collection, and debugging. |
| [AWS CDK v2](cloud/aws/cdk/index.md) | Equivalent TypeScript/Python labs, assertions, synthesis, and deployment. |
| [Data aggregation](databases/data-aggregation.md) | Windows, deduplication, late events, durable state, and Kafka. |
| [RAG](llm/rag/index.md) | Retrieval, citations, grounded generation, evaluation, and a Python lab. |
| [Ona and Gitpod](devops/development-environments/index.md) | Current product availability, reproducible environments, and migration. |

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
- [Programming languages](programming-languages/index.md) - Selective language and bootstrapping notes, not a complete language curriculum.

## AI and architecture

- [AI](ai/index.md) - AI systems, tooling, MCP, knowledge bases, and safe engineering use.
- [AI agents](ai-agents/index.md) - Planned coverage for agent workflows, evaluation, and operational safety; use AI tooling for current agent knowledge-base guidance.
- [LLM](llm/index.md) - Planned LLM route; current retrieval and evaluation material lives in AI tooling.
- [ML](ml/index.md) and [MLOps](mlops/index.md) - Planned topic maps, not yet a complete learning curriculum.
- [Solutions architect](solutions-architect/index.md) - Design trade-offs, proofs of concept, and architecture reviews.
- [Cross-topic guides](cross-topic-guides/index.md) - End-to-end workflows across technologies.

## Learning and reference material

- [Start here](start-here.md) - A beginner-friendly local learning route.
- [Glossary](glossary.md) - Shared terminology.
- [Decision records](decision-records/index.md) - Recorded repository and architecture decisions.
- [Templates](templates/index.md) - Diátaxis-aligned documentation starters.
- [Assets](assets/index.md) - Guidance for diagrams, images, and icons.
- [Bundle log](log.md) - Notable changes to this knowledge bundle.
