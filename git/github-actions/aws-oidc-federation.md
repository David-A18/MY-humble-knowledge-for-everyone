# AWS OIDC federation

## Purpose

Use this page to authenticate GitHub Actions to AWS without storing long-lived AWS access keys as repository secrets.

## Workflow shape

1. The workflow grants `id-token: write`.
2. GitHub issues an OIDC token for the job.
3. AWS IAM validates the token against an IAM OIDC provider and role trust policy.
4. AWS STS returns temporary role credentials.
5. The job uses those temporary credentials for AWS commands.

## Minimal workflow pattern

```yaml
permissions:
  id-token: write
  contents: read
```

What it does: allows the job to request an OIDC token while keeping repository content access read-only.

## Trust-policy reminders

- Restrict the repository, branch, tag, or environment in the `sub` condition.
- Keep `aud` set to the expected AWS STS audience.
- Use separate roles for separate deployment environments.
- Avoid granting broad administrator permissions to CI roles.

## Related links

- [OIDC fundamentals](../../security/identity-federation/oidc-fundamentals.md)
- [IAM OIDC provider and STS web identity](../../cloud/aws/security/iam-oidc-provider-and-sts-web-identity.md)
- [GitHub Actions security, secrets, and permissions](security-secrets-and-permissions.md)
- [GitHub OIDC documentation](https://docs.github.com/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [Back to GitHub Actions](README.md)
- [Back to Git index](../README.md)
- [Back to root index](../../README.md)
