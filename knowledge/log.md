# Knowledge bundle log

## 2026-09-30

- **Teaching-hub second wave**: Rewrote six explanations to the teaching standard with plain definitions, analogies with stated limits, bounded illustrative examples, diagrams with text alternatives, understanding checks, and keyed official-source citations: relational vs. document databases, MongoDB fundamentals, Kafka topic and event design, custom resources and CRDs, OIDC fundamentals, and CDN and edge fundamentals. All six remain drafts with no review, execution, or freshness evidence added.
- **Teaching-hub first batch**: Added a beginner Git fundamentals explanation and rewrote the Kubernetes and Terraform fundamentals explanations with plain definitions, analogies with stated limits, Mermaid diagrams with text alternatives, bounded illustrative examples, understanding checks, and keyed official-source citations. Start here now reads Git fundamentals before Git undo and recovery. All three pages remain drafts without new review or execution evidence.
- **Authoring template**: The knowledge article template now provides separate Explanation and How-to Guide skeletons aligned with the teaching standard in the writing instructions.

## 2026-09-26

- **Publishing decision**: ADR-0005 accepts a separate static reading site built from pinned `main` revisions and moves reader testing to after the first release. The Markdown bundle remains canonical.

## 2026-09-21

- **Terraform workflow quality pass**: Expanded the stable core workflow guide with official Terraform CLI command sources, expected results, saved-plan handling, provider lock-file guidance, CI validation boundaries, and stop signals.
- **Terraform state quality pass**: Expanded the stable state-management guide with official Terraform state, backend, locking, remote-state, sensitive-data, plan, and state-command sources; added safer mental models, command guidance, drift handling, and recovery decision points.
- **Git troubleshooting quality pass**: Expanded the stable undo-and-recovery guide with official Git source records, safer decision paths, expected results, recovery limits, untracked cleanup guidance, reflog branch recovery, and disposable-repository validation evidence.

## 2026-09-20

- **Quality refactor**: Added a deterministic concept catalog, retrieval-case data, command-path validation, stronger metadata checks, and CI coverage for each.
- **Learning routes**: Extracted Kubernetes fundamentals and the Terraform local-state tutorial from reserved indexes into metadata-bearing concepts.
- **Foundation coverage**: Added safer `kubectl` inspection, Terraform fundamentals, and FinOps cost-allocation guides with official sources and review deadlines.
- **Migration repair**: Corrected post-migration command paths, Terraform formatting scope, and contributor index guidance.
- **Migration**: Moved the curated engineering knowledge corpus into this Open Knowledge Format v0.2 bundle.
- **Structure**: Replaced directory `README.md` indexes with reserved `index.md` files and added profile metadata to every concept.
- **Licensing**: Adopted CC BY 4.0 for authored knowledge and visual assets; repository code and automation remain MIT-licensed.
