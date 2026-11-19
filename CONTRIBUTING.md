# Contributing

Thank you for improving this knowledge base. Read [AGENTS.md](AGENTS.md),
[context.md](context.md), [instructions.md](instructions.md), and the
[content and security policy](governance/content-policy.md) before editing.

## What we accept

- **Text only.** Knowledge is Markdown (`.md`) under `knowledge/`. Code goes in
  fenced code blocks; runnable lab files go in [examples](examples/README.md) in
  plain-text formats.
- **No images, video, binaries, archives, or executables.** Use tables, lists, or
  Mermaid diagrams instead of pictures.
- **Safe links only.** Use `https://` links to domains on the reviewed
  [allowlist](governance/policy/allowed-link-domains.txt). If you need a new
  domain, add it in the same pull request and explain why it is trustworthy.
- **Respectful language.** Offensive, sexual, or hateful content is blocked
  automatically and recorded for maintainer review. Confirmed cases lead to the
  sanctions in the [content policy](governance/content-policy.md#moderation-and-sanctions).

## Add or improve knowledge

1. Start from [knowledge/index.md](knowledge/index.md) and find the nearest parent `index.md`.
2. Choose one Diátaxis reader outcome and use the corresponding `type`.
3. Write for everyone: open with a plain summary, show a small example, and
   define terms. See [Write for everyone](instructions.md#write-for-everyone).
4. Add complete OKF profile frontmatter and focused, original Markdown content.
5. Update the nearest parent index, related concepts, and `knowledge/log.md` for notable changes.
6. Add provenance and review metadata only when you can substantiate it. Use a
   named maintainer or `unassigned`; use `stable` only with sources and a review deadline.
7. Rebuild the catalog with `python3 scripts/build-knowledge-catalog.py` after
   changing concept metadata.
8. Run the required validation suite in [AGENTS.md](AGENTS.md).

For news, follow the [news editorial policy](governance/news-editorial-policy.md)
and the [news brief template](knowledge/templates/news-brief-template.md).

## Content checklist

- [ ] The concept is in `knowledge/`, is Markdown, and has the required OKF profile fields.
- [ ] The parent `index.md` lists the concept or child directory.
- [ ] Internal links are relative and resolve locally; external links use allowlisted `https://` domains.
- [ ] The page opens with a plain explanation and stays on one reader outcome.
- [ ] Commands have prerequisites, explanation, and nearby safety notes.
- [ ] Technical claims use official sources where appropriate.
- [ ] The generated catalog is current after metadata changes.
- [ ] The content is original or use is explicitly permitted and attributed.
- [ ] The change is recorded in `knowledge/log.md` or [CHANGELOG.md](CHANGELOG.md) when notable.

## License

By contributing original material under `knowledge/`, you license it under
[CC BY 4.0](LICENSES/README.md). Contributions to code, scripts, configuration,
and automation are licensed under the [MIT License](LICENSE).
