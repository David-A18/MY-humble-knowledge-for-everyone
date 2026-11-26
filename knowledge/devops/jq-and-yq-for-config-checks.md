---
type: Explanation
title: Choose jq or yq for JSON and YAML checks
description: Choose a CLI for structured configuration checks and identify which yq implementation your script requires.
tags: [devops, json, yaml, jq, yq]
status: draft
audience: Engineering learners and practitioners
maintainer: unassigned
sources:
  - id: jq-manual
    resource: https://github.com/jqlang/jq/blob/jq-1.8.1/docs/content/manual/manual.yml
    title: jq 1.8.1 manual source
  - id: go-yq
    resource: https://github.com/mikefarah/yq/blob/v4.47.2/README.md
    title: Mike Farah yq 4.47.2 documentation
  - id: python-yq
    resource: https://github.com/kislyuk/yq/blob/v3.4.3/README.rst
    title: Kislyuk yq 3.4.3 documentation
---

# Choose jq or yq for JSON and YAML checks

For a JSON API response, start with jq. It reads JSON and applies a filter
to extract or check a value. For a YAML configuration file, Mike Farah's
yq can read the file directly and run a similar-looking
expression.[^jq-manual][^go-yq]

## Choose the tool

| Situation | What to use |
| --- | --- |
| A command already emits JSON | Use jq directly. For CI assertions, `-e` makes a false or null last result unsuccessful.[^jq-manual] |
| The source is YAML and the check is simple | Use Mike Farah's yq. Its `-e` flag reports failure when the expression has no match or returns null or false.[^go-yq] |
| The source is YAML and you need an existing jq-specific filter | Convert the YAML with Mike Farah's yq using `-o=json`, then run jq. Another option is Kislyuk's yq, which converts YAML to JSON and passes the result to jq.[^go-yq][^python-yq] |

Both yq projects install a command named `yq`. Mike Farah's implementation
uses its own expression engine with syntax inspired by jq. Kislyuk's project
wraps jq and requires it to be installed. In shared scripts, name the
implementation and pin the version so teammates can install the same
tool.[^go-yq][^python-yq]

## Compare the same check in each format

Save this JSON example as `service.json`:

```json
{"service":{"replicas":2}}
```

Save the equivalent YAML as `service.yaml`:

```yaml
service:
  replicas: 2
```

```bash
jq -e '.service.replicas == 2' service.json
yq -e '.service.replicas == 2' service.yaml
```

What it does: each command checks the same field and prints `true` for this
example. Change the expected value to `3` to see the failure exit status.
The yq command here uses Mike Farah's implementation.[^jq-manual][^go-yq]

Use this read-only conversion when you need the parsed values in JSON.[^go-yq][^jq-manual]

```bash
yq -o=json '.' service.yaml | jq -e '.service.replicas == 2'
```

What it does: emits JSON for jq to read. The final check is still the same
assertion.[^go-yq][^jq-manual]

## Evidence and limits

On 26 November 2026, jq 1.8.1 and Mike Farah's yq v4.47.2 on Ubuntu 26.04
under WSL returned success for the direct checks and conversion. Both direct
checks returned failure for an expected value of `3`. The comparison with
Kislyuk's yq was based on its documentation.

## Related links

- [Validate Docker Compose configuration](docker-compose-config.md)
- [DevOps index](index.md)
- [Knowledge home](../index.md)

[^jq-manual]: [jq 1.8.1 manual source](https://github.com/jqlang/jq/blob/jq-1.8.1/docs/content/manual/manual.yml)
[^go-yq]: [Mike Farah yq 4.47.2 documentation](https://github.com/mikefarah/yq/blob/v4.47.2/README.md)
[^python-yq]: [Kislyuk yq 3.4.3 documentation](https://github.com/kislyuk/yq/blob/v3.4.3/README.rst)
