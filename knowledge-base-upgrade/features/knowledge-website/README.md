# Git-backed knowledge website

## Purpose

Specify a separate, public reading site for the canonical [OKF knowledge bundle](../../../knowledge/index.md). The website renders an exact revision of this repository's `main` branch as static pages. Git remains the content source of truth; the site owns presentation, search output, redirects, and deployment.

Status: Local website project scaffolded; public GitHub repository, host, and domain remain to be selected
Audience: Website implementers and knowledge-base maintainers
Maintainer: Unassigned
Design input: Read-only Claude Code Opus 5.5 architecture reviews on 2026-09-26; these are design reviews, not runtime or reader-test evidence

## Documents

| Document | Use it for |
| --- | --- |
| [Requirements](requirements.md) | Reader journeys, first-release boundaries, and acceptance criteria. |
| [Architecture](architecture.md) | Repository responsibilities, rendering stack, update workflow, and security boundaries. |
| [Content contract](content-contract.md) | Snapshot format, inclusion, metadata, URL, asset, and link rules. |
| [Rollout](rollout.md) | Repository setup, validation, deployment gate, recovery, and reader testing. |

The decision to launch before independent reader testing is recorded in [ADR-0005](../../../knowledge/decision-records/adr-0005-git-backed-reading-site.md). [ADR-0004](../../../knowledge/decision-records/adr-0004-machine-readable-discovery.md) still requires the website to consume canonical Markdown and the derived catalog.

## Repository boundary

This directory contains the source-side specification. The separate local website project holds code and operational instructions. When published as a GitHub repository, it will reference this specification at the pinned source revision rather than copying knowledge prose or maintaining competing requirements.

## Related links

- [Feature index](../README.md)
- [Upgrade hub](../../README.md)
- [Root repository index](../../../README.md)
