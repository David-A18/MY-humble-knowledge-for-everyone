---
type: "Explanation"
title: "K9s"
description: "Use this page to understand what K9s is, how to move around in it, and how to inspect common Kubernetes resources without typing every kubectl command manually."
tags: [kubernetes, applications-and-tools, k9s]
status: draft
audience: "Engineering learners and practitioners"
maintainer: "unassigned"
---

# K9s

## Purpose

Use this page to understand what K9s is, how to move around in it, and how to inspect common Kubernetes resources without typing every `kubectl` command manually.

## What K9s is

K9s is a terminal UI for Kubernetes. It uses the same kubeconfig, current context, namespaces, and RBAC permissions that `kubectl` uses, but presents resources in interactive tables with shortcuts for common actions.

It is useful for daily cluster inspection, workload debugging, log reading, context switching, namespace navigation, and quick operational checks. It does not replace Kubernetes fundamentals: each K9s view still maps back to Kubernetes API resources such as Pods, Deployments, Services, ConfigMaps, Secrets, Nodes, Events, and custom resources.

```text
kubeconfig context
  -> K9s terminal UI
  -> Kubernetes API resources
  -> interactive views, logs, describes, edits, shells, and dashboards
```

## When to use it

- You want a fast view of Pods, Deployments, Services, Nodes, and Events.
- You need to move between namespaces or contexts repeatedly.
- You want to follow logs or describe resources without copying long names.
- You are learning how Kubernetes resources relate to each other.
- You need a read-only operational view for production inspection.

## Prerequisites

- A working kubeconfig for the target cluster.
- Kubernetes RBAC permissions to list, get, watch, and optionally modify the resources you need.
- A terminal that supports 256-color output.
- `EDITOR` or `KUBE_EDITOR` set if you plan to edit resources from K9s.

> [!IMPORTANT]
> K9s can only show and modify what your Kubernetes identity is allowed to access. If a view is empty or an action fails, check your active context, namespace, and RBAC permissions before assuming the cluster is broken.

## Contents

