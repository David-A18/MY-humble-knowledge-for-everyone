# Manifest comparison, drift, and regression testing

Use different checks for source changes, rendered configuration, live drift, and application behavior. A clean YAML diff does not prove a deployment works.

## Learning path

Read in order, or choose a task from the table.

| Guide | Use it for |
| --- | --- |
| [Concepts and tool selection](concepts-and-tool-selection.md) | Choose comparison, validation, and behavior checks. |
| [Rendered YAML comparison](rendered-yaml-comparison.md) | Compare Helm/Kustomize output semantically. |
| [Desired versus live drift](live-drift.md) | Interpret server-side comparisons and GitOps reconciliation. |
| [Schema and policy validation](schema-and-policy.md) | Reject invalid or forbidden configuration. |
| [Regression lab and CI](regression-lab-and-ci.md) | Catch a Service routing regression with behavioral checks. |

## Evidence and practice

The [routing lab](regression-lab-and-ci.md) now supplies checksum-pinned tools, eight actual source-tool checks and thirteen cluster assertions, including live diff statuses, a real Service failure/recovery, Chainsaw positive/negative runs and cleanup. Source-only and hosted execution are recorded in the lab; future hosted outcomes must still be read for the exact revision. The section remains draft material; Helm/GitOps integrations and independent reader/platform sessions remain follow-ups.

## Related links

- [Runnable example files](examples/index.md)

- [Back to parent index](../index.md)
- [Back to root index](../../../../README.md)
