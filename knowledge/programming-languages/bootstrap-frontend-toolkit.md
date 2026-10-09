---
type: "Explanation"
title: "Bootstrap frontend toolkit"
description: "Understand how Bootstrap CSS classes and optional JavaScript components change an HTML page without replacing HTML, CSS, or application code."
tags: [programming-languages, bootstrap, frontend]
status: draft
maturity: draft
audience: "Beginning web learners and practitioners"
maintainer: "unassigned"
sources:
  - id: bootstrap-introduction
    resource: https://getbootstrap.com/docs/5.3/getting-started/introduction/
    title: Bootstrap - Get started
  - id: bootstrap-grid
    resource: https://getbootstrap.com/docs/5.3/layout/grid/
    title: Bootstrap - Grid system
  - id: bootstrap-modal
    resource: https://getbootstrap.com/docs/5.3/components/modal/
    title: Bootstrap - Modal component
  - id: bootstrap-download
    resource: https://getbootstrap.com/docs/5.3/getting-started/download/
    title: Bootstrap - Download and package managers
---

# Bootstrap frontend toolkit

## Purpose

Use this page when someone asks you to "add Bootstrap" to a web page. You
will learn what Bootstrap supplies, what your own HTML and application still
must supply, and how to recognize a missing stylesheet or JavaScript bundle.
The examples use the Bootstrap 5.3 documentation; check the official page for
the exact files and version used by your project.

## What it is

Bootstrap is a frontend toolkit. Its CSS supplies prepared layout, spacing,
and visual styles that your HTML selects with class names. Its optional
JavaScript supplies behavior for components such as modals and
dropdowns.[^bootstrap-introduction]

A class such as `btn` does not create a new HTML element. It is a label on an
ordinary element that Bootstrap's stylesheet matches. In the same way,
`data-bs-toggle` attributes can tell Bootstrap's JavaScript to operate a
component, but the JavaScript bundle must be loaded first.

Imagine a set of reusable building parts. A Bootstrap class selects a part;
the HTML still says what the part is and contains. The analogy stops at
accessibility and meaning: a styled `div` does not become a semantic
`button` just because it looks like one.

## One small layout

This is illustrative markup, not a claim that the repository rendered it.
Assume the Bootstrap 5.3 CSS is loaded using an official installation method
and the HTML page has the viewport meta tag described in the
[getting-started guide](https://getbootstrap.com/docs/5.3/getting-started/introduction/).

```html
<div class="container">
  <div class="row g-3">
    <section class="col-12 col-md-6">
      <h2>Profile</h2>
      <p>About this learner.</p>
    </section>
    <section class="col-12 col-md-6">
      <h2>Activity</h2>
      <p>What they studied recently.</p>
    </section>
  </div>
</div>
```

`container` limits and centers the content width; `row` holds grid
columns; `g-3` adds a gutter. Each `col-12` takes the full row by default,
while `col-md-6` gives it half the row from the medium breakpoint
upwards.[^bootstrap-grid]

Visual expectation:

```text
Narrow screen:       Medium and wider:
+---------------+    +---------+---------+
| Profile       |    | Profile | Activity|
+---------------+    +---------+---------+
| Activity      |
+---------------+
```

This sketch shows the relationship, not measured browser output. If both
sections stay unstyled, first check whether the Bootstrap CSS actually
loaded. If they do not change columns at the expected width, check the
viewport meta tag, grid classes, and the version's breakpoint definitions.

## CSS and JavaScript have different jobs

| Need | Bootstrap supplies | You still supply |
| --- | --- | --- |
| A styled button | CSS for `btn` and a variant such as `btn-primary`. | A real `<button>`, its label, and what clicking it does. |
| A responsive grid | Grid classes and breakpoint styles. | The content order, meaningful headings, and a layout that works for your users. |
| A modal | Component styles and JavaScript behavior, when the required bundle or plugin is loaded. | The dialog content, an accessible trigger, and application action after confirmation.[^bootstrap-modal] |

The official quick start shows CDN files with version-specific integrity
hashes. Copy the exact CSS and JavaScript links for the version you choose;
do not reuse an old integrity hash with a new file. Projects with a build
pipeline can install Bootstrap through a package manager instead.[^bootstrap-introduction][^bootstrap-download]

## Decide whether to use it

Bootstrap can speed up a prototype or a conventional application interface
when its established patterns match the design. If a product has a specific
design system or only needs a small amount of CSS, compare the cost of
adapting Bootstrap with writing those styles directly. The toolkit does not
choose product language, information architecture, or interaction design for
you.

## Check your understanding

- Which part styles a `btn` class: the browser alone or the loaded
  Bootstrap CSS?
- Why can a modal look styled but fail to open?
- What is the smallest browser check that would tell you whether the CSS file
  loaded?

## Official documentation for deeper study

- [Bootstrap getting started](https://getbootstrap.com/docs/5.3/getting-started/introduction/) shows the supported first-page setup.
- [Bootstrap grid system](https://getbootstrap.com/docs/5.3/layout/grid/) explains rows, columns, and breakpoints.
- [Bootstrap modal](https://getbootstrap.com/docs/5.3/components/modal/) documents a component that needs JavaScript behavior.
- [Bootstrap download](https://getbootstrap.com/docs/5.3/getting-started/download/) covers installation choices.

## Related links

- [Bootstrap and bootstrapping](bootstrap-and-bootstrapping.md)
- [Bootstrapping a system](bootstrapping-a-system.md)
- [Back to programming languages](index.md)
- [Back to knowledge index](../index.md)

[^bootstrap-introduction]: [Bootstrap - Get started](https://getbootstrap.com/docs/5.3/getting-started/introduction/), source record `bootstrap-introduction`.
[^bootstrap-grid]: [Bootstrap - Grid system](https://getbootstrap.com/docs/5.3/layout/grid/), source record `bootstrap-grid`.
[^bootstrap-modal]: [Bootstrap - Modal component](https://getbootstrap.com/docs/5.3/components/modal/), source record `bootstrap-modal`.
[^bootstrap-download]: [Bootstrap - Download and package managers](https://getbootstrap.com/docs/5.3/getting-started/download/), source record `bootstrap-download`.
