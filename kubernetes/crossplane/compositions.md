# Crossplane compositions

## Purpose

Use this page to design Crossplane platform APIs with Composite Resource Definitions, composite resources, composition functions, composition revisions, and local rendering.

Compositions are where Crossplane becomes a platform-engineering tool. A platform team defines a small API that users can request, then implements that API with managed resources, ordinary Kubernetes resources, and function logic.

## Composition model

| Layer | Owner | Responsibility |
| --- | --- | --- |
| Composite Resource Definition | Platform team | Defines the API group, kind, scope, versions, validation, and allowed request shape. |
| Composite resource | Application, service, or platform consumer | Requests an instance of the platform API. |
| Composition | Platform team | Selects a function pipeline that turns an XR into composed resources. |
| Composition Function | Platform team or package maintainer | Generates, patches, transforms, validates, or enriches desired resources. |
| Composed resources | Crossplane and Kubernetes controllers | Reconcile external infrastructure or cluster resources. |

In Crossplane v2, namespaced XRs are the default model and a composition can compose ordinary Kubernetes resources as well as Crossplane managed resources.

## Example platform API

The user-facing request should be small and intent-focused:

```yaml
apiVersion: platform.example.com/v1alpha1
kind: WebApplication
metadata:
  name: demo
  namespace: default
spec:
  image: nginx:stable-alpine
  replicas: 2
```

What it does: asks for an application by intent. The platform implementation can decide labels, Service ports, security defaults, resource requests, network policy, and optional infrastructure.

## Define the XRD

```yaml
apiVersion: apiextensions.crossplane.io/v2
kind: CompositeResourceDefinition
metadata:
  name: webapplications.platform.example.com
spec:
  scope: Namespaced
  group: platform.example.com
  names:
    kind: WebApplication
    plural: webapplications
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
                image:
                  type: string
                replicas:
                  type: integer
                  minimum: 1
                  maximum: 5
                  default: 1
              required:
                - image
```

What it does: creates a namespaced `WebApplication` API and restricts user input to a small schema.

### Validate the XRD

```bash
kubectl apply --dry-run=server -f webapplication-xrd.yaml
kubectl apply -f webapplication-xrd.yaml
kubectl get xrds
```

What it does: validates the XRD, installs it, and checks that the definition exists.

## Install a composition function

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Function
metadata:
  name: function-patch-and-transform
spec:
  package: xpkg.crossplane.io/crossplane-contrib/function-patch-and-transform:v0.8.2
```

What it does: installs the Patch and Transform function package so a Composition can generate resources from an XR.

```bash
kubectl apply -f function.yaml
kubectl get functions.pkg.crossplane.io -w
```

What it does: installs the function and waits for it to report health.

> [!IMPORTANT]
> Function versions have independent release cycles. Pin a tested version and verify compatibility with your Crossplane release before production use.

## Create a pipeline composition

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: webapplication-basic
spec:
  compositeTypeRef:
    apiVersion: platform.example.com/v1alpha1
    kind: WebApplication
  mode: Pipeline
  pipeline:
    - step: create-resources
      functionRef:
        name: function-patch-and-transform
      input:
        apiVersion: pt.fn.crossplane.io/v1beta1
        kind: Resources
        resources:
          - name: deployment
            base:
              apiVersion: apps/v1
              kind: Deployment
              metadata:
                namespace: default
              spec:
                selector:
                  matchLabels:
                    app: placeholder
                template:
                  metadata:
                    labels:
                      app: placeholder
                  spec:
                    containers:
                      - name: application
                        image: nginx:stable-alpine
                        ports:
                          - containerPort: 80
            patches:
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.name
                toFieldPath: metadata.name
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.namespace
                toFieldPath: metadata.namespace
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.name
                toFieldPath: spec.selector.matchLabels.app
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.name
                toFieldPath: spec.template.metadata.labels.app
              - type: FromCompositeFieldPath
                fromFieldPath: spec.image
                toFieldPath: spec.template.spec.containers[0].image
              - type: FromCompositeFieldPath
                fromFieldPath: spec.replicas
                toFieldPath: spec.replicas
          - name: service
            base:
              apiVersion: v1
              kind: Service
              metadata:
                namespace: default
              spec:
                selector:
                  app: placeholder
                ports:
                  - name: http
                    port: 80
                    targetPort: 80
            patches:
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.name
                toFieldPath: metadata.name
                transforms:
                  - type: string
                    string:
                      type: Format
                      fmt: "%s-service"
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.namespace
                toFieldPath: metadata.namespace
              - type: FromCompositeFieldPath
                fromFieldPath: metadata.name
                toFieldPath: spec.selector.app
```

