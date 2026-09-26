# Website content contract

## Source snapshot

The website's `content-lock.json` contains exactly the public source repository and a full lowercase 40-character commit SHA:

```json
{
  "repository": "David-A18/MY-humble-knowledge-for-everyone",
  "commit": "<40-character-commit-sha>"
}
```

The website accepts `okf_version: "0.2"` in `knowledge/index.md` and `catalog_version: "1"` in [the derived catalog](../../../generated/README.md). It checks catalog freshness at the locked commit with the source repository's validator. An unknown version or mismatch fails the build. The catalog provides metadata for concepts only; `index.md` pages are discovered from source paths and do not receive invented concept metadata.

## Publication inventory

- Include every `knowledge/**/*.md` except files named `log.md`. `knowledge/index.md` is the home page; nested indexes and all concepts, including [decision records](../../../knowledge/decision-records/index.md), are public pages.
- Copy non-Markdown files under `knowledge/` that are referenced by published pages into the static artifact. Keep paths safe within the bundle; reject traversal outside the checked-out repository.
- Do not publish root governance, `sources/`, `.github/`, scripts, or generated files as site pages. A link to one of these opens its source file or directory on GitHub at the locked SHA. A link to an excluded `log.md` follows the same rule.
- Keep source citations in articles. Render recorded source links and optional verification fields without treating absent data as evidence.

## Routes and links

| Source target | Website behavior |
| --- | --- |
| `knowledge/index.md` | `/` under the configured base path. |
| `knowledge/x/index.md` or `knowledge/x/` | `/x/`. |
| `knowledge/x/page.md` | `/x/page/`. |
| `#heading` or `page.md#heading` | Preserve fragment semantics with GitHub-compatible slugs and duplicate-heading suffixes. |
| Repository file outside published bundle | `https://github.com/<repository>/blob/<SHA>/<path>`. |
| Repository directory outside published bundle | `https://github.com/<repository>/tree/<SHA>/<path>`. |
| External URL or email link | Preserve the authored destination. |

Normalize URL encoding without changing case-sensitive source path lookup. All generated website routes use trailing slashes and the configured base path. Validate that every internal target and fragment exists in the generated site. Keep existing GitHub-style source links working through redirect stubs when a published Markdown path moves. The website repository owns `redirects.json`; its CI compares the previous published route manifest with the proposed one and fails on an uncovered removal.

## Presentation metadata

Concept pages use their required OKF fields: `type`, `title`, `description`, `tags`, `status`, `maturity`, `audience`, and `maintainer`. Display `sources`, `verified`, `generated`, and `stale_after` only when actually recorded. Index pages have navigation text rather than concept frontmatter. All pages show a link to their source at the locked SHA and the applicable [content license](../../../LICENSES/README.md).

## Related links

- [Requirements](requirements.md)
- [Architecture](architecture.md)
- [Rollout](rollout.md)
- [Website plan](README.md)
