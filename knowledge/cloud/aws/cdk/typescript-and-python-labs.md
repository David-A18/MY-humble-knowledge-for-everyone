---
type: Tutorial
title: Equivalent TypeScript and Python CDK labs
description: Synthesize the same encrypted, private, versioned S3 bucket in both languages.
tags:
- cloud
- cdk
status: draft
maturity: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
- id: cdk-testing
  resource: https://docs.aws.amazon.com/cdk/v2/guide/testing.html
  title: CDK testing
- id: s3-bucket-construct
  resource: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.Bucket.html
  title: S3 Bucket construct
---

# Equivalent TypeScript and Python CDK labs

## Purpose

Synthesize the same encrypted, private, versioned S3 bucket in both languages.

Sources reviewed: 2026-10-29. See the [validation record](../../../../knowledge-base-audit.md) for executed checks and unexecuted runtime labs.

## Versions and files

Examples pin `aws-cdk-lib==2.275.0` / `aws-cdk-lib: 2.275.0` and `constructs==10.8.1`. TypeScript tooling pins CDK CLI 2.1146.1 and tsx 4.23.15. Use Node 24 and Python 3.13. See [TypeScript files](examples/typescript/index.md) and [Python files](examples/python/index.md).[^cdk-testing][^s3-bucket-construct]

The stack enables S3-managed encryption, blocks all public access, requires TLS through a bucket policy, enables versioning, and retains the bucket on removal. It creates no application objects and needs no AWS calls for basic synthesis/assertions.

## TypeScript

```bash
cd examples/typescript
pnpm install --ignore-scripts
pnpm test
pnpm synth
```

What it does: installs exact direct dependencies, checks security assertions, and writes a local cloud assembly. Record the generated lockfile for reproducible transitive versions. No deploy command is part of this step.

## Python

```bash
cd examples/python
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python test_stack.py
.venv/bin/python app.py
```

What it does: runs equivalent checks in an isolated environment and synthesizes the same stack. On Windows use `.venv/Scripts/python.exe`. The jsii runtime also requires Node on PATH.

## Compare results

Inspect `cdk.out/KbDocsLab.template.json` from both directories. The bucket properties, TLS-deny policy, and retention attributes should match. Generated metadata can vary with tool configuration; compare the actual infrastructure contract instead of ignoring every difference.

## Cleanup

Delete only generated example `cdk.out`, build, and virtual-environment directories when finished. Cloud deployment is an optional separate exercise in the deployment chapter; the examples deliberately use retention to protect any bucket that is deployed.

## Related links

- [CDK testing](https://docs.aws.amazon.com/cdk/v2/guide/testing.html)
- [S3 Bucket construct](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.Bucket.html)
- [Back to parent index](index.md)
- [Back to major area](../../index.md)
- [Back to root index](../../../../README.md)

[^cdk-testing]: [CDK testing](https://docs.aws.amazon.com/cdk/v2/guide/testing.html).
[^s3-bucket-construct]: [S3 Bucket construct](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_s3.Bucket.html).