What it does: maps one `WebApplication` XR into a Deployment and Service.

## Create an XR

```yaml
apiVersion: platform.example.com/v1alpha1
kind: WebApplication
metadata:
  name: demo
  namespace: default
spec:
  image: nginx:stable-alpine
  replicas: 2
```

What it does: creates an instance of the platform API. Crossplane runs the Composition pipeline and creates the composed Kubernetes resources.

### Inspect composed resources

```bash
kubectl get webapplications.platform.example.com -n default
kubectl describe webapplication demo -n default
kubectl get deployments,services,pods -n default
```

What it does: checks XR readiness and confirms the generated resources exist.

## Design rules

- Keep the platform API small and stable.
- Hide provider-specific details unless users must choose them.
- Version APIs when breaking changes are needed.
- Test rendering and reconciliation before exposing a composition broadly.
- Decide how secrets and connection details flow to workloads.
- Prefer namespaced APIs for tenant-facing abstractions.
- Use schema enums, defaults, and validation to prevent invalid requests early.
- Keep functions deterministic and reviewable.
- Treat the XRD as the contract and the Composition as implementation.
- Use composition revisions deliberately for rollout and rollback behavior.
- Avoid exposing every cloud-provider field as a platform API field.

## Composition revisions

Crossplane creates revisions when Compositions change. XRs can automatically follow the latest revision or pin to a manual revision policy.

Use automatic updates for low-risk APIs and early development. Use manual update policies when a composition change may alter production infrastructure.

## Render and test before rollout

### Render locally

```bash
crossplane composition render \
  xr.yaml \
  composition.yaml \
  functions.yaml
```

What it does: runs the composition function pipeline locally and prints the resources Crossplane would produce.

> [!NOTE]
> Rendering improves reviewability but does not replace testing against real provider APIs, cloud permissions, quotas, and eventual consistency.

### Recommended development loop

```text
Edit XRD, Composition, or Function
        |
YAML, policy, and server-side schema validation
        |
Local composition render
        |
Kind or local integration test
        |
Sandbox cloud integration test
        |
Pull request
        |
GitOps promotion
```

## Platform API checklist

- [ ] The XRD exposes user intent, not provider internals.
- [ ] Required fields are minimal and validated.
- [ ] Defaults, enums, and constraints prevent common bad requests.
- [ ] Composed resources use explicit provider configs.
- [ ] Destructive lifecycle behavior is documented.
- [ ] Connection details and secrets have a clear flow.
- [ ] Composition rendering is part of CI.
- [ ] A sandbox reconciliation test exists before production promotion.

## Related links

- [Crossplane](README.md)
- [Managed resources and lifecycle](managed-resources-and-lifecycle.md)
- [Production, GitOps, and operations](production-gitops-and-operations.md)
- [Crossplane references](references.md)
- [Crossplane composition documentation](https://docs.crossplane.io/latest/composition/compositions/)
- [Composite Resource Definitions](https://docs.crossplane.io/latest/composition/composite-resource-definitions/)
- [Crossplane CLI command reference](https://docs.crossplane.io/cli/latest/command-reference/)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
