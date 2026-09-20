# Roadmap

This roadmap tracks the intended growth of `engineering-knowledge-base`.

## Current improvement sequence

Use the [knowledge-base improvement plan](knowledge-base-improvement-plan.md) to implement the findings in the [2026-09-18 review](knowledge-base-review.md). It provides task dependencies, affected files, validation instructions, and completion criteria.

The improvement plan has completed its documentation-scope work. The first local beginner route and Terraform exercise now exist and have author execution evidence. Crossplane AWS runtime validation and reader testing remain optional follow-up evidence rather than blockers for the knowledge base. Use the expansion ideas below as a backlog after those foundations; track implementation status in the plan rather than duplicating it here.

Use the [maintenance review queue](maintenance-review-queue.md) to schedule priority guide reviews, record optional validation follow-ups, and run reader-task testing before making larger navigation or site-search decisions.

## Near term

- Expand Git command references and recovery procedures.
- Add Terraform state, module, provider, and workspace examples.
- Add Kubernetes troubleshooting guides for pods, services, ingress, DNS, storage, and scheduling.
- Add AWS networking and IAM practical guides.
- Add FinOps examples for cost allocation, tagging, budgets, and rightsizing.

## Medium term

- Add end-to-end deployment walkthroughs that combine GitHub Actions, Terraform, AWS, and Kubernetes.
- Add architecture decision examples for common cloud trade-offs.
- Add diagrams under [assets/diagrams](assets/diagrams/README.md).
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
