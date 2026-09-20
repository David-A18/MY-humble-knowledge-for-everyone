# AI agent router

Use this guide when changing the repository. The reader-facing knowledge base is
the [OKF v0.2 bundle](knowledge/index.md); governance and automation remain
outside that bundle.

## First reads

1. [README.md](README.md)
2. [context.md](context.md)
3. [instructions.md](instructions.md)
4. [CONTRIBUTING.md](CONTRIBUTING.md)
5. The nearest parent `index.md` in [knowledge](knowledge/index.md)

## OKF authoring contract

- Create reader-facing content only under `knowledge/`.
- Use lowercase kebab-case names. Each knowledge directory needs an `index.md`.
- `index.md` and `log.md` are reserved. Nested indexes and logs have no frontmatter; only `knowledge/index.md` declares `okf_version: "0.2"`.
- Every other Markdown file is a concept with `type`, `title`, `description`, `tags`, `status`, `maturity`, `audience`, and `maintainer`.
- Use the controlled Diátaxis-oriented types in [instructions.md](instructions.md). Keep one primary reader outcome per concept.
- Use relative internal links and list every direct concept and child directory in its parent `index.md`.
- Do not invent provenance, reviewers, execution evidence, or freshness dates. Add `sources`, `verified`, `generated`, and `stale_after` only when they are real.
- Treat Markdown under `sources/`, `.github/`, and repository-governance files as outside the bundle.

## Routes

| Need | Start here |
| --- | --- |
| Reader-facing technical knowledge | [Knowledge bundle](knowledge/index.md) |
| Templates and page structures | [Templates](knowledge/templates/index.md) |
| Shared terminology | [Glossary](knowledge/glossary.md) |
| Architecture decisions | [Decision records](knowledge/decision-records/index.md) |
| Upgrades, tools, skills, or MCP templates | [Upgrade hub](knowledge-base-upgrade/README.md) |
| Raw source notes | [Sources](sources/README.md) |

## Validation and publication

Run these checks before committing:

```bash
git status --short --branch
python3 scripts/test-okf-validator.py
python3 scripts/validate-okf.py knowledge
python3 scripts/test-issue-template-validator.py
python3 scripts/validate-issue-templates.py
python3 scripts/check-github-labels.py --repo David-A18/MY-humble-knowledge-for-everyone
npx markdownlint-cli2 "**/*.md"
node scripts/test-local-link-validator.mjs
node scripts/validate-local-links.mjs
git diff --check
```

Commit and push only intended changes. Use `develop` for knowledge-base upgrades,
wait for CI, and merge to `main` only when the bundle and governance checks pass.
