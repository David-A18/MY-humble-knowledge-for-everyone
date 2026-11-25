---
type: News Brief
title: GitHub Code Quality fails uploads in unsupported formats
description: The coverage upload action now fails when a report uses an unsupported format.
tags: [news, github-actions, code-quality]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
published: 2026-11-25
stale_after: 2027-02-25
sources:
  - id: announcement
    resource: https://github.blog/changelog/2026-11-23-code-coverage-uploads-now-flag-invalid-report-formats/
    title: GitHub Changelog on coverage upload validation
---

# GitHub Code Quality fails uploads in unsupported formats

## What happened

On 23 November 2026, GitHub announced that its Code Quality coverage upload
action now fails the upload step when the report uses an unsupported format.
The action expects Cobertura XML. GitHub lists availability for Team and
Enterprise Cloud repositories with Code Quality enabled.[^announcement]

## Why it matters

An upload could previously look successful in Actions while coverage was
missing from the pull request. The failure now points to the upload step, so
teams can distinguish a reporting problem from a failing test.[^announcement]

## What to do

Check the upload step in the workflow log. If it flags the format, configure
the test tool to produce Cobertura XML or convert the report before uploading.
Check that the upload points to the new file and that coverage appears on a
test pull request.

## Related links

- [GitHub Actions troubleshooting](../../../git/github-actions/common-solutions.md)
- [November 2026](index.md)
- [News](../../index.md)
- [Knowledge home](../../../index.md)

[^announcement]: [GitHub Changelog on coverage upload validation](https://github.blog/changelog/2026-11-23-code-coverage-uploads-now-flag-invalid-report-formats/)
