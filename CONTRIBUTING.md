# Contributing

Thank you for improving this knowledge base. Read [AGENTS.md](AGENTS.md),
[context.md](context.md), and [instructions.md](instructions.md) before editing.

## Add or improve knowledge

1. Start from [knowledge/index.md](knowledge/index.md) and find the nearest parent `index.md`.
2. Choose one Diátaxis reader outcome and use the corresponding `type`.
3. Add complete OKF profile frontmatter and focused, original Markdown content.
4. Update the nearest parent index, related concepts, and `knowledge/log.md` for notable changes.
5. Add provenance and review metadata only when you can substantiate it.
6. Run the required validation suite in [AGENTS.md](AGENTS.md).

## Content checklist

- [ ] The concept is in `knowledge/` and has the required OKF profile fields.
- [ ] The parent `index.md` lists the concept or child directory.
- [ ] Internal links are relative and resolve locally.
- [ ] Commands have prerequisites, explanation, and nearby safety notes.
- [ ] Technical claims use official sources where appropriate.
- [ ] The content is original or use is explicitly permitted and attributed.
- [ ] The change is recorded in `knowledge/log.md` or [CHANGELOG.md](CHANGELOG.md) when notable.

## License

By contributing original material under `knowledge/`, you license it under
[CC BY 4.0](LICENSES/README.md). Contributions to code, scripts, configuration,
and automation are licensed under the [MIT License](LICENSE).
