# Landing zone design brief

## Purpose

State what the landing zone has to do, using only facts from this repository, so the design starts from the real content and the real constraints.

Status: Draft
Audience: Designers and AI agents designing the knowledge website home page
Page type: Design brief
Maintainer: Unassigned
Last substantive review: Not independently reviewed; written 2026-11-19
Applicable versions: Corpus figures from `scripts/report-knowledge-health.py` on 2026-11-19
Validation evidence: Statically checked. Figures were read from the health report; no reader testing has happened.
Known limitations: Corpus figures change with every content update. Never copy them into the design as constants.
Next review: When the first design is drafted

## Reader outcome

One outcome: within the first screen, a learner or practitioner understands what this knowledge base is, can start a topic or a goal, and can see how much to trust a page.

The audience is public engineering learners and practitioners, as set in the [requirements](../requirements.md).

## What the landing zone can honestly present

| Fact | Value on 2026-11-19 | Design consequence |
| --- | --- | --- |
| Concepts | 284 across 16 areas plus root pages (about 192,000 words) | Show the real count at build time, read from the derived catalog. |
| Largest areas | Kubernetes 94, Cloud 63, Git 20, Cross-topic guides 19, Terraform 16 | Lead with these topics; many other areas are small. |
| Trust status | 281 `draft`, 3 `stable`, 0 independently verified | Do not market the content as reviewed or authoritative. Show the status vocabulary and let readers judge. |
| Sourced concepts | 155 of 284 | Present sources as a visible signal, never as a blanket claim. |
| News | 4 briefs in the first weekly roundup, each with a freshness date | News is a distinct, dated entry point with its own listing and feed. |
| Learning paths | 10 expanded paths in `knowledge/index.md` | Candidate "start here" cards. |
| Goal-based starts | 6 goals, such as recover a Git mistake or diagnose a Kubernetes workload | Candidate task-first entry points. |

The honest trust position is the strongest design constraint. Nearly all concepts are `draft`, so a landing zone that implies expert review would be wrong. A good landing zone makes the trust labels part of the visual language.

## Must-haves

These come from the [requirements](../requirements.md) and apply to the landing zone as well as to inner pages.

1. Topic navigation from the index hierarchy, reachable without JavaScript.
2. A search entry point. Search is the only feature that may need JavaScript. Browsing must work without it.
3. Visible trust and attribution: `status` vocabulary, the CC BY 4.0 licence link, and the source commit.
4. A news entry point.
5. Keyboard access, narrow-screen layout, and no serious or critical automated accessibility violations.
6. No accounts, comments, analytics, CMS, live GitHub reads, or AI answers in this release.

## Repository constraints for the design work

- This repository accepts text only. No images, video, audio, fonts, or archives can be committed here. Visual assets belong in the website repository.
- Markdown in `knowledge/` cannot contain images, embedded media, or raw HTML. The landing zone is website code, so it is not bound by that rule, but it must render the Markdown content as authored.
- Markdown links in this repository must use a host on the [reviewed allowlist](../../../../governance/policy/allowed-link-domains.txt).
- The website renders a pinned commit of this repository. The design must not depend on content that exists only in the website.
- Fonts are self-hosted. No Google Fonts requests.

## Techniques to carry over

The [toolchain reference](toolchain.md) lists each technique with the reason it was chosen. The ones that suit a reading site are:

- Astro static output with almost no JavaScript, which matches the [architecture](../architecture.md).
- CSS scroll-driven animations as the first choice for motion, with an `IntersectionObserver` fallback.
- A rule that animations never change opacity, so content cannot be left invisible.
- Respect for reduced motion and `Save-Data`, and a complete experience with no JavaScript.
- Self-hosted variable fonts.
- A typed, build-time checked file for landing copy and theme settings, so a missing field or translation fails the build.
- A numeric quality bar instead of opinion.

## Quality bar

The reference project's bar was Lighthouse performance at least 90, accessibility at least 95, and best practices at least 90. Adopt it as the starting target. The [requirements](../requirements.md) add retrieval, link, route, trust-label, and accessibility criteria that also apply.

## Open decisions for the owner

| # | Decision | Recommended default | Blocks |
| --- | --- | --- | --- |
| 1 | Hero film or static hero | Static hero with CSS motion. A film needs real source imagery, which this knowledge base does not have. | The whole hero design |
| 2 | Landing zone and `/` | Keep `knowledge/index.md` as `/` and place the landing zone above it, so the content contract is unchanged. | Route and contract |
| 3 | Languages | English only, matching the corpus. The reference project had EN/ES routes. | Copy and routing |
| 4 | Name, logo, and visual identity | None exists in the repository. The owner supplies or approves them. | Visual design |
| 5 | Website repository and host | Not chosen. See ROADMAP Phase 5. Design can start before the host is chosen. | Deployment only |
| 6 | Typeface | Reuse the reference pairing (a width-variable display face plus a compact sans) only if the owner likes the look. | Visual design |
| 7 | Colour schemes | Light and dark, following the system setting. | Theme tokens |

Also note that ROADMAP says Phases 1 and 2 must be complete before website design starts. Phase 2 still has one open maintainer item: applying the repository settings in the [content policy checklist](../../../../governance/content-policy.md#maintainer-settings-checklist).

## Related links

- [Landing zone design pack](README.md)
- [Toolchain reference](toolchain.md)
- [Preflight and quality gates](preflight.md)
- [Website plan](../README.md)
- [Upgrade hub](../../../README.md)
- [Back to root index](../../../../README.md)
