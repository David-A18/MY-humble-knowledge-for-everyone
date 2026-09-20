# Repository context

## Purpose

`engineering-knowledge-base` is a public, Git-backed collection of practical
engineering knowledge. Its canonical curated corpus is the
[Open Knowledge Format v0.2 bundle](knowledge/index.md), designed for human
reading and AI-agent retrieval.

## Repository boundaries

| Area | Role |
| --- | --- |
| [`knowledge/`](knowledge/index.md) | Canonical, CC BY 4.0 licensed knowledge bundle. Reader-facing concepts, indexes, glossary, templates, decisions, and asset guidance live here. |
| Root files | Repository entry point, governance, licensing, plans, and contributor instructions. |
| [`sources/`](sources/README.md) | Raw or archived input, not curated OKF knowledge. |
| [`knowledge-base-upgrade/`](knowledge-base-upgrade/README.md) | Develop-branch upgrade work and maintainer tooling. |
| [`.github/`](.github/PULL_REQUEST_TEMPLATE.md) and [`scripts/`](scripts/validate-okf.py) | Automation and validation, licensed under MIT. |

## Navigation model

1. Readers begin at [README.md](README.md), then open [knowledge/index.md](knowledge/index.md).
2. Each `index.md` lists its concepts and child indexes.
3. Concepts use related links to move across subjects and return to nearby indexes.
4. Agents read indexes first, then load only the concepts needed for a request.

## OKF profile

Every non-reserved Markdown file under `knowledge/` has parseable YAML
frontmatter. The repository requires `type`, `title`, `description`, `tags`,
`status`, `maturity`, `audience`, and `maintainer`.

`status` is `draft`, `stable`, or `deprecated`. `maturity` preserves the
reader-facing distinction between `initial-outline`, `draft`, `maintained`, and
`deprecated`. Provenance, human review, generation details, and freshness are
optional and must be recorded only when evidence exists.

Use the official [OKF v0.2 specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md). The previous `knowledge-catalog` copy is frozen.

## Validation

- [`scripts/validate-okf.py`](scripts/validate-okf.py) enforces the repository's strict OKF producer profile.
- [`scripts/validate-local-links.mjs`](scripts/validate-local-links.mjs) enforces valid internal links and reachability, a stricter rule than OKF consumer conformance.
- Markdown lint, issue-template validation, GitHub label checks, link validation, Terraform format checks, and OKF validation run in CI on `develop` and `main`.

## Validation scripts

The maintained scripts live in [`scripts/`](scripts/validate-okf.py). Use the
commands in [AGENTS.md](AGENTS.md) before committing.

## Licensing

Original prose and visual material in `knowledge/` are
[CC BY 4.0](LICENSES/README.md). Scripts, manifests, configuration, workflow
files, executable examples, and automation are [MIT licensed](LICENSE).
External citations are evidence, not permission to reproduce external material.
