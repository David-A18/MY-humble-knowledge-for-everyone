# Roadmap

This is the single current plan for the knowledge base. Earlier plans and
audits are in the [governance archive](governance/archive/README.md).

## Foundation plan (started 2026-11-19)

Build a strong, reliable base first, then design the website. Phases 1 and 2
must be complete before website design starts, because the website consumes the
structure and checks they define.

### Phase 1: Repository structure — done

- [x] `knowledge/` is Markdown only; runnable lab files moved to [examples](examples/README.md), and lab tutorials moved up to their topic.
- [x] The sample OKF bundle moved out of the reader corpus, and its reserved types were retired.
- [x] The duplicate `maturity` field was removed; `status` is the single trust signal.
- [x] Empty placeholder sections (`ai-agents`, `ml`, `mlops`, `assets`) were removed; they are listed as planned topics below.
- [x] Root planning documents moved to [governance](governance/README.md), with superseded plans archived.
- [x] Decision-record file names now follow the lowercase kebab-case rule.
- [x] Merged into `develop` and released to `main` on 2026-11-19 after the repository gate passed (David-A18/MY-humble-knowledge-for-everyone#7, #8, and #9).
- [ ] Maintainer: delete the seven fully merged stale branches (`codex/aws-governance-access`, `codex/aws-security-review`, `codex/core-reader-journey`, `codex/istio-security-runtime`, `codex/knowledge-website-plan`, `codex/manifest-validation-runtime`, `feat/rag-retrieval-engine`).
- [ ] Maintainer: decide on `codex/knowledge-clarity-upgrade`, which holds 223 unmerged commits from 2026-10-17, before deleting it.

### Phase 2: Security and integrity pipeline — live on main, settings pending

- [x] One required [repository gate](.github/workflows/repository-gate.yml): content policy, moderation, secret scan, OKF and catalog, links, Markdown lint, and issue templates.
- [x] [Content policy](governance/content-policy.md) checks: allowed text file types, no binaries or executables, hidden-Unicode detection, safe Markdown, and link safety with a reviewed domain allowlist.
- [x] Moderation scan with hashed blocked terms, plus a [trusted content scan](.github/workflows/trusted-content-scan.yml) that pull requests cannot weaken and that records moderation cases.
- [x] Every action pinned to a commit SHA, with [Dependabot](.github/dependabot.yml) updates.
- [x] Tested the pipeline: the repository gate passed on a pull request, and a simulated malicious pull request was caught by the policy checker and the trusted scan.
- [ ] Maintainer: apply the repository settings in the [content policy checklist](governance/content-policy.md#maintainer-settings-checklist): branch protection, required checks, secret scanning, and labels.

### Phase 3: Content quality — done; ongoing upkeep

- [x] Plain-language style rules added to the [authoring instructions](instructions.md#write-for-everyone).
- [x] Split the six pages over 2,900 words by reader task (Git and eksctl command catalogs, the GitHub Actions catalog, the Velero runbooks, and two Crossplane pages). The glossary stays one lookup page.
- [x] Reviewed the remaining long pages: split the Velero integrations, K9s, and Crossplane component-model pages. The rest (about 2,000 to 2,350 words) each serve one reader task.
- [x] Rewrote the openings of [Start here](knowledge/start-here.md) and the Kubernetes and Terraform fundamentals in plain language, with a first example.
- [x] Added plain openings and "new here?" starting points to the Git, AWS, and FinOps entry pages.
- [x] Replaced nine empty sections: new starter pages for Git practices and tricks, AWS fundamentals, storage, and troubleshooting; Kubernetes practices and tricks moved from indexes into pages; AWS solutions-architect and Azure placeholders removed.
- [ ] Ongoing: apply the plain-language rules whenever a page is edited.
- [x] Expanded the four outline pages in [cross-topic guides](knowledge/cross-topic-guides/index.md) into complete guides.
- [ ] Ongoing: review each section for relevance and duplication, using the [section quality ledger](governance/section-quality-progress.md).

### Phase 4: News — first edition published

- [x] [ADR-0006](knowledge/decision-records/adr-0006-news-briefs.md), the [news editorial policy](governance/news-editorial-policy.md), the [news brief template](knowledge/templates/news-brief-template.md), validator rules, and the [news section](knowledge/news/index.md).
- [x] Published the [first weekly roundup](knowledge/news/2026/11/index.md) with four briefs from primary sources, and added their domains to the allowlist.
- [ ] Publish a roundup each week, and mark briefs `deprecated` when later events overturn them.
- [ ] Optional: a scheduled workflow that collects candidate links into `sources/` for a person to turn into briefs. Nothing publishes automatically.

### Phase 5: Website — critical, scheduled for a separate session

The knowledge base has no deployed website yet. The specification is ready in the
[website plan](knowledge-base-upgrade/features/knowledge-website/README.md) and
[ADR-0005](knowledge/decision-records/adr-0005-git-backed-reading-site.md).

- [x] Prepared the [landing zone design pack](knowledge-base-upgrade/features/knowledge-website/landing-zone/README.md): brief, reference toolchain, and preflight. Open owner decisions are listed in the brief.
- [x] Chose the landing zone concept (interactive knowledge spirals) and built a working prototype; see the [concept and build plan](knowledge-base-upgrade/features/knowledge-website/landing-zone/spiral-concept-and-plan.md).
- [ ] Generate the Gemini reference clips and tune the prototype to them.
- [ ] Choose the website repository and hosting provider.
- [ ] Build the static site from the content contract, including the news listing and feed, search, and trust labels.
- [ ] Set `SITE_REPOSITORY` so [website dispatch](.github/workflows/website-dispatch.yml) notifies the site after each validated `main` update.
- [ ] Run reader task tests after launch.

### Planned topics

Agent workflows and evaluation, machine-learning fundamentals, MLOps, and Azure return
as sections when each has at least one complete, sourced concept. Until then,
the [AI section](knowledge/ai/index.md) and [LLM section](knowledge/llm/index.md)
cover current material.

## Evidence follow-ups

The [new learning paths](knowledge/index.md#expanded-learning-paths) document all ten requested topic groups. These follow-ups add runtime evidence; they are not claims that live cloud or reader testing occurred during authoring.

| Follow-up | Completion evidence |
| --- | --- |
| Review draft concepts and assign ownership | A real maintainer, official sources, review scope, and a justified freshness deadline; keep drafts visible until then. |
| Istio, IRSA, kro and manifest labs | [Istio sidecar](knowledge/kubernetes/applications-and-tools/istio/security-lab.md#validation) and [manifest validation](knowledge/kubernetes/applications-and-tools/manifest-validation/regression-lab-and-ci.md#validation-boundary) have recorded runs. Next evidence includes authorized IRSA and disposable kro runs, plus Istio ambient and rollout cases. |
| Collector/Pixie/Kafka deployment labs | Delivery/capture, outage/recovery, and persistent-state results on supported infrastructure. |
| RAG answer quality | A ten-question spot check on `qwen3:4b` is in the [lab](knowledge/llm/rag/repository-lab.md). Still open: a scored run covering paraphrases, conflicting sources, and grounding. |
| Dev Container/Ona runtime | Container startup/rebuild and, where access exists, hosted workflow evidence. |

Use the [maintenance review queue](governance/maintenance-review-queue.md) to schedule guide reviews and the [knowledge-base upgrade hub](knowledge-base-upgrade/README.md) for repository-level tools, skills, and MCP templates.

## Prioritized content backlog

This replaces the old broad bullets after checking the current articles and indexes. Reviewed documentation and executed infrastructure are distinct completion states. The [section ledger](governance/section-quality-progress.md) tracks full section reviews; these entries identify concrete remaining deliverables.

| Priority / state | Existing coverage | Remaining task and completion criterion |
| --- | --- | --- |
| P1 / foundation documentation complete; runtime open | [AWS networking](knowledge/cloud/aws/networking/index.md): ten guides and a read-only inspection lab | Follow up with account-backed path verification, permitted/denied traffic and failover results; add focused Transit Gateway provisioning, hybrid DNS/BGP, and endpoint-policy recovery procedures. |
| P1 / foundation documentation and local labs complete; remote evidence open | [Terraform learning path](knowledge/terraform/index.md), [module/workspace lab](knowledge/terraform/module-workspace-lab.md), and [provider alias lab](knowledge/terraform/provider-alias-lab.md) | Follow up with backend-specific competing-writer/restore/migration drills, cloud/provider imports, drift/recovery, and hosted credential/artifact checks. Preserve the executed local contracts and existing workflow/state guides. |
| P1 / foundation docs and synthetic calculations complete; real evidence open | [FinOps learning path](knowledge/finops/index.md), [AWS FinOps](knowledge/cloud/aws/finops/index.md), and [calculation lab](knowledge/finops/cost-analysis-lab.md) | Follow up with account-backed notification delivery, source-bill reconciliation, representative controlled rightsizing/SLO tests, and attributable financial outcomes. Synthetic math does not establish realized savings. |
| P1 / manifest source/runtime lab verified; extensions open | [Manifest validation](knowledge/kubernetes/applications-and-tools/manifest-validation/index.md) | Preserve the linked eight offline/thirteen live assertions and require each revision's CI. Extend with Helm/Helm Diff release gates, GitOps ownership/controller, CRD admission and independent platform/reader cases. |
| P1 / documentation complete; runtime open | [Kubernetes troubleshooting](knowledge/kubernetes/troubleshooting/index.md) | Eleven focused guides cover the requested diagnostic areas. Next evidence: disposable failure/recovery drills, actual versions, and redacted expected outputs. |
| P2 / documentation complete; broader drills open | [Git undo/recovery](knowledge/git/troubleshooting/undo-and-recovery.md) | Preserve the source-reviewed and locally exercised guide. Add submodule/corruption/shared-history edge cases only as separate bounded recovery drills. |
| P2 / governance docs and synthetic review complete; account evidence open | [AWS governance and access](knowledge/cloud/aws/governance-and-access/index.md), [access-review lab](knowledge/cloud/aws/governance-and-access/access-review-lab.md) | Validate actual collection/pagination, human login and allowed/denied operations, provisioning, SCP/RCP changes, emergency recovery and issued-session containment in authorized accounts. The local join is not IAM evaluation. |
| P2 / foundation docs and local contracts complete; live access open | [AWS security](knowledge/cloud/aws/security/index.md), [policy-contract lab](knowledge/cloud/aws/security/policy-contract-lab.md), and [EKS comparison](knowledge/cross-topic-guides/eks-workload-identity.md) | Execute authorized IAM simulation and positive/negative resource tests, IRSA/Pod Identity exchange and cache tests, KMS/secret rotation, audit/notification delivery, and session-containment/recovery drills. Preserve local fixture evidence separately. |
| P2 / local journey implemented; independent reader/cloud evidence open | [Cross-topic guides](knowledge/cross-topic-guides/index.md), including local, EKS, GitOps, and observability routes | Retain the checked Git → kind → local Terraform beginner route and its failure/recovery/cleanup gates. Run independent reader/platform sessions; then connect one authorized GitHub Actions → Terraform → AWS → Kubernetes journey with explicit ownership and sandbox results. |
| P2 / partial | [Decision records](knowledge/decision-records/index.md) | Add a cloud trade-off decision, with a Mermaid diagram where it resolves a concrete reader choice; document consequences and reconsideration criteria. |
| P2 / partial | [New topic series](knowledge/index.md#expanded-learning-paths) | Complete the runtime acceptance evidence listed above; retain draft labels where ownership/runtime review is missing. |
| P3 / planned | [Operational troubleshooting](knowledge/kubernetes/troubleshooting/index.md) and [best practices](knowledge/kubernetes/best-practices/index.md) | Assemble an incident handbook with escalation, evidence capture, and readiness checklists after validating the component runbooks. |
| P3 / planned | Existing [AWS and Kubernetes guides](knowledge/cross-topic-guides/index.md) | Add one reusable reference architecture with requirements, threat/failure model, costs, manifests, cleanup, and bounded execution evidence. |

Command-output captures (as text) are supporting tasks for the selected guide, not a separate repository-wide rewrite. Keep unrelated improvements queued.

## Prioritization rules

1. Document recurring operational problems first.
2. Prefer high-signal commands, diagnostics, and decision criteria.
3. Keep pages small enough to maintain.
4. Update navigation immediately when adding new pages.
5. Use reader feedback and review evidence from the maintenance queue before starting broad restructuring work.
