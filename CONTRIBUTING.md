# Contributing

Thank you for improving `engineering-knowledge-base`. Contributions should make the repository easier to navigate, more accurate, or more useful during real operational work.

## Contribution principles

- Prefer practical guidance over broad theory.
- Keep articles focused on one task, concept, command family, or troubleshooting scenario.
- Use relative links for internal repository navigation.
- Link to official documentation for product behavior, limits, and command references.
- Do not include secrets, customer-specific data, private infrastructure details, or unverified claims.

## Article checklist

- [ ] File and directory names use lowercase kebab-case.
- [ ] The page has a clear purpose and audience.
- [ ] The page type is clear: tutorial, how-to, reference, explanation, troubleshooting, or ADR.
- [ ] Substantially reviewed operational pages include the review-information block from [instructions](instructions.md).
- [ ] Long pages include a table of contents.
- [ ] Commands use fenced code blocks with language identifiers.
- [ ] Runnable examples state tools, versions, permissions, starting state, expected result, and cleanup.
- [ ] Illustrative examples say they are illustrative before the code block.
- [ ] Risky operations include warnings or rollback notes.
- [ ] Internal links are relative and verified.
- [ ] External links use descriptive text and point to authoritative sources.
- [ ] The article links back to its parent index and the root `README.md`.

## Recommended article structure

1. Purpose
2. When to use it
3. Prerequisites
4. Procedure or explanation
5. Examples
6. Troubleshooting
7. Related links

Use the templates in [templates](templates/README.md) when starting new content.

## Pull request expectations

- Keep changes scoped.
- Update indexes when adding, moving, or removing pages.
- Update [GLOSSARY.md](GLOSSARY.md) when adding important new terms.
- Update [CHANGELOG.md](CHANGELOG.md) for meaningful structural or content additions.

## Maintenance and reader feedback

- Use the [maintenance review queue](maintenance-review-queue.md) for priority article reviews, blocked validation follow-ups, and reader-task testing.
- Use the [external evidence request checklist](external-evidence-request.md) before collecting AWS sandbox or reader-test evidence for blocked plan work.
- Use the [reader test facilitator guide](reader-test-facilitator-guide.md) to run KB-14 sessions consistently.
- Use the reader-test results issue form for KB-14 sessions and the Crossplane AWS S3 validation issue form for KB-04 sandbox runs. Keep issue-template labels declared in [.github/labels.yml](.github/labels.yml), then check live labels with `python3 scripts/check-github-labels.py --repo David-A18/MY-humble-knowledge-for-everyone` when `gh` is available.
- When a reader reports confusion or a blocked step, record the page, environment or version when relevant, expected result, actual result, and the smallest confusing term or instruction.
- Do not record unnecessary personal information about readers. Broad experience level is enough for knowledge-base improvement work.
