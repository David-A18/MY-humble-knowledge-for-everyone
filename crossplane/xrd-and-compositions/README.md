# XRDs and Compositions

## Purpose

Explain what XRDs are, how they work, how to define them, how users call them, and how they compare with Terraform modules.

## Short answer

XRDs are not Terraform modules.

| Terraform module | Crossplane XRD and Composition |
| --- | --- |
| A reusable HCL package called during `terraform plan` and `terraform apply`. | A Kubernetes API and controller-backed implementation reconciled continuously. |
| The module input variables define the interface. | The XRD OpenAPI schema defines the interface. |
| The module resources define the implementation. | The Composition defines the implementation. |
| Terraform records mappings in state. | Kubernetes stores desired state, and Crossplane/provider controllers update status. |
| Changes happen when Terraform runs. | Changes are reconciled continuously by controllers. |

The closest Crossplane equivalent to a Terraform module is the pair of an XRD plus one or more Compositions. The XRD is the API contract. The Composition is the implementation behind that contract.

## What an XRD does

An XRD, or `CompositeResourceDefinition`, defines a new Kubernetes API type for composite resources.

For example, this XRD creates a new API:

```yaml
apiVersion: apiextensions.crossplane.io/v2
kind: CompositeResourceDefinition
metadata:
  name: platformdatabases.platform.example.org
spec:
  group: platform.example.org
  scope: Namespaced
  names:
    kind: PlatformDatabase
    plural: platformdatabases
  versions:
  - name: v1alpha1
    served: true
    referenceable: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              engine:
                type: string
                enum:
                - postgres
                - mysql
              size:
                type: string
                enum:
                - small
                - medium
              region:
                type: string
            required:
            - engine
            - size
            - region
```

What it does: creates a Kubernetes API where users can create `PlatformDatabase` resources in namespaces.

After applying it, check the XRD:

```bash
kubectl apply -f xrd-platformdatabase.yaml
kubectl get xrd
kubectl describe xrd platformdatabases.platform.example.org
```

What it does: verifies Crossplane accepted the XRD and established the generated API.

## How users call an XRD

Users do not call the XRD object directly. They create an XR, which is an instance of the API the XRD defines.

```yaml
apiVersion: platform.example.org/v1alpha1
kind: PlatformDatabase
metadata:
  namespace: payments
  name: orders
spec:
  engine: postgres
  size: small
  region: eu-west-1
  crossplane:
    compositionRef:
      name: platformdatabase-aws-small
```

Apply it:

```bash
kubectl apply -f database-orders.yaml
kubectl get platformdatabases -n payments
kubectl describe platformdatabase orders -n payments
```

What it does: creates a composite resource. Crossplane selects a Composition and creates the lower-level resources that satisfy the request.

## What a Composition does

A Composition tells Crossplane how to turn an XR into composed resources.

Example Composition structure:

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: platformdatabase-aws-small
  labels:
    provider: aws
    size: small
spec:
  compositeTypeRef:
    apiVersion: platform.example.org/v1alpha1
    kind: PlatformDatabase
  mode: Pipeline
  pipeline:
  - step: patch-and-transform
    functionRef:
      name: function-patch-and-transform
    input:
      apiVersion: pt.fn.crossplane.io/v1beta1
      kind: Resources
      resources:
      - name: metadata-secret
        base:
          apiVersion: v1
          kind: Secret
          type: Opaque
          stringData:
            engine: postgres
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.engine
          toFieldPath: stringData.engine
```

What it does: defines a Composition pipeline that uses a function to create resources from an XR. This simplified example composes a Kubernetes `Secret`; real platform database Compositions usually include provider managed resources such as subnet groups, security groups, database instances, users, and connection-detail secrets.

For namespaced XRs, do not hard-code `metadata.namespace` in namespaced composed resource templates. Crossplane places composed namespaced resources in the XR namespace.

> [!IMPORTANT]
> Crossplane v2 Compositions can compose any Kubernetes resource, but Crossplane must have RBAC permissions to create and manage the resource kinds used in the Composition.

## Composition selection

An XR can choose a Composition explicitly:

```yaml
spec:
  crossplane:
    compositionRef:
      name: platformdatabase-aws-small
