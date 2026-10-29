# Knowledge-base publication audit

Audit date: **2026-10-29**. This is a dated evidence record, not a live CI dashboard.

## Current source of truth

Fetching GitHub revealed 58 commits absent from the original checkout. Published `main` at `b0c4f0e` already migrated the corpus to `knowledge/`, adopted reserved `index.md` navigation, added strict OKF metadata and a generated catalog, expanded Git/Terraform/local learning, and repaired the old lint findings.

The ten requested topic groups were ported into that current structure without replacing the newer guides or governance. Their [learning paths](knowledge/index.md#expanded-learning-paths) cover Istio security, Kubernetes tools, manifest differences/regressions, IRSA, kro, observability/eBPF/Pixie, AWS CDK, aggregation, RAG, and Ona/Gitpod.

New concepts remain `draft` with an `unassigned` maintainer. Their official source records and citations identify evidence; they do not claim human approval or production execution. Executable examples and configurations remain MIT-licensed; authored knowledge follows the bundle's CC BY 4.0 license.

## Validation

| Gate | Recorded result |
| --- | --- |
| Repository checks | All 21 required/example commands passed, including OKF/profile fixtures, canonical paths, catalog reproducibility, 22 retrieval cases, issue templates, live label comparison, Markdown, links, and executable sample tests. |
| Markdown | All 369 curated/governance Markdown files pass lint. |
| Navigation | Local targets, fragments, parent indexes, and reachability pass the maintained repository validator. |
| External evidence | All 434 unique external URLs checked returned HTTP 200 after redirects; external fragments were not tested. |
| Discovery | The generated catalog contains 218 concepts; ten new reader questions supplement the existing retrieval dataset. |
| RAG | Five test methods cover exclusions, rebuilding, citations, mocked generation, lifecycle handling, and lexical queries across all ten topic groups. |
| CDK | TypeScript/Python assertions and synthesis pass; generated resource contracts match exactly. |
| Manifest tools | dyff 1.12.0, kubeconform 0.8.0, and Conftest 0.71.1 checks pass against the migrated fixtures. |
| Kubernetes schemas | Fourteen native fixture objects pass strict Kubernetes 1.34.0 schemas; core JSON fixtures were also parsed and checked in the initial authoring run. |
| Extension schemas | Istio 1.31.0 security policies, kro 0.9.4 RGD, and Chainsaw 0.2.15 test validate against their selected schemas. |
| Signing | The synthetic JWT signature and public JWKS verify; no private key is written. |
| Data and protocol tests | Aggregation replay/windows, Kafka processed-offset commits, and mocked OTLP acceptance/rejection/error contracts pass. |
| Portable maintenance | Label validation works through a tested REST fallback without `gh`; retrieval-validator tests use the selected Python interpreter on Windows and Linux. |
| Git | Whitespace validation passes; only the isolated publication worktree is staged. |

The expansion adds 79 Markdown concepts/indexes/governance pages to the current structure. New concepts have traceable official source records and keyed citations. Human review, cloud execution, and hosted model quality are not inferred from these local checks.

Local runtime versions: Python 3.13.17, SQLite 3.50.4/FTS5, Node 24.22.1, CDK library 2.275.0, constructs 10.8.1, CDK CLI 2.1146.1, and markdownlint-cli2 0.24.0. Hosted CI is checked against the exact published revision rather than inferred from a previous green run.

## Source freshness and operating limits

- Rechecked the current Istio release documentation, kro 0.9.4 documentation, AWS IRSA/Pod Identity guidance, and Ona availability using official sources.
- Ona's current documentation states that new customer signup is closed. Hosted walkthroughs require existing-organization access; the portable Dev Container example remains usable independently.
- Pinned educational tool/image versions identify the example baseline, not a promise that they are the newest supported release. Review compatibility and security updates before live use.
- RAG accepts the repository root or the `knowledge/` bundle, preserves real repository citation paths and draft/maturity labels, and excludes deprecated concepts. It does not promote draft sources into verified production guidance.
- Live cluster/AWS/Pixie/Ona/container-startup tests remain unexecuted on this host. Local state-engine restart/replay tests, source/schema checks, and mocked protocol tests are separate evidence.

## Original workspace preservation

The original checkout and its unrelated Jev/Laya draft, `work/` files, pending metadata, and unpushed Claude Code commit remain untouched. Publication uses an isolated worktree based on current remote `main`; it does not publish those drafts or rewrite the original checkout's history.

## Ongoing maintenance

Weekly upkeep was requested by the user. Reviews should compare against current `origin/main`, choose a focused quality/freshness improvement, verify official sources, preserve unrelated work, run the maintained validation suite, and publish validated changes to `main`. Record runtime gaps honestly and stay quiet when no meaningful action is needed.

Use the [maintenance queue](maintenance-review-queue.md) for work selection and [roadmap](ROADMAP.md) for broader direction. Do not treat a future runtime test or an unowned draft as completed review evidence.

## Related links

- [Knowledge bundle](knowledge/index.md)
- [Roadmap](ROADMAP.md)
- [Maintenance review queue](maintenance-review-queue.md)
- [Contributor contract](CONTRIBUTING.md)
- [Back to repository index](README.md)
