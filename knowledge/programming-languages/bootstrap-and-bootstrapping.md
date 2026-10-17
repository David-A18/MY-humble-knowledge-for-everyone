---
type: "Explanation"
title: "Bootstrap and bootstrapping"
description: "Distinguish the Bootstrap web toolkit from bootstrapping a project or system, then choose the explanation you need."
tags: [programming-languages, bootstrap-and-bootstrapping]
status: draft
maturity: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
sources:
  - id: bootstrap-introduction
    resource: https://getbootstrap.com/docs/5.3/getting-started/introduction/
    title: Bootstrap - Get started
  - id: terraform-s3-backend
    resource: https://developer.hashicorp.com/terraform/language/backend/s3
    title: Terraform - S3 backend
  - id: rust-compiler-bootstrap
    resource: https://rustc-dev-guide.rust-lang.org/building/bootstrapping/what-bootstrapping-does.html
    title: Rust Compiler Development Guide - What bootstrapping does
  - id: aws-cdk-bootstrap
    resource: https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html
    title: AWS CDK - Bootstrapping
---

# Bootstrap and bootstrapping

## Purpose

The same word appears in several engineering conversations. Use this page to
identify what is being prepared before following instructions or debugging a
problem.

| Phrase you hear | Meaning in this context | Read next |
| --- | --- | --- |
| "Add Bootstrap to this page" | Use the **Bootstrap** frontend toolkit: its CSS classes and optional JavaScript components style and operate a web page.[^bootstrap-introduction] | [Bootstrap frontend toolkit](bootstrap-frontend-toolkit.md) |
| "Bootstrap this project" | Prepare the minimum files, dependencies, or configuration needed before normal work can start. | [Bootstrapping a system](bootstrapping-a-system.md) |
| "Bootstrap the infrastructure" | Prepare a prerequisite such as an S3 bucket before Terraform can use that bucket as its state backend.[^terraform-s3-backend] | [Bootstrapping a system](bootstrapping-a-system.md) |
| "Bootstrap the compiler" | Build a new compiler using an earlier compiler, then use the new one in later build stages.[^rust-compiler-bootstrap] | [Rust compiler bootstrapping](https://rustc-dev-guide.rust-lang.org/building/bootstrapping/what-bootstrapping-does.html) |
| "Run `cdk bootstrap`" | Prepare an AWS environment with resources that later AWS CDK deployments need.[^aws-cdk-bootstrap] | [AWS CDK bootstrapping](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html) |

The capital **B** often helps when people write about the toolkit, but spoken
language has no capitalization. Look at the surrounding task: a CSS class in
HTML points to the toolkit; a missing dependency or first-run setup points to
the general process. A compiler build or named CDK command points to its own
documented version of that process.

## A small example

An illustrative team says, "Bootstrap the dashboard before the demo." That
sentence alone is ambiguous. If they mean "make the buttons look consistent,"
they may be choosing the Bootstrap toolkit. If they mean "install dependencies
and create the first configuration file," they are bootstrapping the project.
The two tasks can both happen, but one does not perform the other.

Think of a toolkit as a box of prefabricated parts and bootstrapping as
preparing the workshop so work can begin. The analogy is only a memory aid:
software startup dependencies and browser styling have different failure
modes.

## Check your understanding

- What would you ask before acting on "bootstrap the app"?
- Does adding Bootstrap CSS classes to a page install the project's other
  dependencies or initialize its database?

## Official documentation for deeper study

- [Bootstrap getting started](https://getbootstrap.com/docs/5.3/getting-started/introduction/) defines the frontend toolkit and its first page.
- [Terraform S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3) assumes its state bucket already exists.
- [Rust compiler bootstrapping](https://rustc-dev-guide.rust-lang.org/building/bootstrapping/what-bootstrapping-does.html) shows a staged compiler build.
- [AWS CDK bootstrapping](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html) shows the resources CDK prepares before deployment.

## Related links

- [Bootstrap frontend toolkit](bootstrap-frontend-toolkit.md)
- [Bootstrapping a system](bootstrapping-a-system.md)
- [Back to programming languages](index.md)
- [Back to the knowledge base index](../index.md)

[^bootstrap-introduction]: [Bootstrap - Get started](https://getbootstrap.com/docs/5.3/getting-started/introduction/), source record `bootstrap-introduction`.
[^terraform-s3-backend]: [Terraform - S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3), source record `terraform-s3-backend`.
[^rust-compiler-bootstrap]: [Rust Compiler Development Guide - What bootstrapping does](https://rustc-dev-guide.rust-lang.org/building/bootstrapping/what-bootstrapping-does.html), source record `rust-compiler-bootstrap`.
[^aws-cdk-bootstrap]: [AWS CDK - Bootstrapping](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html), source record `aws-cdk-bootstrap`.
