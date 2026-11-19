# Landing zone design pack

## Purpose

Give the next design session everything it needs to design the landing zone of the knowledge website without re-deriving context: what the site must show, which tools a previous landing-page project used, what this repository allows, what has been checked, and what the owner still has to decide.

Status: Draft
Audience: The maintainer and AI agents starting the landing zone design
Page type: Hand-off index
Maintainer: Unassigned
Last substantive review: Not independently reviewed; written 2026-11-19
Applicable versions: Current repository structure on the `develop` branch
Validation evidence: Statically checked with the repository gate. Container tool versions were read on 2026-11-19. Nothing in the toolchain was run end to end for this knowledge base.
Known limitations: The reference project's code, skills, and documents were not available in this session. The toolchain pages rest on the maintainer's description. Reported measurements were not re-run.
Next review: When the website repository exists or the first design is drafted

## What "landing zone" means here

The landing zone is the first screen and first scroll of the website home route (`/`). The [content contract](../content-contract.md) maps `knowledge/index.md` to `/`. The recommended approach keeps that mapping: the designed landing zone sits above the rendered home index, so the route table does not change. The [design brief](design-brief.md) records this as an open decision.

## Documents

| Document | Use it for |
| --- | --- |
| [Knowledge spiral concept and build plan](spiral-concept-and-plan.md) | The chosen concept, the spiral-to-content mapping, interaction states, visual system, the role of Gemini video, and phased delivery. |
| [Design brief](design-brief.md) | The reader outcome, the real content to present, hard constraints, the quality bar, and the open decisions for the owner. |
| [Toolchain reference](toolchain.md) | The film, page, quality, and Claude Code tooling from the reference project, with what to adopt, adapt, or skip here. |
| [Preflight and quality gates](preflight.md) | What was verified in this container, what is missing, the pre-design checklist, and the proposed quality gates. |
| [Landing zone design skill](../../../skills/landing-zone-design/README.md) | A draft skill that makes a design session follow this pack. |

## How to start the design task

1. Read the [design brief](design-brief.md), then the [toolchain reference](toolchain.md).
2. Run the [preflight](preflight.md) checklist and resolve any blocker it lists.
3. Ask the owner for the open decisions in the brief that the preflight marks as blocking.
4. Design and build in the website repository, not here. This repository only holds text and cannot hold images, video, or fonts.
5. Record what was checked, and at which [evidence level](../../../instructions/evidence-levels.md), in the website repository's documents.

## Related links

- [Website plan](../README.md)
- [Requirements](../requirements.md)
- [Architecture](../architecture.md)
- [Rollout](../rollout.md)
- [Upgrade hub](../../../README.md)
- [Back to root index](../../../../README.md)
