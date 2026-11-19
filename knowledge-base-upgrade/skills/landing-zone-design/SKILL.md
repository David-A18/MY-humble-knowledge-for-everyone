# Landing zone design

## Purpose

Use this skill when designing or reviewing the landing zone (the first screen and scroll of the home route) of the knowledge website. It keeps the design tied to real content, honest trust signals, and a measurable quality bar.

## Before you start

Read, in order:

1. [Design brief](../../features/knowledge-website/landing-zone/design-brief.md)
2. [Toolchain reference](../../features/knowledge-website/landing-zone/toolchain.md)
3. [Preflight and quality gates](../../features/knowledge-website/landing-zone/preflight.md)
4. [Website requirements](../../features/knowledge-website/requirements.md) and [content contract](../../features/knowledge-website/content-contract.md)

## Rules

- Present only real content. Read counts and topics from the derived catalog at build time; never hard-code corpus figures.
- Do not imply expert review. Almost every concept is `draft`; make the `status` vocabulary part of the visual language.
- Browsing, topic navigation, and the news link must work with no JavaScript. Only search may need it.
- Prefer CSS scroll-driven animations with an `IntersectionObserver` fallback. Never animate opacity.
- Honor reduced motion and `Save-Data`. Heavy media loads only after the first interaction, and a poster or static view is always complete on its own.
- Self-host fonts. Add no analytics, trackers, accounts, comments, or third-party embeds.
- Keep the route mapping in the content contract unless the owner approves a change.
- Do not commit images, video, or fonts to the knowledge-base repository. Build assets belong in the website repository.
- Do not invent source imagery. A hero film must come from real material, with AI limited to light and motion.
- Ask the owner before deciding: hero film, languages, visual identity, and typeface.

## Workflow

1. Run the preflight checklist. Stop and report any blocker, especially the Node version.
2. Confirm the open decisions with the owner. Record the answers in the website repository's design guide.
3. Define design tokens first: type scale, spacing, colour for light and dark, and the trust-status labels.
4. Build the static hero and the topic, news, and search entry points as plain Astro and CSS.
5. Add scroll-driven motion with the fallback, then test reduced motion.
6. Only if a film is chosen, follow the film steps in the toolchain reference and review the generated clips before use.
7. Run the quality gates: build, type check, Playwright over HTTP, Lighthouse, accessibility scan. Take screenshots at desktop and phone width.
8. Record exactly what ran and at which evidence level. Do not claim reader testing.

## Done criteria

- Lighthouse meets 90 for performance, 95 for accessibility, and 90 for best practices on a served build.
- No serious or critical accessibility violations on the landing page.
- No horizontal overflow at 390 px wide, and keyboard reaches search and topic links.
- No-JavaScript and reduced-motion views are complete.
- Trust labels, the licence link, and the source commit are visible.
- The evidence record names the checks that ran and the limits that remain.

## Related links

- [Skill index](../README.md)
- [Landing zone design pack](../../features/knowledge-website/landing-zone/README.md)
- [Evidence levels](../../instructions/evidence-levels.md)
- [Back to root index](../../../README.md)