- [Start K9s](#start-k9s)
- [Screen model](#screen-model)
- [Move around](#move-around)
- [Simple resource commands](#simple-resource-commands)
- [Inspect and see things](#inspect-and-see-things)
- [Filtering and searching](#filtering-and-searching)
- [Common workflows](#common-workflows)
- [Special views](#special-views)
- [Risky actions](#risky-actions)
- [Configuration that helps daily use](k9s-configuration-and-troubleshooting.md#configuration-that-helps-daily-use)
- [Troubleshooting](k9s-configuration-and-troubleshooting.md#troubleshooting)
- [Official documentation](#official-documentation)
- [Related links](#related-links)

## Start K9s

| Task | Command | When to use it |
| --- | --- | --- |
| Open K9s with the current kubeconfig context | `k9s` | Start from your default context and namespace. |
| Show CLI help | `k9s help` | Check the options supported by your installed version. |
| Show runtime information | `k9s info` | Find config paths, log paths, and runtime details. |
| Start in one namespace | `k9s -n <namespace>` | Focus on one application or team namespace. |
| Start in a specific view | `k9s -c pod` | Open directly in a resource view. |
| Start with a specific context | `k9s --context <context>` | Avoid changing context after launch. |
| Start in read-only mode | `k9s --readonly` | Inspect production while disabling modification commands. |

### Start safely in production

```bash
k9s --context prod --readonly
```

What it does: opens K9s against the `prod` kubeconfig context and disables modification commands such as edit, delete, and kill.

## Screen model

| Area | What it means | How to use it |
| --- | --- | --- |
| Header | Current cluster, context, namespace, and view state. | Confirm you are in the right cluster before taking action. |
| Resource table | Rows from the current Kubernetes API resource. | Move the cursor to the resource you want to inspect. |
| Status and menu area | Available shortcuts for the current view. | Use it as the first source for resource-specific actions. |
| Command mode | Resource, filter, and special-view commands. | Press `:` and type a command such as `pod`, `svc`, or `ctx`. |
| Filter mode | Search and narrowing inside a view. | Press `/` and type a filter. |

> [!TIP]
> Press `?` inside K9s whenever you are unsure. K9s actions can be view-specific, so the help screen is the safest way to confirm available keys in the current version and resource view.

## Move around

| Action | Key or command | What it does |
| --- | --- | --- |
| Show help | `?` | Opens the active keyboard shortcuts and view-specific actions. |
| Show resource aliases | `Ctrl-A` | Lists available resource aliases and API resources. |
| Open command mode | `:` | Lets you jump to resources and special views. |
| Leave command, filter, or current panel | `Esc` | Backs out of the active mode or returns to the previous view. |
| Quit K9s | `:q` or `Ctrl-C` | Exits K9s. |
| Move selection | Arrow keys or Vim-style movement keys | Moves through rows in the active table. |
| Select a row | `Space` | Marks a row for multi-resource actions where supported. |
| Select a range | `Space`, move, `Ctrl-Space` | Selects a range between the first selected row and current row. |

### Jump to Pods

```text
:pod
```

What it does: opens the Pod view. Press `Enter` after typing the command.

### Go back

```text
Esc
```

What it does: exits the current command or filter mode, or returns to the previous view when K9s has navigation history.

## Simple resource commands

K9s accepts Kubernetes resource names, plural names, short names, and K9s aliases in command mode. Use `Ctrl-A` to see the exact aliases available in your cluster and K9s version.

| Need | K9s command | Comparable `kubectl` idea |
| --- | --- | --- |
| Pods | `:pod` or `:po` | `kubectl get pods` |
| Deployments | `:deploy` or `:dp` | `kubectl get deployments` |
| ReplicaSets | `:rs` | `kubectl get replicasets` |
| StatefulSets | `:sts` | `kubectl get statefulsets` |
| DaemonSets | `:ds` | `kubectl get daemonsets` |
| Services | `:svc` | `kubectl get services` |
| Ingresses | `:ing` | `kubectl get ingress` |
| ConfigMaps | `:cm` | `kubectl get configmaps` |
| Secrets | `:sec` | `kubectl get secrets` |
| Namespaces | `:ns` | `kubectl get namespaces` |
| Nodes | `:node` or `:no` | `kubectl get nodes` |
| PersistentVolumeClaims | `:pvc` | `kubectl get pvc` |
| PersistentVolumes | `:pv` | `kubectl get pv` |
| Jobs | `:job` | `kubectl get jobs` |
| CronJobs | `:cj` | `kubectl get cronjobs` |
| CustomResourceDefinitions | `:crd` | `kubectl get crd` |
| Events | `:events` | `kubectl get events` |
| Contexts | `:ctx` | `kubectl config get-contexts` |

### Open Pods in one namespace

```text
:pod app
```

What it does: opens the Pod view scoped to the `app` namespace.

### Open Pods by label

```text
:pod app=web,env=prod
```

What it does: opens Pods matching the labels `app=web` and `env=prod`.

### Open Pods in another context

```text
:pod @staging
```

What it does: opens Pods in the `staging` context and switches the active K9s context.

> [!IMPORTANT]
> Context switching inside K9s changes the target cluster for later actions. Confirm the header before deleting, editing, scaling, restarting, or opening a shell.

## Inspect and see things

| Task | Shortcut or command | Use it when |
| --- | --- | --- |
| Describe selected resource | `d` | You need events, conditions, mounts, probes, image pull errors, or scheduler messages. |
| View selected resource YAML | `v` | You need to inspect the live API object without editing it. |
| Edit selected resource | `e` | You need an emergency live edit and have permission. |
| Show logs | `l` | You need container logs for the selected Pod or workload. |
| Open shell | `s` | You need an interactive shell in a selected Pod or enabled NodeShell context. |
| Toggle wide columns | `Ctrl-W` | You need extra columns similar to `kubectl get -o wide`. |
| Show error resources | `Ctrl-Z` | You want a focused error-state view. |
| Show saved screen dumps | `:screendump` or `:sd` | You need previously saved resource snapshots. |

### Describe a failing Pod

```text
:pod
d
```

What it does: opens the Pod view, then describes the selected Pod so you can inspect events, restart reasons, pull failures, scheduling problems, volume mounts, and probe failures.

### View live YAML

```text
v
```

What it does: opens the selected Kubernetes object as live YAML for inspection.

### Follow logs

```text
l
```

What it does: opens logs for the selected Pod or supported workload. If the Pod has multiple containers, K9s may prompt you to choose one.

> [!TIP]
> For crash loops, inspect both `d` for events and `l` for logs. Events often explain scheduling, image, probe, or volume failures that application logs cannot show.

## Filtering and searching

| Need | Command | Example |
| --- | --- | --- |
| Text filter | `/<filter>` | `/api` |
| Regex filter | `/<regex>` | `/api\|worker` |
| Inverse filter | `/! <filter>` | `/! completed` |
| Label filter | `/-l <selector>` | `/-l app=web` |
| Fuzzy find | `/-f <filter>` | `/-f paymn` |
| Filter from command mode | `:<resource> /<filter>` | `:pod /api` |

### Filter Pods by name

```text
/api
```

What it does: narrows the current resource table to rows matching `api`.

### Filter by label

```text
/-l app=web
```

What it does: narrows the current resource view to resources matching the `app=web` label selector.

## Common workflows

### Daily namespace check

```text
:ns
:pod app
:svc app
:events app
```

What it does: checks namespaces, Pods, Services, and Events around the `app` namespace.

### Deployment health check

```text
:dp app
d
:rs app
:pod app
```

What it does: starts from Deployments, describes the selected Deployment, then checks ReplicaSets and Pods in the same namespace.

### Application failure check

```text
:pod app
/! Running
d
l
```

What it does: filters out running Pods, describes a failing selected Pod, then opens its logs.

### Service routing check

```text
:svc app
d
:ep app
:pod app
```

What it does: inspects a Service, checks its Endpoints, then checks the backing Pods.

### Cluster pressure check

```text
:node
:pod all
Ctrl-W
:events all
```

What it does: checks Nodes, all Pods with wider columns, and all namespace events for pressure, scheduling, or eviction signals.

## Special views

| View | Command | What it helps with |
| --- | --- | --- |
| Pulses | `:pulses` or `:pu` | High-level dashboard of cluster health and resource state. |
| XRay | `:xray <resource> [namespace]` | Relationship view for resources such as Pods, Services, Deployments, ReplicaSets, StatefulSets, and DaemonSets. |
| RBAC views | `:role`, `:rolebinding`, `:clusterrole`, `:clusterrolebinding` | Permission and binding inspection. |

### Inspect deployment relationships

```text
:xray deploy app
```

What it does: opens an XRay view for Deployments in the `app` namespace so you can inspect related resources from one screen.

## Risky actions

| Action | Shortcut | Risk |
| --- | --- | --- |
| Edit resource | `e` | Changes live cluster state immediately after save. |
| Delete resource | `Ctrl-D` | Deletes the selected resource after confirmation. |
| Kill resource | `Ctrl-K` | Deletes immediately without the normal graceful path. |
| Open shell | `s` | Gives interactive access inside a container or, with NodeShell enabled, through a temporary node shell Pod. |

> [!WARNING]
> Prefer `k9s --readonly` for production inspection when you do not intend to change anything. Do not use `Ctrl-K` unless you understand that it is equivalent to an immediate delete path.

## Related pages

Configuration and troubleshooting have their own page:

- [K9s configuration and troubleshooting](k9s-configuration-and-troubleshooting.md) - Configure K9s aliases, hotkeys, plugins, and read-only mode for daily use, and fix common K9s start-up and display problems.

## Official documentation

- [K9s documentation](https://k9scli.io/)
- [K9s commands](https://k9scli.io/topics/commands/)
- [K9s installation](https://k9scli.io/topics/install/)
- [K9s aliases](https://k9scli.io/topics/aliases/)
- [K9s hotkeys](https://k9scli.io/topics/hotkeys/)
- [K9s plugins](https://k9scli.io/topics/plugins/)
- [K9s configuration](https://k9scli.io/topics/config/)
- [K9s RBAC](https://k9scli.io/topics/rbac/)

## Related links

- [Kubernetes daily usage commands](../commands/daily-usage.md)
- [Kubernetes common commands](../commands/common-commands.md)
- [Kubernetes troubleshooting](../troubleshooting/index.md)
- [Back to Kubernetes applications and tools](index.md)
- [Back to Kubernetes index](../index.md)
- [Back to root index](../../../README.md)
