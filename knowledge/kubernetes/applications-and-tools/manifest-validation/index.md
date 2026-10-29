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

## Related links

- [Runnable example files](examples/index.md)

- [Back to parent index](../index.md)
- [Back to root index](../../../../README.md)
