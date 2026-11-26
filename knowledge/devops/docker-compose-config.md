---
type: How-to Guide
title: Validate and troubleshoot Docker Compose configuration
description: Inspect merged Compose files, identify the source of interpolated values, and catch missing inputs before startup.
tags: [devops, docker, compose, troubleshooting]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: compose-install
    resource: https://github.com/docker/docs/blob/main/content/manuals/compose/install/_index.md
    title: Install Docker Compose
  - id: compose-config
    resource: https://github.com/docker/compose/blob/v2.39.4/cmd/compose/config.go
    title: Docker Compose v2.39.4 config command source
  - id: compose-merge
    resource: https://github.com/docker/docs/blob/main/content/manuals/compose/how-tos/multiple-compose-files/merge.md
    title: Merge Compose files
  - id: compose-interpolation
    resource: https://github.com/docker/docs/blob/main/content/manuals/compose/how-tos/environment-variables/variable-interpolation.md
    title: Docker Compose variable interpolation
  - id: compose-release
    resource: https://github.com/docker/compose/releases/tag/v2.39.4
    title: Docker Compose v2.39.4 release
---

# Validate and troubleshoot Docker Compose configuration

Use `docker compose config` to see the merged configuration Compose will
use. For example, if a service starts in the wrong mode, inspect the rendered
model to see whether the environment file, your shell, or an override file
supplied that value.[^compose-config][^compose-interpolation][^compose-merge]

## Prepare an example

Install Compose using Docker's instructions for your platform. Use a
disposable directory and the following three files. The example uses an
environment mapping for the service and a required interpolation
expression.[^compose-install][^compose-interpolation][^compose-merge]

### compose.yaml

```yaml
services:
  app:
    image: busybox:1.37
    environment:
      APP_MODE: "${APP_MODE:?set APP_MODE}"
```

### compose.override.yaml

```yaml
services:
  app:
    environment:
      LOG_LEVEL: debug
```

### review.env

```dotenv
APP_MODE=demo
```

## Validate and inspect

Run the following from the example directory, with `APP_MODE` unset in the
shell for the first pass. Specify the base file first and the override
second.[^compose-merge][^compose-interpolation]

```bash
docker compose --env-file review.env -f compose.yaml -f compose.override.yaml config -q
docker compose --env-file review.env -f compose.yaml -f compose.override.yaml config
```

What it does: the first command validates without printing the resolved
configuration. The second prints it for review. In this example, look for
`APP_MODE: demo` and `LOG_LEVEL: debug` in `app`'s environment. These
commands render the configuration without starting the service.[^compose-config][^compose-merge]

> [!WARNING]
> The rendered model can contain resolved environment values. Use synthetic
> values when sharing output and avoid publishing rendered configuration or
> interpolation input dumps that contain credentials.[^compose-config]

## Find why the result differs

| Observation | Check |
| --- | --- |
| `APP_MODE` has an unexpected value | Inspect the shell environment. Shell variables take precedence over values supplied via the environment file for interpolation.[^compose-interpolation] |
| A value is missing and validation fails | Supply a nonempty `APP_MODE` in the shell or interpolation file. The `:` in the required expression makes an empty value invalid too.[^compose-interpolation] |
| The override is missing or resolves a path unexpectedly | Review the `-f` order and the first file. Compose resolves paths relative to the base file in this merge workflow.[^compose-merge] |

For focused diagnosis with synthetic data, run the same Compose invocation
with `config --environment` to see the interpolation inputs. Use
`config --format json` if you want CI to assert a specific resolved field.
Passing configuration validation is one check before a separate startup and
health test.[^compose-config]

## Evidence and limits

On 26 November 2026, the checksum-verified Docker Compose v2.39.4 Linux
AMD64 binary ran in Ubuntu 26.04 under WSL in standalone form. The example
validated successfully, resolved both expected environment keys, honored
a shell override, and returned an error when the required input was absent.
The run exercised configuration rendering and did not start any
containers.[^compose-release]

## Related links

- [Development environments](development-environments/index.md)
- [DevOps index](index.md)
- [Knowledge home](../index.md)

[^compose-install]: [Install Docker Compose](https://github.com/docker/docs/blob/main/content/manuals/compose/install/_index.md)
[^compose-config]: [Docker Compose v2.39.4 config command source](https://github.com/docker/compose/blob/v2.39.4/cmd/compose/config.go)
[^compose-merge]: [Merge Compose files](https://github.com/docker/docs/blob/main/content/manuals/compose/how-tos/multiple-compose-files/merge.md)
[^compose-interpolation]: [Docker Compose variable interpolation](https://github.com/docker/docs/blob/main/content/manuals/compose/how-tos/environment-variables/variable-interpolation.md)
[^compose-release]: [Docker Compose v2.39.4 release](https://github.com/docker/compose/releases/tag/v2.39.4)
