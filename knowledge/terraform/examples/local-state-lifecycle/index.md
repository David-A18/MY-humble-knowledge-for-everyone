# Terraform local state lifecycle

Use this directory for the local Terraform exercise and its support files.

## Tutorial

- [Local state lifecycle](local-state-lifecycle.md) - Initialize, validate,
  plan, apply, inspect, change, and destroy local Terraform state safely.

## Support files

- [main.tf](main.tf) - Uses `terraform_data` so the exercise creates no cloud resources.
- [.gitignore](.gitignore) - Excludes state, plans, cache, and override files.
- [validate-lab.py](validate-lab.py) - Repeats create/update, plan status/input behavior, destruction, and empty-state checks in a temporary local copy.

Continue from the [local Kubernetes walkthrough](../../../cross-topic-guides/local-deployment-learning-path.md) after cleaning up its cluster. The two exercises manage separate targets; this Terraform state does not own Kubernetes resources.

[Back to Terraform examples](../index.md) | [Back to Terraform index](../../index.md) | [Back to knowledge index](../../../index.md)
