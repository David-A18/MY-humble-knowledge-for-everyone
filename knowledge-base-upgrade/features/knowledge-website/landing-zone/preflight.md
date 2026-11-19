# Landing zone preflight and quality gates

## Purpose

Say what was verified for the landing zone design work, what is still missing, and which checks the website repository should run before anyone sees the design.

Status: Draft
Audience: The maintainer and AI agents about to design or build the landing zone
Page type: Checklist and reference
Maintainer: Unassigned
Last substantive review: Not independently reviewed; written 2026-11-19
Applicable versions: Container tool versions and npm registry versions on 2026-11-19
Validation evidence: Locally executed in a disposable cloud container. A minimal Astro page was built, loaded over HTTP in Chromium through Playwright, and audited with Lighthouse. This proves the toolchain starts. It is not a design and says nothing about the real landing zone.
Known limitations: Versions are what the registry offered on 2026-11-19, not a pin. Pin them when the website repository is created. The film chain, Flow, and the maintainer's PC were not checked.
Next review: When the website repository is created

## Verified in the cloud container

| Item | Result on 2026-11-19 |
| --- | --- |
| Node and npm | Node 22.23.5, npm 10.9.9 |
| Python and Git | Python 3.13.18, Git 2.43.0 |
| FFmpeg | 6.1.1 |
| Playwright and Chromium | Preinstalled; `require('playwright')` works and Chromium is at the preinstalled path |
| GPU | None (no NVIDIA tool, no `/dev/dri`) |
| npm registry | Reachable. Latest versions seen: Astro 7.4.13, `@astrojs/check` 0.9.12, Pagefind 1.6.0, `@playwright/test` 1.65.1, Lighthouse 13.6.0, `@fontsource-variable/archivo` 5.3.0, `@fontsource/inter-tight` 5.3.0 |
| Astro build | Installed and built a one-page site in under a second |
| Fonts | Archivo variable has a width-axis stylesheet (`wdth.css`), so the expanded-capitals look is available. Inter Tight loaded. Both are self-hosted by the build. |
| Scroll-driven CSS | `animation-timeline: view()` is supported in the container's Chromium |
| Phone overflow | None at 390 px wide on the smoke page |
| Lighthouse | Runs against a local server. The smoke page scored 100 for performance, 94 for accessibility, and 96 for best practices. |

Two things the smoke test taught:

- **Astro 7.4.13 requires Node 22.23.4 or newer.** The container clears that by one patch version. Check the maintainer's PC and the CI image before anything else, and read the [Astro installation guide](https://docs.astro.build/en/install-and-setup/) for the current range.
- **Serve the built site over HTTP in tests.** Opening `dist/index.html` through `file://` blocked the font loads and logged console errors. Over HTTP there were none.

The smoke page failed the 95 accessibility bar only because it had no `<main>` landmark, and logged a favicon 404 as a console error. Both are cheap to avoid, and they show that the Lighthouse gate catches real problems.

## Not available or not decided

| Gap | Effect | Who resolves it |
| --- | --- | --- |
| Website repository does not exist | Nothing to scaffold into; no pinned versions, no CI | Owner, per ROADMAP Phase 5 |
| Host and domain not chosen | Deployment adapter and origin are undecided; design can still start | Owner |
| Reference project files not in this session | The skills `hero-film` and `site-qa`, the film player, the pipeline scripts, and the guides cannot be ported, only re-planned | Owner supplies the files or attaches the repository |
| No GPU in the container | Real-ESRGAN, RIFE, ComfyUI, Qwen, and Wan cannot run here | Run on the maintainer's PC if a film is chosen |
| Flow needs the owner's sign-in | An agent cannot start a Flow render alone | Owner |
| ROADMAP Phase 2 settings item | Branch protection and secret scanning settings are still pending | Maintainer |
| Open design decisions | Hero film, route relationship, languages, identity, typeface, colours | Owner; see the [design brief](design-brief.md) |

## Pre-design checklist

1. Confirm Node 22.23.4 or newer on every machine that will build the site.
2. Confirm the open decisions in the [design brief](design-brief.md) that block design: hero film or static, route relationship, languages, and visual identity.
3. Regenerate the corpus figures with the command below and use them as inputs, never as constants.
4. Create or choose the website repository, then pin dependency versions in its lockfile.
5. If a hero film is chosen, confirm the PC tools and the Flow sign-in before planning keyframes. If none is chosen, skip the whole film chain.

```bash
python3 scripts/report-knowledge-health.py
python3 scripts/build-knowledge-catalog.py --check
```

## Proposed quality gates for the website repository

These adapt the reference project's gates. They are a proposal until the website repository exists and runs them.

| Gate | Purpose | Notes |
| --- | --- | --- |
| Landing data check | Landing copy and theme match a schema; a missing field fails the build | Replaces the multi-client data check |
| `astro check` | Type errors | Install `@astrojs/check` |
| Unit tests with `node --test` | Any custom script logic | Only if custom logic exists |
| Playwright, served over HTTP | No-JavaScript browsing works; reduced motion shows no movement; no horizontal overflow at 390 px; keyboard reaches search and topic links; screenshots at desktop and phone width | Keep tests few and meaningful |
| Lighthouse | Performance 90 or more, accessibility 95 or more, best practices 90 or more | Run on a served build |
| Automated accessibility scan | No serious or critical violations on the home, topic, concept, and search templates | Required by the [requirements](../requirements.md) |
| Retrieval cases against the search index | At least one expected page in the first ten results per case | Required by the [requirements](../requirements.md) |
| Link and route checks | Every internal link and fragment resolves | Required by the [requirements](../requirements.md) |
| Smoothness check | Glide and exact frame, with a simulated wheel | Only with a hero film |

## Proposed website repository layout

The [rollout](../rollout.md) already lists `README.md`, `docs/README.md`, `docs/deployment.md`, `docs/operations.md`, source, tests, `content-lock.json`, `redirects.json`, and workflows. For the landing zone, add:

- a landing data file and its schema, for copy and theme settings;
- `docs/DESIGN-GUIDE.md` for tokens, type, spacing, and the trust-label language;
- `docs/ANIMATION-GUIDE.md` for motion rules, including no opacity animation and reduced-motion behavior;
- `docs/TOOLCHAIN.md` for pinned versions and the tool health check;
- launch configurations for the dev server, and for ComfyUI only if a film is chosen.

## Questions for the owner at the start of the design session

1. Static hero or scroll-driven film?
2. Is the landing zone placed above the rendered home index, keeping `/` as the home route?
3. English only, or English and Spanish?
4. Is there a name, logo, or colour direction to follow?
5. Which repository will hold the site, and may the design start before the host is chosen?
6. Can the reference project's files be supplied?

## Related links

- [Landing zone design pack](README.md)
- [Design brief](design-brief.md)
- [Toolchain reference](toolchain.md)
- [Evidence levels](../../../instructions/evidence-levels.md)
- [Upgrade hub](../../../README.md)
- [Back to root index](../../../../README.md)