```

Or select by labels:

```yaml
spec:
  crossplane:
    compositionSelector:
      matchLabels:
        provider: aws
        size: small
```

What it does: lets platform teams publish multiple implementations for the same API. For example, `PlatformDatabase` could have AWS, Azure, dev, production, small, and large Compositions.

## Composition revisions

Crossplane creates Composition revisions when a Composition changes. XRs can either automatically use newer revisions or stay pinned.

```yaml
spec:
  crossplane:
    compositionUpdatePolicy: Manual
```

What it does: prevents an existing XR from automatically switching to the newest Composition revision.

Use this when Composition changes may affect production infrastructure and you want controlled rollout.

## Designing useful XRDs

Good XRDs hide implementation detail without hiding the decisions the application team must own.

| Design question | Good API choice |
| --- | --- |
| Should users choose exact cloud resource names? | Usually no. Let the platform own naming and tagging unless integration requires a stable name. |
| Should users choose region? | Yes, if data residency, latency, or cost depends on it. Otherwise default it in Composition. |
| Should users choose instance class? | Often no. Expose sizes such as `small`, `medium`, and `large`. |
| Should users choose network IDs? | Usually no. Select networks from environment or namespace policy. |
| Should users choose deletion behavior? | Only if the organization has a clear retention model. |

Keep the API stable and platform-owned. Change implementation details inside Compositions when possible.

## Common XRD fields

| Field | Purpose |
| --- | --- |
| `spec.group` | API group for the new resource, such as `platform.example.org`. |
| `spec.names.kind` | User-facing kind, such as `PlatformDatabase`. |
| `spec.names.plural` | Plural resource name, such as `platformdatabases`. |
| `spec.scope` | Whether XRs are `Namespaced` or `Cluster` scoped. |
| `spec.versions` | Served API versions and schemas. |
| `schema.openAPIV3Schema` | Validation schema for user-provided fields. |

## Common Composition fields

| Field | Purpose |
| --- | --- |
| `spec.compositeTypeRef` | Connects the Composition to an XR API version and kind. |
| `spec.mode` | Use `Pipeline` for function-based Compositions. |
| `spec.pipeline` | Ordered function steps. |
| `functionRef.name` | References the installed Function to call. |
| `input` | Function-specific configuration, such as Patch and Transform resources. |
| `patches` | Maps fields between the XR and composed resources. |

## Troubleshooting XRDs and Compositions

| Symptom | Check | Likely cause |
| --- | --- | --- |
| `kubectl get <plural>` fails | `kubectl get xrd` | XRD is not established or API name is different. |
| XR stays `Synced=False` | `kubectl describe <xr-kind> <name>` | Composition error, invalid patch, function error, or missing RBAC. |
| XR stays `Ready=False` | `crossplane beta trace ...` | One or more composed resources are not ready. |
| Managed resource fails | `kubectl describe <managed-kind> <name>` | Provider credentials, cloud permissions, quota, region, or invalid provider field. |
| Composition is not selected | Inspect `spec.crossplane.compositionRef` or selector labels | `compositeTypeRef` does not match the XRD API version and kind, or selector labels do not match. |

## Related links

- [Crossplane Compositions](https://docs.crossplane.io/latest/composition/compositions/)
- [Crossplane XRDs](https://docs.crossplane.io/latest/composition/composite-resource-definitions/)
- [Crossplane composite resources](https://docs.crossplane.io/latest/composition/composite-resources/)
- [Terraform modules](https://developer.hashicorp.com/terraform/language/modules)
- [Crossplane examples](../examples/README.md)
- [Back to Crossplane index](../README.md)
- [Back to root index](../../README.md)
