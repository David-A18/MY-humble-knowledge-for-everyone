# AI agent router

Use this guide when changing the repository. The reader-facing knowledge base is
the [OKF v0.2 bundle](knowledge/index.md); runnable lab files, governance, and
automation stay outside that bundle.

## First reads

1. [README.md](README.md)
2. [context.md](context.md)
3. [instructions.md](instructions.md)
4. [CONTRIBUTING.md](CONTRIBUTING.md)
5. [Content and security policy](governance/content-policy.md)
6. The nearest parent `index.md` in [knowledge](knowledge/index.md)

## OKF authoring contract

- Create reader-facing content only under `knowledge/`, and only as Markdown (`.md`). Put runnable lab files under [examples](examples/README.md), mirroring the topic path.
- Use lowercase kebab-case names. Each knowledge directory needs an `index.md`.
- `index.md` and `log.md` are reserved. Nested indexes and logs have no frontmatter; only `knowledge/index.md` declares `okf_version: "0.2"`.
- Every other Markdown file is a concept with `type`, `title`, `description`, `tags`, `status`, `audience`, and `maintainer`.
- Use the controlled Diátaxis-oriented types in [instructions.md](instructions.md). Keep one primary reader outcome per concept, and follow its plain-language style rules.
- News briefs use type `News Brief` in `knowledge/news/YYYY/MM/` with `published`, `sources`, and `stale_after`; see the [news editorial policy](governance/news-editorial-policy.md).
- Use relative internal links and list every direct concept and child directory in its parent `index.md`.
- Do not invent provenance, reviewers, execution evidence, or freshness dates. Add `sources`, `verified`, `generated`, and `stale_after` only when they are real.
- No images, embedded media, or raw HTML. Link only to domains on the reviewed [allowlist](governance/policy/allowed-link-domains.txt); add new domains in the same change so a maintainer reviews them.
- Treat Markdown under `sources/`, `examples/`, `governance/`, `.github/`, and repository-governance files as outside the bundle.

## Routes

| Need | Start here |
| --- | --- |
| Reader-facing technical knowledge | [Knowledge bundle](knowledge/index.md) |
| News briefs | [News](knowledge/news/index.md) |
| Runnable lab files | [Examples](examples/README.md) |
| Templates and page structures | [Templates](knowledge/templates/index.md) |
| Shared terminology | [Glossary](knowledge/glossary.md) |
| Allowed content, link safety, and moderation | [Content and security policy](governance/content-policy.md) |
| Plans and ongoing section reviews | [Roadmap](ROADMAP.md) and [governance](governance/README.md) |
| Architecture decisions | [Decision records](knowledge/decision-records/index.md) |
| Upgrades, tools, skills, or MCP templates | [Upgrade hub](knowledge-base-upgrade/README.md) |
| Designing the website landing zone | [Landing zone design pack](knowledge-base-upgrade/features/knowledge-website/landing-zone/README.md) |
| Raw source notes | [Sources](sources/README.md) |

## Validation and publication

Run these checks before committing. CI runs the same checks in the
[repository gate](.github/workflows/repository-gate.yml):

```bash
git status --short --branch
python3 scripts/test-repository-policy.py
python3 scripts/validate-repository-policy.py
python3 scripts/test-content-moderation.py
python3 scripts/moderate-content.py
python3 scripts/test-okf-validator.py
python3 scripts/validate-okf.py knowledge
python3 scripts/test-command-path-validator.py
python3 scripts/validate-command-paths.py knowledge
python3 scripts/build-knowledge-catalog.py --check
python3 scripts/test-retrieval-case-validator.py
python3 scripts/validate-retrieval-cases.py
python3 examples/llm/rag/test_rag.py
python3 scripts/test-kb-mcp-server.py
python3 scripts/evaluate-retrieval.py --unanswerable tests/unanswerable-questions.yaml --min-hit-at-3 0.9 --min-refused 0.8
python3 scripts/test-issue-template-validator.py
python3 scripts/validate-issue-templates.py
python3 scripts/test-github-label-validator.py
python3 scripts/check-github-labels.py --repo David-A18/MY-humble-knowledge-for-everyone
npx markdownlint-cli2 "**/*.md"
node scripts/test-local-link-validator.mjs
node scripts/validate-local-links.mjs
git diff --check
```

Commit and push only intended changes. Use `develop` for knowledge-base upgrades,
wait for CI, and merge to `main` only when the repository gate and the
trusted content scan pass.
