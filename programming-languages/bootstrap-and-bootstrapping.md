# Bootstrap and bootstrapping

## Purpose

This article explains the two meanings developers usually intend when they say
`bootstrap`:

- `Bootstrap`, the frontend CSS and JavaScript toolkit.
- `bootstrapping`, the startup or setup process that prepares a project,
  application, or platform so the rest of the work can run.

## When to use this

- You see `Bootstrap` in HTML, CSS, package files, or frontend documentation.
- Someone says an app, project, environment, or infrastructure stack needs to
  be bootstrapped.
- You need to understand what startup code is responsible for before debugging
  a web application.

## Key ideas

| Concept | Meaning | Example |
| --- | --- | --- |
| `Bootstrap` | A frontend toolkit for layouts, components, utilities, and JavaScript behaviors. | `class="btn btn-primary"` |
| `bootstrap` as a verb | Initialize enough state, files, services, or configuration for something to work. | `npm install` before running a Node app. |
| Bootstrap CSS class | A predefined class that maps to existing Bootstrap styling. | `.container`, `.row`, `.col-md-6` |
| Bootstrap JavaScript plugin | Optional browser behavior for interactive components. | Modal, dropdown, tooltip, collapse, carousel. |
| Bootstrap infrastructure | Foundational resources needed before other automation can manage the system. | Remote Terraform state bucket, lock table, base IAM role. |

## Bootstrap as a frontend toolkit

`Bootstrap` with a capital `B` is a web frontend toolkit. It gives developers a
shared set of CSS classes and JavaScript components so common interface patterns
do not need to be written from scratch for every project.

Bootstrap commonly provides:

- layout primitives such as containers, rows, columns, gutters, and responsive
  breakpoints;
- styled content defaults for typography, tables, forms, and images;
- reusable components such as buttons, alerts, cards, navbars, dropdowns,
  modals, accordions, tabs, offcanvas panels, toasts, and tooltips;
- utility classes for spacing, display, flexbox, sizing, borders, colors,
  shadows, positioning, text, and visibility;
- optional JavaScript behavior for interactive components.

Bootstrap does not replace HTML, CSS, or JavaScript. It sits on top of them. You
still write HTML structure, choose meaningful content, wire application state,
and decide how the page should behave.

## What Bootstrap classes mean

When you see this:

```html
<button class="btn btn-primary">Save</button>
```

What it does: the browser renders a normal HTML `<button>`, then Bootstrap CSS
matches the `btn` and `btn-primary` classes and applies prebuilt button styles.
`btn` gives the generic button shape and spacing. `btn-primary` gives the
primary visual variant.

Bootstrap classes are usually small declarations of intent:

| Class | Plain meaning |
| --- | --- |
| `container` | Center content and give it responsive horizontal width limits. |
| `row` | Create a horizontal wrapper for grid columns. |
| `col` | Let an element behave like a grid column. |
| `col-md-6` | Use half the 12-column row width at the `md` breakpoint and above. |
| `d-flex` | Apply `display: flex`. |
| `gap-3` | Add a predefined gap between child items. |
| `mt-4` | Add a predefined top margin. |
| `text-center` | Center inline text. |
| `visually-hidden` | Keep content available to assistive technology while hiding it visually. |

## Layout example

```html
<div class="container">
  <div class="row g-3">
    <section class="col-12 col-md-6">
      <h2>Profile</h2>
      <p>Visible full width on small screens and half width on medium screens.</p>
    </section>

    <section class="col-12 col-md-6">
      <h2>Activity</h2>
      <p>Stacks below the first section on phones and sits beside it on wider screens.</p>
    </section>
  </div>
</div>
```

What it does: `container` centers the content, `row` creates the grid row,
`g-3` adds gutter spacing, `col-12` makes each section full width by default,
and `col-md-6` changes each section to half width at the medium breakpoint and
larger.

## JavaScript component example

Some Bootstrap components need JavaScript because they react to clicks, keyboard
events, focus, transitions, or page state.

```html
<button
  class="btn btn-primary"
  data-bs-toggle="modal"
  data-bs-target="#confirmModal"
>
  Open dialog
</button>

<div class="modal" id="confirmModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title fs-5">Confirm action</h2>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div class="modal-body">
        This action needs confirmation.
      </div>
    </div>
  </div>
</div>
```

What it does: Bootstrap's JavaScript listens for the `data-bs-toggle` and
`data-bs-target` attributes, finds the modal with `id="confirmModal"`, and
opens it when the button is clicked.

## How Bootstrap is loaded

There are two common ways to use Bootstrap.

### CDN

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
>
<script
  src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
