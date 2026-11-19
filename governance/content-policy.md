# Content and security policy

This policy says what may be merged into this repository and how the checks
enforce it. It protects readers, contributors, and anyone who runs an example.
The [repository gate](../.github/workflows/repository-gate.yml) runs every rule
on each pull request and push; the
[trusted content scan](../.github/workflows/trusted-content-scan.yml) re-runs the
policy and moderation rules with the default branch's own scripts and lists.

## What the repository accepts

The repository manages text: knowledge written in Markdown and small,
readable code examples.

| Location | Allowed files |
| --- | --- |
| `knowledge/` | Markdown (`.md`) only. Put code inside fenced code blocks. |
| `examples/` | Runnable lab files that knowledge pages link to, using text formats only: `.md`, `.py`, `.ts`, `.mjs`, `.json`, `.jsonl`, `.yaml`, `.yml`, `.tf`, `.hcl`, `.rego`, `.csv`, `.txt`, `.example`, `.gitignore`, and `Dockerfile`. |
| Everything else | The same text formats, plus `.jsonc`, `.toml`, `.sha256`, `CODEOWNERS`, `LICENSE`, and `.gitattributes`. |

Every file must be valid UTF-8 text. The checks reject:

- binary files, executables, archives, documents, images, audio, and video;
- names that hide another extension, such as `report.pdf.md`;
- shell scripts (`.sh`): show shell commands in Markdown code blocks instead;
- executable permission outside `scripts/`, symbolic links, and Git submodules;
- files over 1 MB, or Markdown in `knowledge/` over 100 KB;
- hidden Unicode that can disguise text or code: bidirectional controls in any
  file and zero-width characters in Markdown.

## Safe Markdown

Outside code blocks and inline code:

- **No images or embedded media.** Explain ideas in text, tables, or
  [Mermaid](https://mermaid.js.org/) diagrams.
- **No raw HTML**, except the harmless `<br>`, `<details>`, `<summary>`,
  `<kbd>`, `<sub>`, and `<sup>` without attributes.
- **Links must be safe:**
  - use `https://` (plain `http://` only for `localhost` and `example.com`);
  - no `javascript:`, `data:`, `file:`, or other schemes;
  - no URL shorteners, raw IP addresses, user information before the host
    (`https://trusted@evil.test`), or internationalized or punycode host names;
  - no direct links to executables, archives, or media downloads;
  - every host must be on the reviewed
    [domain allowlist](policy/allowed-link-domains.txt).

Hosts that serve anyone's content, such as video platforms, raw file hosts,
file-sharing sites, and paste sites, can never be allowed as a whole domain. A
maintainer approves each such link individually in the
[URL prefix allowlist](policy/allowed-link-prefixes.txt).

Code blocks are examples, so the link and HTML rules do not apply inside them.
Reviewers still read them.

## Respectful language

The [moderation scanner](../scripts/moderate-content.py) checks every text file
for profanity, explicit sexual language, and slurs in English, Spanish, and
Portuguese. It recognizes common disguises: accents, character substitutions
such as `0` for `o`, stretched letters, and letters split by spaces or dots.

The [blocked-term list](policy/blocked-terms.sha256) stores SHA-256 hashes, so the
repository does not display the words, and findings show only a masked form
such as `w***`. Maintainers add terms without committing plain text:

```bash
printf '%s\n' 'term' | python3 scripts/moderate-content.py --hash-terms profanity >> governance/policy/blocked-terms.sha256
```

What it does: normalizes the term the same way the scanner does and appends its
hash with a category (`profanity`, `sexual`, or `hate`).

A legitimate use that matches a blocked term, such as a quoted policy
definition, is recorded in
[moderation exceptions](policy/moderation-exceptions.txt) as a file path and the
term hash printed by the finding. Each exception needs a maintainer review.

## Why a pull request cannot switch the checks off

A pull request runs its own copy of the workflow and scripts, so it could edit a
checker or a list to make its own content pass. Three controls prevent that:

1. The **trusted content scan** runs after the gate, using the policy checker,
   moderation scanner, and lists from the default branch. It reads the pull
   request's files as data and never runs them. It publishes the
   `trusted-content-scan` commit status.
2. **CODEOWNERS** requires a maintainer review for every change, including
   changes to `scripts/`, `governance/policy/`, and `.github/`.
3. **Branch protection** requires the checks below before merging.

## Moderation and sanctions

When the trusted scan finds blocked language, it:

1. fails the `trusted-content-scan` status, which blocks the merge;
2. adds the `moderation-review` label to the pull request;
3. opens, or comments on, a `Moderation review: PR #<number>` issue that records
   the author, commit, files, lines, categories, and masked terms.

A maintainer then reviews the case:

1. **Confirm or dismiss.** A false positive gets an entry in moderation
   exceptions, and the issue is closed with an explanation.
2. **First confirmed case:** close the pull request, remove the content, and
   warn the author in the issue, linking this policy.
3. **Repeated or severe case** (hate speech, sexual content, harassment, or
   deliberate evasion such as split or disguised words): block the account from
   the repository or organization and keep the issue as the record.

A person, never automation alone, decides each sanction, because word lists
produce false positives. The open and closed `moderation-review` issues are the
record of each author's history.

## Maintainer settings checklist

Apply these repository settings once. They cannot be stored in files.

- [ ] Protect `main` and `develop`: require pull requests, a CODEOWNERS
  review, and up-to-date branches.
- [ ] Require these status checks: `Content policy and moderation`,
  `Secret scan`, `OKF structure and catalog`, `Links`, `Markdown lint`,
  `Issue templates and labels`, and `trusted-content-scan`.
- [ ] Enable GitHub secret scanning and push protection.
- [ ] Enable Dependabot security updates (version updates are configured in
  [dependabot.yml](../.github/dependabot.yml)).
- [ ] Set GitHub Actions to require approval before running workflows from
  first-time contributors.
- [ ] Create the `moderation-review` and `dependencies` labels, or sync them from
  [labels.yml](../.github/labels.yml).

## Local checks

Run the policy and moderation checks before opening a pull request:

```bash
python3 scripts/validate-repository-policy.py
python3 scripts/moderate-content.py
```

What it does: runs the same file, Markdown, link, and language rules as the
repository gate on your working tree.
