# Roadmap

This roadmap tracks the intended growth of `engineering-knowledge-base`.

## Current improvement sequence

Use the [knowledge-base improvement plan](knowledge-base-improvement-plan.md) to implement the findings in the [2026-09-18 review](knowledge-base-review.md). It provides task dependencies, affected files, validation instructions, and completion criteria.

Known defects and validation hardening have started in the plan. The first local beginner route and Terraform exercise now exist; Kubernetes execution remains blocked until Docker daemon access is available, and Crossplane AWS credential execution remains blocked until an authorized sandbox is available. Use the expansion ideas below as a backlog after those foundations; track implementation status in the plan rather than duplicating it here.

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