></script>
```

What it does: the page downloads prebuilt Bootstrap CSS and JavaScript from a
CDN. This is convenient for demos, small pages, and learning.

> [!IMPORTANT]
> For production CDN usage, follow the official Bootstrap documentation for
> version pinning, Subresource Integrity attributes, and `crossorigin` handling.

### Package manager

```bash
npm install bootstrap@5.3.8
```

What it does: installs Bootstrap into a Node-based frontend project so the app's
build tool can import Bootstrap CSS, Sass, and JavaScript from dependencies.

Use this path when the application already has a bundler such as Vite, Webpack,
Parcel, or another frontend build pipeline.

## Bootstrapping as a startup process

`Bootstrapping` means preparing the minimum useful foundation so the next layer
can run.

In application code, bootstrapping often includes:

- reading environment variables;
- loading configuration;
- creating dependency containers;
- connecting to databases, queues, caches, or external APIs;
- registering routes, controllers, middleware, or handlers;
- running migrations or startup checks;
- starting the server process.

In project setup, bootstrapping often includes:

- creating the initial repository structure;
- generating `package.json`, `pyproject.toml`, `go.mod`, or equivalent metadata;
- installing dependencies;
- adding scripts for test, lint, build, and development;
- creating local configuration examples;
- proving the project can run with one documented command.

In infrastructure, bootstrapping often includes:

- creating the remote state backend for an IaC tool;
- creating the first deployment identity or access role;
- creating base networking or DNS zones;
- installing a platform controller before it can manage other resources;
- seeding secrets-management or configuration-management foundations.

## Why the word is reused

The word comes from the idea of a system doing enough initial work to help
itself continue. In software, that same idea appears at many layers:

| Layer | Bootstrapping means |
| --- | --- |
| Browser page | Load the CSS and JavaScript needed before components can render correctly. |
| Frontend app | Mount the root component and connect routing, state, and configuration. |
| Backend app | Initialize dependencies and start accepting requests. |
| Repository | Generate the first usable structure and install dependencies. |
| Infrastructure | Create the base resources needed before automation can manage everything else. |

## Bootstrap versus custom CSS

| Situation | Bootstrap is useful | Custom CSS may be better |
| --- | --- | --- |
| Prototype | You need a working interface quickly. | The visual direction is already strict and unique. |
| Internal tool | Consistent forms, tables, buttons, and layout matter more than brand originality. | The app has a mature internal design system. |
| Learning | You want to see common UI patterns without writing all CSS yourself. | You are specifically practicing raw CSS layout and styling. |
| Production app | You want stable defaults and predictable components. | You need minimal CSS size or highly custom interactions. |

## Common confusion

| Phrase | Usually means |
| --- | --- |
| `Add Bootstrap` | Install or link the Bootstrap frontend toolkit. |
| `Use Bootstrap classes` | Apply Bootstrap's predefined class names in HTML. |
| `Bootstrap the app` | Run initialization code before the app becomes usable. |
| `Bootstrap the project` | Create the starter files and dependency setup. |
| `Bootstrap the environment` | Prepare required local, cloud, or platform dependencies. |
| `Bootstrap Terraform` | Create state storage, locks, credentials, or base resources needed before normal Terraform runs. |

## Troubleshooting

| Symptom | Likely cause | Next step |
| --- | --- | --- |
| Bootstrap classes do nothing | Bootstrap CSS is not loaded or the URL is wrong. | Check the browser Network tab and confirm the CSS file returns `200`. |
| Grid does not behave responsively | Missing viewport meta tag or incorrect grid classes. | Add the viewport meta tag and verify breakpoint class names. |
| Modal or dropdown does not open | Bootstrap JavaScript bundle is missing. | Load `bootstrap.bundle.min.js` or import the needed JS plugin. |
| Tooltip or popover positioning is broken | Popper is missing when using separate JS files. | Use the Bootstrap bundle or load Popper before Bootstrap JS. |
| Custom CSS seems ignored | Bootstrap CSS is loaded after custom CSS or selectors are weaker. | Load custom CSS after Bootstrap and use focused selectors. |
| App fails during startup | Bootstrapping code cannot load config or connect to a required dependency. | Check environment variables, startup logs, and dependency health first. |

## Related links

- Official documentation: [Bootstrap getting started](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- Official documentation: [Bootstrap grid system](https://getbootstrap.com/docs/5.3/layout/grid/)
- Official documentation: [Bootstrap download and package managers](https://getbootstrap.com/docs/5.3/getting-started/download/)
- Back to programming languages index: [README.md](README.md)
- Back to root index: [../README.md](../README.md)
