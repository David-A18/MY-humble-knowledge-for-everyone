# Repository context

## Expanded topic routes

The [new learning paths](knowledge/index.md#expanded-learning-paths) use the existing OKF bundle and generated catalog. Keep source/API review distinct from runtime evidence; see the [audit](governance/archive/knowledge-base-audit.md). Preserve newer local learning and Terraform material while improving related topics.

The [section quality ledger](governance/section-quality-progress.md) records reviewed sections, remaining evidence, and the next focused batches. Read it before selecting ongoing improvement work.

## Beginner route maintenance

Start at [Start here](knowledge/start-here.md) and [local preflight](knowledge/cross-topic-guides/local-learning-preflight.md). The local learning workflow checks Git file recovery, Terraform state behavior, and a disposable kind deployment/failure/recovery path. Keep hosted execution, local platform setup, and independent reader evidence distinct; never infer cluster or cloud authority from a link check.

## Manifest-validation routing

Use [manifest validation](knowledge/kubernetes/applications-and-tools/manifest-validation/index.md) to separate text/semantic differences, versioned schema and Rego coverage, prospective API comparison and actual Service behavior. Its private-cluster runner uses synthetic fixtures and explicit contexts; hosted results are revision-specific. Helm/Helm Diff and GitOps selection guidance is not evidence that those integrations ran.

## Istio policy routing

The [Istio lab](knowledge/kubernetes/applications-and-tools/istio/security-lab.md) runs one sidecar request path through baseline connectivity, STRICT peer authentication, JWT validation and combined authorization. Use its recorded result for that pinned setup and the ambient guide for waypoint policy placement.

## AWS identity routing

Use [governance and human access](knowledge/cloud/aws/governance-and-access/index.md) for organization/account ownership, workforce federation, guardrails and offboarding. Use [AWS security](knowledge/cloud/aws/security/index.md) for request evaluation, credential behavior, workload identity and data/security operations. The access-review lab is a synthetic inventory join, never an IAM evaluator or session-containment attestation.

## Purpose

`engineering-knowledge-base` is a public, Git-backed collection of practical
engineering knowledge. Its canonical curated corpus is the
[Open Knowledge Format v0.2 bundle](knowledge/index.md), designed for human
reading and AI-agent retrieval.

## Repository boundaries

| Area | Role |
| --- | --- |
| [`knowledge/`](knowledge/index.md) | Canonical, CC BY 4.0 licensed knowledge bundle, Markdown only. Reader-facing concepts, news briefs, indexes, glossary, templates, and decisions live here. |
| [`examples/`](examples/README.md) | Runnable lab files that knowledge pages link to, in text formats only. |
| [`governance/`](governance/README.md) | Content and security policy, link allowlists, moderation lists, editorial policy, review ledgers, and archived plans. |
| Root files | Repository entry point, roadmap, licensing, and contributor instructions. |
| [`sources/`](sources/README.md) | Raw or archived input, not curated OKF knowledge. |
| [`knowledge-base-upgrade/`](knowledge-base-upgrade/README.md) | Develop-branch upgrade work and maintainer tooling. |
| [Website upgrade plan](knowledge-base-upgrade/features/knowledge-website/README.md) | Source-side contract and rollout plan for a separate static reading site. |
| [`.github/`](.github/PULL_REQUEST_TEMPLATE.md) and [`scripts/`](scripts/validate-okf.py) | Automation and validation, licensed under MIT. |

## Navigation model

1. Readers begin at [README.md](README.md), then open [knowledge/index.md](knowledge/index.md).
2. Each `index.md` lists its concepts and child indexes.
3. Concepts use related links to move across subjects and return to nearby indexes.
4. Agents read indexes first, then load only the concepts needed for a request.

## OKF profile

Every non-reserved Markdown file under `knowledge/` has parseable YAML
frontmatter. The repository requires `type`, `title`, `description`, `tags`,
`status`, `audience`, and `maintainer`.

`status` is `draft`, `stable`, or `deprecated`. The former `maturity` field
duplicated `status` and was retired on 2026-11-19. News briefs also require
`published`, `sources`, and `stale_after`. Provenance, human review, generation details, and freshness are
optional and must be recorded only when evidence exists.

Use the official [OKF v0.2 specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md). The previous `knowledge-catalog` copy is frozen.

## Validation

- [`scripts/validate-okf.py`](scripts/validate-okf.py) enforces the repository's strict OKF producer profile.
- [`scripts/build-knowledge-catalog.py`](scripts/build-knowledge-catalog.py) derives a deterministic catalog for AI retrieval and maintenance tooling.
- [`scripts/validate-command-paths.py`](scripts/validate-command-paths.py) rejects fenced examples that still reference pre-OKF root paths.
- [`scripts/validate-retrieval-cases.py`](scripts/validate-retrieval-cases.py) keeps golden retrieval tasks aligned with real concepts and source IDs.
- [`scripts/evaluate-retrieval.py`](scripts/evaluate-retrieval.py) scores the [RAG lab](knowledge/llm/rag/repository-lab.md) against those tasks and unanswerable questions, and fails below agreed floors.
- [`scripts/kb-mcp-server.py`](scripts/kb-mcp-server.py) serves read-only search and fetch to AI hosts over MCP.
- [`scripts/report-knowledge-health.py`](scripts/report-knowledge-health.py) reports concept counts, trust, sourcing, and thin pages by area.
- [`scripts/check-github-labels.py`](scripts/check-github-labels.py) compares declared labels with GitHub; when `gh` is absent it uses the read-only REST API. Its tests cover pagination and failure reporting without credentials.
- [`scripts/validate-local-links.mjs`](scripts/validate-local-links.mjs) enforces valid internal links and reachability, a stricter rule than OKF consumer conformance.
- [`scripts/validate-repository-policy.py`](scripts/validate-repository-policy.py) enforces the [content policy](governance/content-policy.md): allowed text file types, no binaries or executables, safe Markdown, and safe, allowlisted links.
- [`scripts/moderate-content.py`](scripts/moderate-content.py) blocks profanity, explicit sexual language, and slurs using hashed term lists.
- The [repository gate](.github/workflows/repository-gate.yml) runs all checks, a secret scan, external link checks, and Markdown lint on every pull request and on `develop` and `main`. The [trusted content scan](.github/workflows/trusted-content-scan.yml) re-runs the policy and moderation checks from the default branch and records moderation cases.

## Validation scripts

The maintained scripts live in [`scripts/`](scripts/validate-okf.py). Use the
commands in [AGENTS.md](AGENTS.md) before committing.

## Licensing

Original prose and visual material in `knowledge/` are
[CC BY 4.0](LICENSES/README.md). Scripts, manifests, configuration, workflow
files, executable examples, and automation are [MIT licensed](LICENSE).
External citations are evidence, not permission to reproduce external material.
