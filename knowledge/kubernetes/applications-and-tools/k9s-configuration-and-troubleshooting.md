---
type: How-to Guide
title: K9s configuration and troubleshooting
description: Configure K9s aliases, hotkeys, plugins, and read-only mode for daily use, and fix common K9s start-up and display problems.
tags: [kubernetes, k9s, troubleshooting]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
---

# K9s configuration and troubleshooting

Use this page to tune K9s for daily work and to fix it when it does not start or show what you expect. It is part of [K9s](k9s.md).

## Configuration that helps daily use

| Feature | File or command | Use it for |
| --- | --- | --- |
| Main config | `k9s info` then `config.yaml` | Find and tune K9s config locations and behavior. |
| Aliases | `$XDG_CONFIG_HOME/k9s/aliases.yaml` | Define short commands for frequently used resources or filtered views. |
| Context aliases | `$XDG_DATA_HOME/k9s/clusters/<cluster>/<context>/aliases.yaml` | Define aliases only for one cluster context. |
| Hotkeys | `$XDG_DATA_HOME/k9s/hotkeys.yaml` | Bind favorite views to shortcuts. |
| Plugins | `$XDG_CONFIG_HOME/k9s/plugins.yaml` | Add custom commands that run against selected resources. |
| Read-only mode | `k9s --readonly` or config | Disable modification commands for safer browsing. |

### Alias example

```yaml
aliases:
  pp: v1/pods
  dep: apps/v1/deployments
  apppods: pod app app=web
```

What it does: adds `:pp`, `:dep`, and `:apppods` as command-mode shortcuts.

### Hotkey example

```yaml
hotKeys:
  shift-0:
    shortCut: Shift-0
    description: View app Pods
    command: pod app app=web
  shift-1:
    shortCut: Shift-1
    description: View Deployments
    command: dp
```

What it does: creates shortcuts for a filtered Pod view and the Deployment view. Custom hotkeys appear in K9s help with `?`.

## Troubleshooting

| Symptom | Likely cause | Next step |
| --- | --- | --- |
| K9s opens the wrong cluster | Active kubeconfig context is not what you expected. | Start with `k9s --context <context>` or switch with `:ctx`. |
| A namespace or resource view is empty | Wrong namespace, filter still active, or RBAC does not allow list/watch. | Press `Esc`, clear filters, check `:ns`, and verify access with `kubectl auth can-i`. |
| Logs do not open | The selected resource has no logs, the Pod is gone, or container selection is needed. | Reopen `:pod`, select the current Pod, and use `d` to inspect restart state. |
| Edit does not work | `EDITOR` or `KUBE_EDITOR` is missing, or RBAC denies update/patch. | Set an editor and confirm permissions before retrying. |
| Metrics columns are empty | Metrics Server or metrics API is unavailable. | Check Metrics Server and use `kubectl top` as a second signal. |
| Shell does not open | The image has no shell, RBAC denies exec, or NodeShell is not enabled for node access. | Try another container, inspect permissions, or configure NodeShell only when needed. |

### Confirm access outside K9s

```bash
kubectl auth can-i list pods -n app
kubectl auth can-i get pods/log -n app
kubectl auth can-i update deployments -n app
```

What it does: checks whether your identity can list Pods, read Pod logs, and update Deployments in the `app` namespace.

## Related links

- [K9s](k9s.md)
- [Back to index](index.md)
