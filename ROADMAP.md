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

## Prioritized content backlog

This replaces the old broad bullets after checking the current articles and indexes. Reviewed documentation and executed infrastructure are distinct completion states. The [section ledger](section-quality-progress.md) tracks full section reviews; these entries identify concrete remaining deliverables.

| Priority / state | Existing coverage | Remaining task and completion criterion |
| --- | --- | --- |
| P1 / partial | [AWS networking](knowledge/cloud/aws/networking/index.md): security groups, CloudFront, stateful controls | Add VPC/subnet/route/NAT/endpoint learning sequence with path diagnostics, costs, and cleanup; review the existing three concepts. |
| P1 / partial | [Terraform fundamentals/state](knowledge/terraform/fundamentals/index.md), [core workflow](knowledge/terraform/commands/core-workflow.md), and [executed local lab](knowledge/terraform/examples/local-state-lifecycle/local-state-lifecycle.md) | Add focused modules, provider selection/aliases, workspace isolation, and remote-backend operations. Completion requires linked examples, failure boundaries, and honest execution evidence, not repeated introductory summaries. |
| P1 / partial | [FinOps allocation](knowledge/finops/cost-allocation-basics.md) and [AWS tagging](knowledge/cloud/aws/finops/cost-allocation-tags.md) | Add budgets/anomaly response, measured rightsizing, and reporting examples with ownership, decision criteria, and verification. |
| P1 / documentation complete; runtime open | [Kubernetes troubleshooting](knowledge/kubernetes/troubleshooting/index.md) | Eleven focused guides cover the requested diagnostic areas. Next evidence: disposable failure/recovery drills, actual versions, and redacted expected outputs. |
| P2 / documentation complete; broader drills open | [Git undo/recovery](knowledge/git/troubleshooting/undo-and-recovery.md) | Preserve the source-reviewed and locally exercised guide. Add submodule/corruption/shared-history edge cases only as separate bounded recovery drills. |
| P2 / partial | [AWS identity/security](knowledge/cloud/aws/security/index.md), [EKS workload comparison](knowledge/cross-topic-guides/eks-workload-identity.md) | Validate existing trust/permissions paths; add a general least-privilege IAM exercise with positive/negative evidence and cleanup. |
| P2 / partial | [Cross-topic guides](knowledge/cross-topic-guides/index.md), including local, EKS, GitOps, and observability routes | Connect one GitHub Actions → Terraform → AWS → Kubernetes deployment journey with pinned inputs, rollback ownership, and recorded sandbox results. Reuse the existing focused guides. |
| P2 / partial | [Decision records](knowledge/decision-records/index.md) and [diagram assets](knowledge/assets/diagrams/index.md) | Add a cloud trade-off decision and diagram only where it resolves a concrete reader choice; document consequences and reconsideration criteria. |
| P2 / partial | [New topic series](knowledge/index.md#expanded-learning-paths) | Complete the runtime acceptance evidence listed above; retain draft labels where ownership/runtime review is missing. |
| P3 / planned | [Operational troubleshooting](knowledge/kubernetes/troubleshooting/index.md) and [best practices](knowledge/kubernetes/best-practices/index.md) | Assemble an incident handbook with escalation, evidence capture, and readiness checklists after validating the component runbooks. |
| P3 / planned | Existing [AWS and Kubernetes guides](knowledge/cross-topic-guides/index.md) | Add one reusable reference architecture with requirements, threat/failure model, costs, manifests, cleanup, and bounded execution evidence. |

Command-output captures and screenshots are supporting tasks for the selected guide, not a separate repository-wide rewrite. Keep unrelated improvements queued.

## Prioritization rules

1. Document recurring operational problems first.
2. Prefer high-signal commands, diagnostics, and decision criteria.
3. Keep pages small enough to maintain.
4. Update navigation immediately when adding new pages.
5. Use reader feedback and review evidence from the maintenance queue before starting broad restructuring work.
