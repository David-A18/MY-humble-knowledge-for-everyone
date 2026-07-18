# Custom resources and CRDs

## Purpose

Use this page to understand Kubernetes custom resources, CustomResourceDefinitions, and operators.

## Concepts

| Concept | Meaning |
| --- | --- |
| Custom resource | Extension object stored through the Kubernetes API. |
| CustomResourceDefinition | API object that defines a new custom resource type. |
| Controller | Process that watches resources and reconciles desired state. |
| Operator | Controller pattern that encodes operational knowledge for an application or platform. |

## Design rules

- A CRD stores and validates API objects, but does not create behavior by itself.
- Behavior comes from a controller that watches the custom resource.
- Version CRDs carefully because schema changes affect stored objects and clients.
- Treat finalizers with care; broken controllers can leave resources stuck during deletion.

## Related links

- [Crossplane](../applications-and-tools/crossplane.md)
- [Kubernetes custom resources documentation](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
- [CRD task documentation](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)
- [Back to Kubernetes core objects](README.md)
- [Back to Kubernetes index](../README.md)
- [Back to root index](../../README.md)
