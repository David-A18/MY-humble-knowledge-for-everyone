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
  - id: terraform-backend
    resource: https://developer.hashicorp.com/terraform/language/backend
    title: Terraform - Backend configuration
---

# Bootstrap and bootstrapping

## Purpose

The same word appears in two different engineering conversations. Use this
page to tell them apart before following instructions or debugging a problem.

| Phrase you hear | Usually means | Read next |
| --- | --- | --- |
| "Add Bootstrap to this page" | Use the **Bootstrap** frontend toolkit: its CSS classes and optional JavaScript components style and operate a web page.[^bootstrap-introduction] | [Bootstrap frontend toolkit](bootstrap-frontend-toolkit.md) |
| "Bootstrap this project" | Prepare the minimum files, dependencies, or configuration needed before normal work can start. | [Bootstrapping a system](bootstrapping-a-system.md) |
| "Bootstrap the infrastructure" | Create foundations, such as a state backend, that later automation depends on.[^terraform-backend] | [Bootstrapping a system](bootstrapping-a-system.md) |

The capital **B** often helps when people write about the toolkit, but spoken
language has no capitalization. Look at the surrounding task: a CSS class in
HTML points to the toolkit; a missing dependency or first-run setup points to
the general process.

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
- Does adding Bootstrap CSS install a project's dependencies or initialize
  its database?

## Official documentation for deeper study

- [Bootstrap getting started](https://getbootstrap.com/docs/5.3/getting-started/introduction/) defines the frontend toolkit and its first page.
- [Terraform backend configuration](https://developer.hashicorp.com/terraform/language/backend) shows one kind of setup dependency behind infrastructure bootstrapping.

## Related links

- [Bootstrap frontend toolkit](bootstrap-frontend-toolkit.md)
- [Bootstrapping a system](bootstrapping-a-system.md)
- [Back to programming languages](index.md)
- [Back to root index](../../README.md)

[^bootstrap-introduction]: [Bootstrap - Get started](https://getbootstrap.com/docs/5.3/getting-started/introduction/), source record `bootstrap-introduction`.
[^terraform-backend]: [Terraform - Backend configuration](https://developer.hashicorp.com/terraform/language/backend), source record `terraform-backend`.
