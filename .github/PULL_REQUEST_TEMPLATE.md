# Pull request checklist

## Summary

- What changed?
- Why is it useful?

## Content checklist

- [ ] Knowledge changes are Markdown files under `knowledge/`; runnable lab files are text files under `examples/`.
- [ ] No images, video, binaries, archives, or executables are added.
- [ ] External links use `https://` and allowlisted domains; any new domain is added to `governance/policy/allowed-link-domains.txt` with a reason below.
- [ ] New knowledge directories include an `index.md`, and new pages are listed in their parent index.
- [ ] Pages open with a plain explanation and keep one reader outcome.
- [ ] Commands use fenced code blocks with language identifiers, and risky steps have warnings or rollback notes.
- [ ] News briefs follow the news editorial policy and have `published`, `sources`, and `stale_after`.

## New link domains

- None, or list each domain and why it is a trustworthy source.

## Validation

- [ ] I ran the checks in `AGENTS.md`, including the content policy and moderation scan.
- [ ] The repository gate and trusted content scan pass.
