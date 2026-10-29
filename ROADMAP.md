# Roadmap

This roadmap tracks the intended growth of `engineering-knowledge-base`.

## 2026-10-29 topic expansion

The [new learning paths](knowledge/index.md#expanded-learning-paths) now document all ten requested topic groups in the canonical OKF bundle. Local example checks, source provenance, and unexecuted runtime boundaries are recorded in the [publication audit](knowledge-base-audit.md).

| Follow-up | Completion evidence |
| --- | --- |
| Review draft concepts and assign ownership | A real maintainer, official sources, review scope, and a justified freshness deadline; keep drafts visible until then. |
| Istio/IRSA/kro/manifest labs | Disposable-environment runs recording actual versions, positive/negative behavior, and cleanup. |
| Collector/Pixie/Kafka deployment labs | Delivery/capture, outage/recovery, and persistent-state results on supported infrastructure. |
| RAG answer quality | A selected model digest, grounded/cited answers, paraphrases, conflicts, and insufficient-evidence results. |
| Dev Container/Ona runtime | Container startup/rebuild and, where access exists, hosted workflow evidence. |
| Weekly quality and freshness | Focused source reviews, full validators, reproducible catalog, and validated publication to `main`. |

These are follow-up evidence improvements, not claims that live cloud or reader testing occurred during authoring. Preserve the already-completed Git/Terraform/local-learning improvements when selecting further work.

## Current improvement sequence

Use the [knowledge-base improvement plan](knowledge-base-improvement-plan.md) to implement the findings in the [2026-09-18 review](knowledge-base-review.md). It provides task dependencies, affected files, validation instructions, and completion criteria.

The improvement plan has completed its documentation-scope work. The first local beginner route and Terraform exercise now exist and have author execution evidence. Crossplane AWS runtime validation and reader testing remain optional follow-up evidence rather than blockers for the knowledge base. Use the expansion ideas below as a backlog after those foundations; track implementation status in the plan rather than duplicating it here.

Use the [maintenance review queue](maintenance-review-queue.md) to schedule priority guide reviews and record optional validation follow-ups. The [Git-backed reading-site decision](knowledge/decision-records/adr-0005-git-backed-reading-site.md) now places reader-task testing after the first website launch; see the [website upgrade plan](knowledge-base-upgrade/features/knowledge-website/README.md) for its requirements and release sequence. Use the [knowledge-base upgrade hub](knowledge-base-upgrade/README.md) on `develop` for repository-level features, tools, skills, MCP server templates, and upgrade instructions.

Use the [knowledge content quality and expansion plan](knowledge-content-quality-expansion-plan.md)
to select and review new content. It defines the precision standard,
explanation model, evidence protocol, and reader- and AI-oriented measures for
this roadmap's work.

## Near term

- Expand Git command references and recovery procedures.
- Add Terraform state, module, provider, and workspace examples.
- Add Kubernetes troubleshooting guides for pods, services, ingress, DNS, storage, and scheduling.
- Add AWS networking and IAM practical guides.
- Add FinOps examples for cost allocation, tagging, budgets, and rightsizing.

## Medium term

- Add end-to-end deployment walkthroughs that combine GitHub Actions, Terraform, AWS, and Kubernetes.
- Add architecture decision examples for common cloud trade-offs.
- Add diagrams under [assets/diagrams](knowledge/assets/diagrams/index.md).
- Add command output examples and failure-mode screenshots where they improve comprehension.

## Long term

- Build a curated operating handbook for recurring production issues.
- Add opinionated checklists for design reviews, incident response, and platform readiness.
- Add reusable reference architectures for common AWS and Kubernetes workloads.

## Prioritization rules

1. Document recurring operational problems first.
2. Prefer high-signal commands, diagnostics, and decision criteria.
3. Keep pages small enough to maintain.
4. Update navigation immediately when adding new pages.
5. Use reader feedback and review evidence from the maintenance queue before starting broad restructuring work.
