# OpenID Connect (OIDC) on AWS and Amazon EKS

> A detailed study guide covering OIDC fundamentals, OAuth 2.0, JWTs, AWS IAM federation, Amazon EKS IRSA, EKS Pod Identity, human authentication to EKS, IAM Identity Center, CI/CD federation, security rules, troubleshooting, and practical examples.

**Last reviewed:** 18 July 2026
**Audience:** Cloud engineers, platform engineers, DevOps engineers, Kubernetes administrators, security engineers, and AWS architects.

---

## Table of contents

1. [Executive summary](#1-executive-summary)
2. [What OIDC means](#2-what-oidc-means)
3. [Authentication, authorization, and federation](#3-authentication-authorization-and-federation)
4. [OIDC compared with OAuth 2.0, SAML, and AWS IAM](#4-oidc-compared-with-oauth-20-saml-and-aws-iam)
5. [OIDC actors and components](#5-oidc-actors-and-components)
6. [Discovery metadata and JWKS](#6-discovery-metadata-and-jwks)
7. [OIDC tokens and JWT structure](#7-oidc-tokens-and-jwt-structure)
8. [Important token claims](#8-important-token-claims)
9. [The Authorization Code flow with PKCE](#9-the-authorization-code-flow-with-pkce)
10. [How token validation works](#10-how-token-validation-works)
11. [What an IAM OIDC provider is](#11-what-an-iam-oidc-provider-is)
12. [How AWS STS web identity federation works](#12-how-aws-sts-web-identity-federation-works)
13. [IAM trust policies versus permissions policies](#13-iam-trust-policies-versus-permissions-policies)
14. [Creating a generic IAM OIDC provider](#14-creating-a-generic-iam-oidc-provider)
15. [The three identity problems around Amazon EKS](#15-the-three-identity-problems-around-amazon-eks)
16. [EKS workload identity with IRSA](#16-eks-workload-identity-with-irsa)
17. [Complete IRSA setup lab](#17-complete-irsa-setup-lab)
18. [How IRSA works internally](#18-how-irsa-works-internally)
19. [IRSA trust-policy patterns](#19-irsa-trust-policy-patterns)
20. [EKS Pod Identity](#20-eks-pod-identity)
21. [IRSA versus EKS Pod Identity](#21-irsa-versus-eks-pod-identity)
22. [Human authentication to EKS with an external OIDC provider](#22-human-authentication-to-eks-with-an-external-oidc-provider)
23. [OIDC authentication and Kubernetes RBAC](#23-oidc-authentication-and-kubernetes-rbac)
24. [IAM-based EKS access and access entries](#24-iam-based-eks-access-and-access-entries)
25. [OIDC and AWS IAM Identity Center](#25-oidc-and-aws-iam-identity-center)
26. [Identity Center trusted token issuers](#26-identity-center-trusted-token-issuers)
27. [GitHub Actions OIDC federation with AWS](#27-github-actions-oidc-federation-with-aws)
28. [Other OIDC examples](#28-other-oidc-examples)
29. [OIDC security rules and best practices](#29-oidc-security-rules-and-best-practices)
30. [Common mistakes and misconceptions](#30-common-mistakes-and-misconceptions)
31. [Troubleshooting](#31-troubleshooting)
32. [Architecture decision guide](#32-architecture-decision-guide)
33. [Hands-on learning exercises](#33-hands-on-learning-exercises)
34. [Production-readiness checklist](#34-production-readiness-checklist)
35. [Glossary](#35-glossary)
36. [Official references](#36-official-references)

---

# 1. Executive summary

**OIDC** stands for **OpenID Connect**. It is an identity and authentication protocol built on top of the OAuth 2.0 authorization framework.

OIDC lets an application or platform verify the identity represented by a signed token. The token normally contains claims such as:

- Who issued it: `iss`
- Who or what it represents: `sub`
- Which application or service may accept it: `aud`
- When it expires: `exp`
- Optional identity attributes such as email, username, tenant, or groups

An **OIDC provider** is an identity system or token issuer that publishes:

1. An issuer URL.
2. OIDC discovery metadata.
3. Public signing keys through a JWKS endpoint.
4. Endpoints for authorization, token issuance, and sometimes user information.
5. Signed tokens representing authenticated identities.

In AWS, the term **IAM OIDC provider** has a precise meaning. It is an IAM resource that records trust in an external OIDC issuer. It does not usually host users or perform login itself. Instead, it tells AWS IAM and AWS Security Token Service (STS):

> Tokens from this issuer may be considered when a role trust policy explicitly allows them.

A complete AWS OIDC federation design normally has four layers:

```text
Identity source or workload
        |
        | obtains signed OIDC token
        v
OIDC issuer
        |
        | token contains iss, sub, aud, exp...
        v
AWS IAM role trust policy
        |
        | authorizes sts:AssumeRoleWithWebIdentity
        v
AWS STS
        |
        | issues short-lived AWS credentials
        v
AWS API authorization through the role's permissions policy
```

Around Amazon EKS, OIDC appears in several different contexts:

| Requirement | Typical solution |
|---|---|
| A pod needs AWS permissions | EKS Pod Identity or IRSA |
| A human needs direct OIDC authentication to the Kubernetes API | EKS external OIDC identity-provider association |
| A human signs in to AWS accounts through a corporate identity provider | IAM Identity Center with SAML 2.0 and SCIM |
| An external application propagates a workforce identity into supported AWS applications | Identity Center trusted token issuer |
| GitHub Actions needs AWS credentials without stored access keys | IAM OIDC federation and STS |
| An IAM Identity Center user accesses EKS through an AWS role | IAM Identity Center + IAM role + EKS access entry |

These mechanisms solve related but different identity problems. A large part of mastering OIDC on AWS is learning not to confuse them.

---

# 2. What OIDC means

**OIDC = OpenID Connect**

The name can be understood as follows:

- **OpenID**: a standardized way to represent and verify an identity.
- **Connect**: applications connect to an identity provider instead of implementing authentication independently.

OIDC is defined by the OpenID Foundation. It extends OAuth 2.0 with identity-specific concepts, especially the **ID token**.

OAuth 2.0 mainly provides delegated authorization:

> “This client may access a protected API with these permissions.”

OIDC adds authentication:

> “This user or workload was authenticated by this issuer, and this token represents that identity.”

A common simplified comparison is:

```text
OAuth 2.0:
    What may this client do?

OIDC:
    Who authenticated?

Authorization policy:
    What may that authenticated identity do in this system?
```

OIDC does not replace every identity protocol. For example, SAML 2.0 remains widely used for browser-based enterprise workforce federation, including the standard external identity-provider integration for AWS IAM Identity Center.

---

# 3. Authentication, authorization, and federation

## 3.1 Authentication

Authentication verifies identity.

Examples:

- A user proves control of an account with a password and MFA.
- A pod proves its Kubernetes service-account identity with a signed token.
- A GitHub Actions job proves its repository, branch, workflow, or environment context with a GitHub-issued token.
- A command-line application signs in through a browser and receives an ID token.

The result of authentication is normally an identity such as:

```text
alice@example.com
```

or:

```text
system:serviceaccount:payments:invoice-api
```

or:

```text
repo:example-org/payments-api:ref:refs/heads/main
```

## 3.2 Authorization

Authorization determines what the identity is allowed to do.

Examples:

- An IAM policy permits `s3:GetObject`.
- A Kubernetes Role permits `get`, `list`, and `watch` on Pods.
- A RoleBinding grants a Kubernetes group the permissions of a Role.
- An EKS access policy grants an IAM role namespace-scoped administrative access.
- An IAM Identity Center permission set grants read-only access to an AWS account.

Authentication without authorization gives an identity no useful permissions. Authorization without reliable authentication may give permissions to the wrong identity.

## 3.3 Federation

Federation allows one security domain to trust identities authenticated by another domain.

Examples:

- AWS trusts a GitHub-issued OIDC token.
- AWS trusts a Kubernetes service-account token from an EKS cluster.
- EKS trusts an ID token from Okta, Keycloak, or Microsoft Entra ID.
- IAM Identity Center trusts SAML assertions from an external workforce identity provider.

Federation avoids creating and maintaining a separate long-lived credential for every external workload or user.

---

# 4. OIDC compared with OAuth 2.0, SAML, and AWS IAM

| Technology | Main purpose | Typical artifact | Common AWS use |
|---|---|---|---|
| OAuth 2.0 | Delegated authorization | Access token | Authorizing an application to call an API |
| OIDC | Authentication and identity on top of OAuth 2.0 | ID token, commonly a JWT | Workload federation, application login, EKS user authentication |
| SAML 2.0 | Enterprise browser-based identity federation | XML assertion | External IdP integration with IAM Identity Center |
| SCIM 2.0 | User and group provisioning | REST resources | Synchronizing users/groups into IAM Identity Center |
| AWS IAM | AWS authorization and identity controls | Policies, roles, principals | Authorizing AWS API operations |
| AWS STS | Temporary AWS credentials | Access key, secret key, session token | Role assumption and federation |
| Kubernetes RBAC | Kubernetes API authorization | Role, ClusterRole, bindings | Authorizing users and service accounts inside a cluster |

## 4.1 OIDC is not the same as OAuth 2.0

OIDC uses OAuth 2.0 mechanisms, but OAuth 2.0 alone does not standardize an authenticated user identity.

OIDC adds:

- The `openid` scope.
- ID tokens.
- Standard identity claims.
- UserInfo behavior.
- Discovery metadata.
- Rules for validating the identity represented by the token.

## 4.2 OIDC is not the same as SAML

Both can federate identity, but their formats and ecosystems differ.

| OIDC | SAML |
|---|---|
| JSON and JWT oriented | XML oriented |
| Designed around OAuth 2.0 | Independent federation protocol |
| Common in modern web, mobile, API, CLI, and workload use cases | Common in enterprise browser SSO |
| Uses discovery and JWKS | Uses SAML metadata and X.509 signing certificates |
| Often integrates naturally with APIs | Strongly established for enterprise SaaS SSO |

## 4.3 OIDC does not automatically grant AWS permissions

A valid OIDC token does not itself define AWS permissions.

AWS permissions come from the IAM role assumed after token validation:

```text
OIDC token
    -> satisfies role trust policy
    -> STS issues role session
    -> role permissions policy controls AWS actions
```

The role’s **trust policy** controls who may enter the role. The role’s **permissions policies** control what the resulting session may do.

---

# 5. OIDC actors and components

## 5.1 End user or workload

The subject that needs authentication.

Examples:

- A human user.
- A Kubernetes service account.
- A CI/CD workflow.
- A mobile application user.
- A machine identity.

## 5.2 OpenID Provider

The **OpenID Provider**, often abbreviated **OP**, authenticates identities and issues ID tokens.

Examples include:

- Microsoft Entra ID
- Okta
- Auth0
- Keycloak
- Google
- Amazon Cognito
- The token service used by GitHub Actions
- The service-account issuer associated with an EKS cluster

## 5.3 Relying Party

The **Relying Party**, or **RP**, is the application or service that trusts the OpenID Provider.

Examples:

- A web application.
- The EKS Kubernetes API server.
- AWS IAM and STS.
- A command-line login helper.
- An internal platform portal.

## 5.4 Client

An OIDC client is an application registered with the identity provider.

Registration normally produces:

- A client ID.
- Possibly a client secret.
- One or more redirect URIs.
- Allowed grant types.
- Allowed scopes.
- Token-lifetime and policy settings.

A public client, such as a native application or CLI, cannot safely protect a permanent client secret. A confidential server-side client may use one.

## 5.5 Issuer URL

The issuer URL uniquely identifies the token issuer.

Example:

```text
https://login.example.com/realms/platform
```

The value configured by the relying party must match the token’s `iss` claim exactly according to the applicable validation rules.

## 5.6 Authorization endpoint

The authorization endpoint begins an interactive login and consent flow.

Example:

```text
https://login.example.com/realms/platform/protocol/openid-connect/auth
```

## 5.7 Token endpoint

The token endpoint exchanges an authorization code or another valid grant for tokens.

Example:

```text
https://login.example.com/realms/platform/protocol/openid-connect/token
```

## 5.8 UserInfo endpoint

The optional UserInfo endpoint returns claims about the authenticated user when called with a valid access token.

## 5.9 Redirect URI

The redirect URI is the application endpoint to which the authorization server returns the browser after authentication.

Example:

```text
https://portal.example.com/oauth/callback
```

Redirect URI validation must be strict because an attacker-controlled redirect can steal authorization codes or tokens.

## 5.10 Scopes

Scopes describe requested access or identity information.

Typical OIDC scopes:

```text
openid
profile
email
groups
offline_access
```

`openid` is the scope that changes an OAuth 2.0 authorization request into an OIDC authentication request.

## 5.11 Claims

Claims are name/value statements inside a token.

Examples:

```json
{
  "sub": "00u123456789",
  "email": "alice@example.com",
  "groups": ["developers", "platform"],
  "tenant": "engineering"
}
```

## 5.12 JWKS

A **JSON Web Key Set**, or **JWKS**, publishes public keys that relying parties use to verify token signatures.

The keys often include a key identifier called `kid`. The token header identifies the signing key, and the relying party selects the matching public key from the JWKS.

---

# 6. Discovery metadata and JWKS

An OIDC provider normally exposes discovery metadata at:

```text
<issuer>/.well-known/openid-configuration
```

Example:

```text
https://login.example.com/.well-known/openid-configuration
```

A simplified discovery document might look like this:

```json
{
  "issuer": "https://login.example.com",
  "authorization_endpoint": "https://login.example.com/oauth2/authorize",
  "token_endpoint": "https://login.example.com/oauth2/token",
  "userinfo_endpoint": "https://login.example.com/oauth2/userinfo",
  "jwks_uri": "https://login.example.com/oauth2/keys",
  "response_types_supported": ["code"],
  "subject_types_supported": ["public"],
  "id_token_signing_alg_values_supported": ["RS256"]
}
```

The relying party uses this metadata to learn:

- The canonical issuer.
- Where to send authorization requests.
- Where to exchange authorization codes.
- Where to retrieve public signing keys.
- Which signing algorithms and response types are supported.

## 6.1 Signature verification with JWKS

A simplified verification process is:

```text
1. Read the JWT header.
2. Obtain its algorithm and key ID.
3. Download or use a cached JWKS.
4. Select the public key with the matching key ID.
5. Verify the cryptographic signature.
6. Validate issuer, audience, time, nonce, and application-specific claims.
```

JWKS keys rotate. A production implementation must support key rotation and sensible caching rather than permanently hard-coding one signing key.

## 6.2 TLS certificates versus token-signing keys

These are different:

- The HTTPS/TLS certificate secures the network connection to the issuer and JWKS endpoint.
- The token-signing key signs the JWT.
- The token-signing public key appears in JWKS.
- AWS IAM may store or derive a certificate authority thumbprint for an IAM OIDC provider.

Do not confuse the web server certificate with the JWT signing key.

---

# 7. OIDC tokens and JWT structure

A JWT commonly has three Base64URL-encoded sections separated by periods:

```text
HEADER.PAYLOAD.SIGNATURE
```

Example structure:

```text
eyJhbGciOiJSUzI1NiIsImtpZCI6ImtleS0xIn0
.
eyJpc3MiOiJodHRwczovL2xvZ2luLmV4YW1wbGUuY29tIiwic3ViIjoiYWxpY2UifQ
.
<signature>
```

## 7.1 Header

The header commonly describes:

```json
{
  "alg": "RS256",
  "kid": "key-2026-01",
  "typ": "JWT"
}
```

- `alg`: signing algorithm.
- `kid`: signing-key identifier.
- `typ`: token type indicator.

## 7.2 Payload

The payload contains claims:

```json
{
  "iss": "https://login.example.com",
  "sub": "alice-123",
  "aud": "platform-portal",
  "email": "alice@example.com",
  "groups": ["developers"],
  "iat": 1784372400,
  "exp": 1784376000,
  "nonce": "random-request-value"
}
```

## 7.3 Signature

The signature protects token integrity and authenticity.

It allows the validator to detect whether:

- The token was signed by a trusted key.
- The header or payload was changed after signing.

A signed JWT is not necessarily encrypted. Anyone holding it can often decode the header and payload. Therefore, do not place secrets or unnecessary sensitive information in claims.

## 7.4 ID token

An ID token communicates authentication information to the OIDC client.

It tells the client things such as:

- Who authenticated.
- Which issuer authenticated the subject.
- Which client the token was issued for.
- When authentication and token issuance occurred.

## 7.5 Access token

An access token authorizes calls to a protected API.

Its format may be:

- A JWT.
- An opaque string.
- Another provider-specific token format.

Do not assume every access token is a JWT.

## 7.6 Refresh token

A refresh token allows a client to request new access tokens, and sometimes new ID tokens, without requiring a complete interactive login each time.

Refresh tokens are highly sensitive. They should be protected, rotated when supported, and revoked when no longer needed.

## 7.7 AWS temporary credentials are not OIDC tokens

After successful OIDC federation, AWS STS returns:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_SESSION_TOKEN
expiration
```

These temporary credentials represent an IAM role session. They are not JWTs and are used to sign AWS API requests with AWS Signature Version 4.

---

# 8. Important token claims

| Claim | Meaning | Validation importance |
|---|---|---|
| `iss` | Issuer | Must match the trusted issuer |
| `sub` | Subject | Identifies the user or workload |
| `aud` | Audience | Must identify the intended relying party |
| `exp` | Expiration time | Token must not be expired |
| `iat` | Issued-at time | Helps detect unreasonable issuance times |
| `nbf` | Not-before time | Token must not be accepted too early |
| `nonce` | Request-bound random value | Helps prevent replay and token substitution |
| `azp` | Authorized party | Relevant when multiple audiences are involved |
| `auth_time` | Authentication time | Useful when fresh authentication is required |
| `email` | Email address | An attribute, not always a stable identifier |
| `email_verified` | Whether provider verified email | Important if email is used for decisions |
| `groups` | Group memberships | Often mapped to RBAC |
| `jti` | Token identifier | Can support replay controls and audit |
| `acr` | Authentication context class | May indicate authentication strength |
| `amr` | Authentication methods references | May indicate password, MFA, hardware key, etc. |

## 8.1 `iss`

The issuer is the trust root for the token.

Example:

```json
"iss": "https://oidc.eks.eu-west-1.amazonaws.com/id/EXAMPLE"
```

A token from a different issuer must not be accepted merely because its claims look similar.

## 8.2 `sub`

The subject identifies the principal represented by the token.

For a Kubernetes service account:

```text
system:serviceaccount:<namespace>:<service-account>
```

Example:

```text
system:serviceaccount:payments:invoice-api
```

For GitHub Actions, the subject can encode repository and context, such as:

```text
repo:example-org/payments-api:ref:refs/heads/main
```

The exact GitHub subject depends on workflow context and configuration.

## 8.3 `aud`

The audience states which recipient may accept the token.

Examples:

```text
sts.amazonaws.com
kubernetes
my-web-client-id
```

A token can be cryptographically valid but still invalid for your application because it was issued to another audience.

## 8.4 `exp`, `nbf`, and clock skew

Validators must check token time claims. Systems should keep clocks synchronized. Small configured clock-skew tolerances may be necessary, but broad tolerances increase risk.

## 8.5 Email is not always the best primary identifier

An email address can change. A provider-specific immutable subject identifier is often safer for identity correlation.

If email is used:

- Require `email_verified` when appropriate.
- Understand whether the provider can recycle addresses.
- Avoid using email alone for high-risk authorization unless the lifecycle is controlled.

---

# 9. The Authorization Code flow with PKCE

For modern interactive applications, the preferred baseline is usually the **Authorization Code flow with PKCE**.

PKCE means **Proof Key for Code Exchange**.

## 9.1 Flow

```text
User          Client application          OIDC provider
 |                    |                         |
 | Open application   |                         |
 |------------------->|                         |
 |                    | Create verifier         |
 |                    | Derive challenge        |
 |                    |                         |
 |                    | Authorization request   |
 |                    | + code_challenge        |
 |                    |------------------------>|
 |                    |                         |
 |<-------------------| Redirect to login       |
 | Authenticate + MFA |                         |
 |--------------------------------------------->|
 |                    |                         |
 |                    |<------------------------|
 |                    | Authorization code      |
 |                    |                         |
 |                    | Token request           |
 |                    | + code_verifier         |
 |                    |------------------------>|
 |                    |                         |
 |                    | ID/access tokens        |
 |                    |<------------------------|
```

## 9.2 Why PKCE matters

Before redirecting the browser, the client generates:

- A random `code_verifier`.
- A derived `code_challenge`.

The provider binds the authorization code to that challenge. When redeeming the code, the client must present the original verifier.

An attacker who intercepts only the authorization code cannot redeem it without the verifier.

## 9.3 `state` and `nonce`

`state` binds the authorization response to the original browser transaction and helps mitigate cross-site request forgery and response mix-up.

`nonce` binds the returned ID token to the original authentication request and helps mitigate replay or token substitution.

Both values should be unpredictable and validated on return.

## 9.4 Why the implicit flow is not preferred for new designs

Modern OAuth security guidance deprecates or discourages weaker legacy patterns that return tokens directly through the browser front channel. Authorization Code with PKCE limits exposure and gives the authorization server stronger controls.

---

# 10. How token validation works

A relying party should not trust a token merely because it can be decoded.

A robust validator performs at least the following checks.

## 10.1 Parse safely

- Enforce size limits.
- Reject malformed token structure.
- Reject duplicate or ambiguous claims where the library exposes them.
- Use a mature standards-compliant library.

## 10.2 Restrict algorithms

Do not accept any algorithm chosen by the token without policy.

The application should have an explicit allow-list, for example:

```text
RS256
ES256
```

Reject:

```text
alg = none
```

unless a very specific standard explicitly requires an unsecured token, which normal OIDC deployments do not.

## 10.3 Verify signature

Use the provider’s JWKS and the token’s `kid` to select an allowed public key. Verify the signature before trusting claims.

## 10.4 Validate issuer

The `iss` claim must match the configured issuer.

## 10.5 Validate audience and authorized party

Confirm the token was issued for your client or service. When multiple audiences are present, apply the relevant OIDC rules, including `azp` validation where required.

## 10.6 Validate expiration and not-before

Reject expired tokens and tokens that are not yet valid.

## 10.7 Validate nonce for interactive OIDC login

Compare the token nonce to the nonce stored for the initiating request.

## 10.8 Validate application-specific required claims

Examples:

```text
tenant = engineering
groups contains platform-admins
repository_owner = example-org
environment = production
```

Claims should be used only when their semantics and issuer guarantees are understood.

## 10.9 Validate token type and intended use

Do not accept an ID token where an API expects an access token merely because both are JWTs.

## 10.10 Protect the token

Bearer tokens grant access to whoever possesses them. Protect them from:

- Logs.
- Browser history.
- Query strings.
- Error messages.
- Analytics tools.
- Shell history.
- Unencrypted storage.
- Accidental publication in CI output.

---

# 11. What an IAM OIDC provider is

An **IAM OIDC provider** is an IAM resource that describes an external OIDC issuer trusted by an AWS account.

It contains information such as:

- Issuer URL.
- Accepted client IDs or audiences.
- Certificate authority thumbprint information when applicable.
- Tags.

Conceptually:

```text
IAM OIDC provider:
    "This AWS account recognizes this token issuer."

IAM role trust policy:
    "This specific role may be assumed only by these identities
     from that issuer, under these claim conditions."
```

Creating an IAM OIDC provider alone does **not** grant access.

Access requires all of the following:

1. A valid token from the issuer.
2. An IAM OIDC provider registered for that issuer.
3. An IAM role trust policy that names the provider as a federated principal.
4. Conditions that match token claims.
5. A call to `sts:AssumeRoleWithWebIdentity`.
6. Permissions policies attached to the role.

## 11.1 Provider ARN

An IAM OIDC provider ARN resembles:

```text
arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com
```

For an EKS cluster:

```text
arn:aws:iam::123456789012:oidc-provider/oidc.eks.eu-west-1.amazonaws.com/id/EXAMPLE
```

Notice that the ARN omits the `https://` prefix.

## 11.2 Private versus shared OIDC issuers

A private issuer may have a URL unique to your organization or tenant.

A shared issuer can serve many unrelated customers from the same issuer URL. GitHub Actions is a common example.

With a shared issuer, trust policies must evaluate claims that identify your organization, repository, project, tenant, or other controlled boundary. Trusting only the issuer would trust every tenant using that shared service.

AWS IAM enforces identity-provider controls for certain recognized shared OIDC providers when roles are created or updated.

---

# 12. How AWS STS web identity federation works

The AWS API operation is:

```text
sts:AssumeRoleWithWebIdentity
```

## 12.1 Sequence

```text
1. The user or workload authenticates to an OIDC provider.
2. The provider issues a signed token.
3. The workload sends the token and target role ARN to AWS STS.
4. STS resolves the IAM OIDC provider.
5. STS verifies issuer trust, signature, audience, time, and trust-policy conditions.
6. If allowed, STS creates a temporary IAM role session.
7. STS returns temporary AWS credentials.
8. The workload signs AWS API calls with those credentials.
9. AWS evaluates the role's permissions policies and resource policies.
```

## 12.2 Temporary credentials

A successful response includes:

```json
{
  "AccessKeyId": "ASIA...",
  "SecretAccessKey": "...",
  "SessionToken": "...",
  "Expiration": "2026-07-18T12:00:00Z"
}
```

The credentials expire automatically.

## 12.3 Example direct CLI exchange

This is an educational example. In EKS and CI/CD, an SDK or official action normally performs the exchange automatically.

```bash
aws sts assume-role-with-web-identity \
  --role-arn arn:aws:iam::123456789012:role/OidcFederatedRole \
  --role-session-name example-session \
  --web-identity-token file://token.jwt \
  --duration-seconds 3600
```

## 12.4 Why this is safer than static access keys

Long-lived access keys create lifecycle problems:

- Secure distribution.
- Storage.
- Rotation.
- Revocation.
- Accidental exposure.
- Unclear ownership.
- Credentials remaining active after a workload is deleted.

OIDC federation replaces those permanent credentials with short-lived sessions tied to verifiable workload or user context.

---

# 13. IAM trust policies versus permissions policies

This distinction is essential.

## 13.1 Trust policy

The role trust policy answers:

> Who may assume this role, and under which conditions?

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:example-org/payments-api:ref:refs/heads/main"
        }
      }
    }
  ]
}
```

This permits one specific GitHub context to enter the role.

## 13.2 Permissions policy

A permissions policy answers:

> What may the resulting role session do?

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadDeploymentArtifacts",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::example-deployment-artifacts/*"
    }
  ]
}
```

## 13.3 Both must allow access

A broad trust policy with narrow permissions is still dangerous because an unintended identity can gain those permissions.

A narrow trust policy with broad permissions is dangerous because a compromised approved identity can do too much.

Apply least privilege to both:

```text
Least privilege for entry:
    Exact issuer + audience + subject/context conditions.

Least privilege after entry:
    Exact actions + resources + conditions.
```

---

# 14. Creating a generic IAM OIDC provider

This section applies to external OIDC federation, such as a private issuer or CI/CD platform.

## 14.1 Prerequisites

Obtain:

```text
Issuer URL
Expected audience/client ID
Discovery URL
JWKS URL
Required claims
TLS trust information
```

Verify the discovery document:

```bash
curl -sS https://login.example.com/.well-known/openid-configuration
```

Inspect the JWKS URL from that document:

```bash
curl -sS https://login.example.com/oauth2/keys
```

## 14.2 Create with AWS CLI

AWS IAM can retrieve the top intermediate CA thumbprint when `--thumbprint-list` is omitted in supported creation paths.

```bash
aws iam create-open-id-connect-provider \
  --url https://login.example.com \
  --client-id-list sts.amazonaws.com
```

For an issuer where you intentionally manage a thumbprint:

```bash
aws iam create-open-id-connect-provider \
  --url https://login.example.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list <SHA1_THUMBPRINT>
```

Do not copy an arbitrary thumbprint from an old tutorial. Derive and verify it according to current AWS documentation and your issuer’s certificate chain.

## 14.3 Inspect providers

```bash
aws iam list-open-id-connect-providers
```

```bash
aws iam get-open-id-connect-provider \
  --open-id-connect-provider-arn \
  arn:aws:iam::123456789012:oidc-provider/login.example.com
```

## 14.4 Create a role

Create `trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowTrustedOidcWorkload",
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/login.example.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "login.example.com:aud": "sts.amazonaws.com",
          "login.example.com:sub": "workload:platform:deployment-controller"
        }
      }
    }
  ]
}
```

Create the role:

```bash
aws iam create-role \
  --role-name PlatformDeploymentController \
  --assume-role-policy-document file://trust-policy.json
```

Attach a narrow permissions policy:

```bash
aws iam attach-role-policy \
  --role-name PlatformDeploymentController \
  --policy-arn arn:aws:iam::123456789012:policy/PlatformDeploymentPermissions
```

## 14.5 Terraform example

Provider behavior changes over time, so pin and review a supported AWS provider version.

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_iam_openid_connect_provider" "example" {
  url = "https://login.example.com"

  client_id_list = [
    "sts.amazonaws.com"
  ]

  tags = {
    Name      = "example-oidc"
    ManagedBy = "Terraform"
  }
}
```

Role trust policy:

```hcl
data "aws_iam_policy_document" "oidc_trust" {
  statement {
    sid     = "AllowTrustedOidcWorkload"
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type = "Federated"
      identifiers = [
        aws_iam_openid_connect_provider.example.arn
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "login.example.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "login.example.com:sub"
      values   = ["workload:platform:deployment-controller"]
    }
  }
}

resource "aws_iam_role" "deployment_controller" {
  name               = "PlatformDeploymentController"
  assume_role_policy = data.aws_iam_policy_document.oidc_trust.json
}
```

---

# 15. The three identity problems around Amazon EKS

OIDC is used around EKS for different purposes.

## 15.1 Workload-to-AWS authentication

Question:

> How does a pod obtain AWS credentials for S3, DynamoDB, SQS, Secrets Manager, or another AWS service?

Solutions:

- **EKS Pod Identity**
- **IAM Roles for Service Accounts**, known as **IRSA**

## 15.2 Human-to-Kubernetes authentication

Question:

> How does a developer authenticate to the Kubernetes API?

Solutions include:

- IAM role authentication and EKS access entries.
- An external OIDC provider associated directly with EKS.

## 15.3 Human-to-AWS authentication

Question:

> How does an employee access AWS accounts, the AWS Console, AWS CLI, and then perhaps EKS?

Common solution:

- AWS IAM Identity Center.
- External workforce IdP through SAML 2.0.
- SCIM user/group provisioning.
- Permission sets.
- IAM roles in target accounts.
- EKS access entries for those roles.

These are not interchangeable.

---

# 16. EKS workload identity with IRSA

**IRSA** means **IAM Roles for Service Accounts**.

IRSA maps a Kubernetes ServiceAccount to an IAM role. A pod using that service account receives a projected OIDC token and can exchange it through AWS STS for temporary role credentials.

## 16.1 Architecture

```text
Kubernetes Pod
      |
      | configured with serviceAccountName
      v
Kubernetes ServiceAccount
      |
      | projected signed JWT
      | sub = system:serviceaccount:<namespace>:<service-account>
      | aud = sts.amazonaws.com
      v
EKS cluster OIDC issuer
      |
      | public discovery metadata and signing keys
      v
IAM OIDC provider in AWS account
      |
      | named as Federated principal
      v
IAM role trust policy
      |
      | checks aud and sub
      v
AWS STS AssumeRoleWithWebIdentity
      |
      v
Temporary IAM role credentials
      |
      v
AWS services
```

## 16.2 Why IRSA exists

Without workload identity, pods often inherit the EC2 node role.

That creates several problems:

- Every pod on the node may be able to obtain the same node credentials.
- The node role becomes excessively broad.
- Permissions cannot be cleanly separated per application.
- Auditing shows the node role rather than a workload-specific role.
- Compromise of one pod can expose permissions intended for other workloads.

IRSA improves isolation by assigning AWS permissions to a Kubernetes service account used by a specific workload.

## 16.3 Important security limitation

Containers are not a perfect security boundary. A compromised privileged pod, node component, host process, or pod with access to another pod’s filesystem or metadata may still create risk.

IRSA improves IAM credential scoping; it does not replace:

- Kubernetes security contexts.
- Pod Security Standards.
- Network policies.
- Node isolation.
- Secrets protection.
- Admission controls.
- Runtime security.
- Least-privilege Kubernetes RBAC.

---

# 17. Complete IRSA setup lab

This lab creates an EKS service account that can read objects from one S3 bucket.

## 17.1 Variables

```bash
export AWS_REGION="eu-west-1"
export CLUSTER_NAME="platform-dev"
export NAMESPACE="payments"
export SERVICE_ACCOUNT="invoice-reader"
export ROLE_NAME="EksPaymentsInvoiceReader"
export POLICY_NAME="EksPaymentsInvoiceReaderPolicy"
export BUCKET_NAME="example-payments-invoices"
export ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
```

Verify identity:

```bash
aws sts get-caller-identity
```

Verify cluster connectivity:

```bash
aws eks describe-cluster \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION"
```

```bash
aws eks update-kubeconfig \
  --name "$CLUSTER_NAME" \
  --region "$AWS_REGION"
```

```bash
kubectl get nodes
```

## 17.2 Obtain the cluster OIDC issuer

```bash
export OIDC_ISSUER="$(
  aws eks describe-cluster \
    --name "$CLUSTER_NAME" \
    --region "$AWS_REGION" \
    --query "cluster.identity.oidc.issuer" \
    --output text
)"
```

Display it:

```bash
echo "$OIDC_ISSUER"
```

Example:

```text
https://oidc.eks.eu-west-1.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E
```

Create a host/path form without `https://`:

```bash
export OIDC_PROVIDER="${OIDC_ISSUER#https://}"
echo "$OIDC_PROVIDER"
```

## 17.3 Check whether the IAM OIDC provider exists

```bash
aws iam list-open-id-connect-providers
```

A targeted check:

```bash
aws iam list-open-id-connect-providers \
  --query "OpenIDConnectProviderList[].Arn" \
  --output text | tr '\t' '\n' | grep "$OIDC_PROVIDER" || true
```

## 17.4 Associate the EKS issuer with IAM

Using `eksctl`:

```bash
eksctl utils associate-iam-oidc-provider \
  --cluster "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --approve
```

Console path:

```text
Amazon EKS
  -> Clusters
  -> platform-dev
  -> Overview
  -> OpenID Connect provider URL

IAM
  -> Identity providers
  -> Add provider
  -> OpenID Connect
  -> Provider URL: EKS issuer URL
  -> Audience: sts.amazonaws.com
```

## 17.5 Create namespace

```bash
kubectl create namespace "$NAMESPACE" \
  --dry-run=client \
  -o yaml | kubectl apply -f -
```

## 17.6 Create the IAM permissions policy

Create `s3-read-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListInvoiceBucket",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::example-payments-invoices"
    },
    {
      "Sid": "ReadInvoiceObjects",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::example-payments-invoices/*"
    }
  ]
}
```

Create it:

```bash
aws iam create-policy \
  --policy-name "$POLICY_NAME" \
  --policy-document file://s3-read-policy.json
```

Store the ARN:

```bash
export POLICY_ARN="arn:aws:iam::$ACCOUNT_ID:policy/$POLICY_NAME"
```

## 17.7 Create the service account and role with `eksctl`

```bash
eksctl create iamserviceaccount \
  --cluster "$CLUSTER_NAME" \
  --region "$AWS_REGION" \
  --namespace "$NAMESPACE" \
  --name "$SERVICE_ACCOUNT" \
  --role-name "$ROLE_NAME" \
  --attach-policy-arn "$POLICY_ARN" \
  --approve
```

This can:

- Create or manage the Kubernetes service account.
- Create the IAM role.
- Attach the permissions policy.
- Create the OIDC trust policy.
- Annotate the service account with the role ARN.

## 17.8 Inspect the ServiceAccount

```bash
kubectl get serviceaccount "$SERVICE_ACCOUNT" \
  -n "$NAMESPACE" \
  -o yaml
```

Expected annotation:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: invoice-reader
  namespace: payments
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/EksPaymentsInvoiceReader
```

## 17.9 Inspect the IAM trust policy

```bash
aws iam get-role \
  --role-name "$ROLE_NAME" \
  --query "Role.AssumeRolePolicyDocument"
```

Expected structure:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/oidc.eks.eu-west-1.amazonaws.com/id/EXAMPLE"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.eu-west-1.amazonaws.com/id/EXAMPLE:aud": "sts.amazonaws.com",
          "oidc.eks.eu-west-1.amazonaws.com/id/EXAMPLE:sub": "system:serviceaccount:payments:invoice-reader"
        }
      }
    }
  ]
}
```

## 17.10 Deploy a test pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: irsa-test
  namespace: payments
spec:
  serviceAccountName: invoice-reader
  restartPolicy: Never
  containers:
    - name: aws-cli
      image: public.ecr.aws/aws-cli/aws-cli:2
      command:
        - sh
        - -c
        - |
          aws sts get-caller-identity
          aws s3 ls s3://example-payments-invoices
          sleep 3600
```

Apply it:

```bash
kubectl apply -f irsa-test.yaml
```

Read logs:

```bash
kubectl logs -n "$NAMESPACE" irsa-test
```

The ARN returned by `get-caller-identity` should represent the IRSA role session, not the EC2 node role.

## 17.11 Inspect injected configuration

```bash
kubectl exec -n "$NAMESPACE" irsa-test -- env | \
  grep -E 'AWS_ROLE_ARN|AWS_WEB_IDENTITY_TOKEN_FILE|AWS_REGION'
```

Typical variables include:

```text
AWS_ROLE_ARN
AWS_WEB_IDENTITY_TOKEN_FILE
AWS_REGION
AWS_DEFAULT_REGION
```

Inspect the token file path without printing the complete token into logs:

```bash
kubectl exec -n "$NAMESPACE" irsa-test -- \
  sh -c 'ls -l "$AWS_WEB_IDENTITY_TOKEN_FILE"'
```

## 17.12 Use IRSA in a Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: invoice-api
  namespace: payments
spec:
  replicas: 2
  selector:
    matchLabels:
      app: invoice-api
  template:
    metadata:
      labels:
        app: invoice-api
    spec:
      serviceAccountName: invoice-reader
      containers:
        - name: application
          image: 123456789012.dkr.ecr.eu-west-1.amazonaws.com/invoice-api:1.0.0
          ports:
            - name: http
              containerPort: 8080
```

The application should use a supported AWS SDK and its default credential-provider chain. Do not hard-code access keys or manually force node-role credentials.

## 17.13 Manual role creation alternative

Create the service account:

```bash
kubectl create serviceaccount "$SERVICE_ACCOUNT" \
  --namespace "$NAMESPACE"
```

Create `irsa-trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowExactKubernetesServiceAccount",
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/oidc.eks.eu-west-1.amazonaws.com/id/EXAMPLE"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.eu-west-1.amazonaws.com/id/EXAMPLE:aud": "sts.amazonaws.com",
          "oidc.eks.eu-west-1.amazonaws.com/id/EXAMPLE:sub": "system:serviceaccount:payments:invoice-reader"
        }
      }
    }
  ]
}
```

Create role:

```bash
aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document file://irsa-trust-policy.json
```

Attach permissions:

```bash
aws iam attach-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-arn "$POLICY_ARN"
```

Annotate ServiceAccount:

```bash
kubectl annotate serviceaccount "$SERVICE_ACCOUNT" \
  --namespace "$NAMESPACE" \
  "eks.amazonaws.com/role-arn=arn:aws:iam::$ACCOUNT_ID:role/$ROLE_NAME" \
  --overwrite
```

Restart existing pods so they are recreated with the required projected-token and environment configuration:

```bash
kubectl rollout restart deployment invoice-api \
  --namespace "$NAMESPACE"
```

---

# 18. How IRSA works internally

## 18.1 Kubernetes ServiceAccount identity

A Kubernetes ServiceAccount provides an identity for processes running in pods.

A pod references it:

```yaml
spec:
  serviceAccountName: invoice-reader
```

## 18.2 Projected service-account token

Modern Kubernetes can issue time-limited projected ServiceAccount tokens with:

- An issuer.
- A subject.
- One or more audiences.
- Expiration.
- A cryptographic signature.
- Claims that bind the token to Kubernetes identity context.

For IRSA, the key subject format is:

```text
system:serviceaccount:<namespace>:<service-account-name>
```

## 18.3 EKS cluster issuer

Each EKS cluster has an OIDC issuer URL. EKS publishes public signing keys so external systems such as AWS IAM and STS can validate the cluster-issued service-account token.

## 18.4 IAM OIDC provider

The AWS account registers the cluster issuer as an IAM OIDC provider. This links the external issuer identity to IAM trust-policy evaluation.

## 18.5 Service-account annotation

The annotation identifies the role the pod should request:

```yaml
eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/EksPaymentsInvoiceReader
```

## 18.6 Pod mutation and credential chain

When the pod is admitted, EKS-integrated behavior supplies configuration such as:

```text
AWS_ROLE_ARN
AWS_WEB_IDENTITY_TOKEN_FILE
```

A supported AWS SDK’s default credential chain detects those values and calls STS `AssumeRoleWithWebIdentity`.

The application normally does not need to implement token exchange manually.

## 18.7 Credential rotation

The projected token and AWS role credentials are temporary. Kubernetes and the AWS SDK participate in refreshing credentials.

Applications should:

- Reuse SDK clients appropriately.
- Avoid copying credentials into static configuration.
- Avoid reading credentials once and assuming they never expire.
- Use current supported SDK versions.

---

# 19. IRSA trust-policy patterns

## 19.1 Exact service account — preferred default

```json
"Condition": {
  "StringEquals": {
    "<issuer-host-and-path>:aud": "sts.amazonaws.com",
    "<issuer-host-and-path>:sub": "system:serviceaccount:payments:invoice-reader"
  }
}
```

This is the narrowest common pattern.

## 19.2 Several exact service accounts

Use multiple statements or a controlled list when the policy syntax and semantics are clear:

```json
"Condition": {
  "StringEquals": {
    "<issuer-host-and-path>:aud": "sts.amazonaws.com",
    "<issuer-host-and-path>:sub": [
      "system:serviceaccount:payments:invoice-reader",
      "system:serviceaccount:payments:invoice-writer"
    ]
  }
}
```

Separate IAM roles are usually clearer when workloads need different permissions.

## 19.3 All service accounts in one namespace

```json
"Condition": {
  "StringEquals": {
    "<issuer-host-and-path>:aud": "sts.amazonaws.com"
  },
  "StringLike": {
    "<issuer-host-and-path>:sub": "system:serviceaccount:payments:*"
  }
}
```

This is broader. Every service account in `payments` can potentially assume the role if configured to do so.

Use only when the namespace itself is a strong and well-governed security boundary.

## 19.4 Dangerous wildcard

Avoid:

```json
"StringLike": {
  "<issuer-host-and-path>:sub": "system:serviceaccount:*:*"
}
```

That trusts every service account in the cluster.

## 19.5 Cross-account IRSA

A pod in Account A can access a role or resources in Account B through designs such as:

1. Registering the EKS issuer from Account A in Account B and trusting it directly.
2. Assuming a local IRSA role in Account A, then using `sts:AssumeRole` into a target role in Account B.

Cross-account design must address:

- Trust policy in both accounts.
- Permissions to call `sts:AssumeRole`.
- External IDs where appropriate.
- Session duration.
- Resource policies.
- CloudTrail audit paths.
- Organizational controls and SCPs.

---

# 20. EKS Pod Identity

EKS Pod Identity is an AWS-managed mechanism for mapping Kubernetes service accounts to IAM roles without creating an IAM OIDC provider for each cluster.

## 20.1 Architecture

```text
Pod
  |
  | uses Kubernetes ServiceAccount
  v
EKS Pod Identity Agent on the node
  |
  | communicates with EKS Auth API
  v
Amazon EKS service
  |
  | assumes IAM role
  | principal = pods.eks.amazonaws.com
  v
AWS STS
  |
  | returns temporary credentials
  v
Pod SDK credential provider
```

## 20.2 Main components

- Kubernetes ServiceAccount.
- EKS Pod Identity association.
- EKS Pod Identity Agent.
- EKS Auth API.
- IAM role trusting `pods.eks.amazonaws.com`.
- Supported AWS SDK default credential chain.

## 20.3 Install the Pod Identity Agent

For standard EKS clusters:

```bash
aws eks create-addon \
  --cluster-name "$CLUSTER_NAME" \
  --addon-name eks-pod-identity-agent
```

Check:

```bash
kubectl get daemonset \
  -n kube-system \
  eks-pod-identity-agent
```

EKS Auto Mode includes the necessary capability, so the separate setup requirement differs.

## 20.4 IAM role trust policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowEksAuthToAssumeRoleForPodIdentity",
      "Effect": "Allow",
      "Principal": {
        "Service": "pods.eks.amazonaws.com"
      },
      "Action": [
        "sts:AssumeRole",
        "sts:TagSession"
      ]
    }
  ]
}
```

`sts:TagSession` allows EKS Pod Identity to attach Kubernetes context as role-session tags.

## 20.5 Restrict by namespace and ServiceAccount

A more restrictive trust policy can evaluate request tags:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowExactPodIdentity",
      "Effect": "Allow",
      "Principal": {
        "Service": "pods.eks.amazonaws.com"
      },
      "Action": [
        "sts:AssumeRole",
        "sts:TagSession"
      ],
      "Condition": {
        "StringEquals": {
          "aws:RequestTag/kubernetes-namespace": "payments",
          "aws:RequestTag/kubernetes-service-account": "invoice-reader"
        }
      }
    }
  ]
}
```

Review current AWS documentation for the complete set and exact use of Pod Identity session tags.

## 20.6 Create an association

```bash
aws eks create-pod-identity-association \
  --cluster-name "$CLUSTER_NAME" \
  --namespace "$NAMESPACE" \
  --service-account "$SERVICE_ACCOUNT" \
  --role-arn "arn:aws:iam::$ACCOUNT_ID:role/$ROLE_NAME"
```

List associations:

```bash
aws eks list-pod-identity-associations \
  --cluster-name "$CLUSTER_NAME"
```

Describe one:

```bash
aws eks describe-pod-identity-association \
  --cluster-name "$CLUSTER_NAME" \
  --association-id <ASSOCIATION_ID>
```

Unlike IRSA, the ServiceAccount does not require the IRSA role annotation to define the association.

## 20.7 Session tags and ABAC

EKS Pod Identity can include predefined session tags such as:

```text
eks-cluster-arn
eks-cluster-name
kubernetes-namespace
kubernetes-service-account
kubernetes-pod-name
```

These attributes can support attribute-based access control.

Example concept:

```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::example-app-data/${aws:PrincipalTag/kubernetes-namespace}/*"
}
```

ABAC can reduce the number of separate roles and policies, but it must be designed carefully. Ensure users cannot manipulate the attributes that drive authorization in an unsafe way.

## 20.8 Operational considerations

- The agent runs as a DaemonSet on nodes.
- It serves credentials only to pods on the same node.
- Supported SDK versions are required.
- Credentials are temporary.
- Association changes may not be reflected in already cached credentials immediately.
- A service account can be associated with one role in the relevant cluster/account model.
- Cross-account designs can use target roles and role chaining.
- Pod Identity is specific to Amazon EKS.

---

# 21. IRSA versus EKS Pod Identity

| Area | IRSA | EKS Pod Identity |
|---|---|---|
| IAM OIDC provider required | Yes | No |
| Role trust principal | Cluster-specific OIDC provider ARN | `pods.eks.amazonaws.com` |
| STS operation | `AssumeRoleWithWebIdentity` | `AssumeRole` through EKS |
| Kubernetes mapping | ServiceAccount annotation and role trust conditions | EKS Pod Identity association |
| Per-cluster trust-policy entry | Commonly yes | Not required in the same way |
| Session tags | Not the primary IRSA model | Built-in Kubernetes context tags |
| Agent on nodes | No dedicated Pod Identity Agent | Required, except integrated modes such as EKS Auto Mode |
| Platform scope | EKS and other compatible Kubernetes environments | Amazon EKS |
| Existing ecosystem | Mature and widely deployed | Newer AWS-managed mechanism |
| New EKS workload recommendation | Still supported | AWS recommends/suggests it for many new EKS workload-permission cases |
| Direct OIDC learning value | High | It deliberately hides/removes the per-cluster OIDC integration |

## 21.1 Choose EKS Pod Identity when

- You are building a new standard Amazon EKS deployment.
- You want simpler separation between IAM administration and cluster administration.
- You want reusable IAM-role trust policies.
- You want Kubernetes context as session tags.
- Your SDK and platform requirements are supported.
- You prefer EKS-managed associations.

## 21.2 Choose or retain IRSA when

- You already operate IRSA reliably.
- You need a Kubernetes environment beyond standard EKS where IRSA-style federation is supported.
- A controller, add-on, or platform integration is documented specifically for IRSA.
- Your organization’s controls are already built around OIDC provider trust.
- Migration cost exceeds the immediate benefit.
- You need direct control of the `sub` and `aud` web-identity trust model.

## 21.3 Migration approach

A safe migration should:

1. Inventory ServiceAccounts, roles, policies, annotations, and workloads.
2. Confirm Pod Identity Agent and SDK compatibility.
3. Create Pod Identity roles and associations.
4. Test with a non-production workload.
5. Confirm the role identity with `aws sts get-caller-identity`.
6. Compare AWS API authorization behavior.
7. Remove the IRSA annotation only after successful testing.
8. Retain rollback instructions.
9. Remove obsolete trust statements and providers only after all dependencies are gone.

---

# 22. Human authentication to EKS with an external OIDC provider

EKS can associate an external OIDC provider to authenticate users directly to the Kubernetes API.

Examples:

- Okta.
- Keycloak.
- Auth0.
- Ping Identity.
- Microsoft Entra ID, when configured as an OIDC issuer for this use case.
- Another standards-compliant public OIDC provider.

This is different from IRSA.

```text
IRSA:
    Kubernetes ServiceAccount -> AWS role

External EKS OIDC:
    Human-issued ID token -> Kubernetes user and groups
```

## 22.1 Flow

```text
Developer
   |
   | authenticates, often through browser + MFA
   v
Corporate OIDC provider
   |
   | issues ID token
   v
kubectl exec credential plugin or login helper
   |
   | sends bearer token
   v
EKS Kubernetes API server
   |
   | validates issuer, signature, audience, time, required claims
   v
Kubernetes username and groups
   |
   v
Kubernetes RBAC
```

## 22.2 EKS constraints and important facts

Current AWS documentation states:

- You can associate one OIDC identity provider with a cluster.
- The issuer must be publicly reachable so EKS can discover signing keys.
- Self-signed certificates are not supported for this integration.
- IAM authentication cannot be disabled because EKS still requires it, including for nodes.
- The EKS cluster itself must be created by an IAM principal.
- OIDC-authenticated users can appear in Kubernetes control-plane audit logs when enabled.
- Direct OIDC Kubernetes authentication does not sign the user into the AWS Management Console.
- Direct OIDC Kubernetes users do not automatically receive IAM permissions for EKS or other AWS APIs.

## 22.3 Required provider information

You need:

```text
Issuer URL
Client ID / audience
Username claim
Optional username prefix
Groups claim
Optional groups prefix
Optional required claims
```

## 22.4 `eksctl` configuration example

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: platform-dev
  region: eu-west-1

identityProviders:
  - name: corporate-oidc
    type: oidc

    issuerUrl: https://login.example.com/realms/engineering
    clientId: kubernetes

    usernameClaim: email
    usernamePrefix: "oidc:"

    groupsClaim: groups
    groupsPrefix: "oidc:"

    requiredClaims:
      tenant: engineering
```

Associate it:

```bash
eksctl associate identityprovider \
  -f associate-identity-provider.yaml
```

## 22.5 AWS CLI example

```bash
aws eks associate-identity-provider-config \
  --cluster-name platform-dev \
  --oidc '{
    "identityProviderConfigName": "corporate-oidc",
    "issuerUrl": "https://login.example.com/realms/engineering",
    "clientId": "kubernetes",
    "usernameClaim": "email",
    "usernamePrefix": "oidc:",
    "groupsClaim": "groups",
    "groupsPrefix": "oidc:",
    "requiredClaims": {
      "tenant": "engineering"
    }
  }'
```

Check update status:

```bash
aws eks describe-update \
  --name platform-dev \
  --update-id <UPDATE_ID>
```

Describe provider:

```bash
aws eks describe-identity-provider-config \
  --cluster-name platform-dev \
  --identity-provider-config \
  type=oidc,name=corporate-oidc
```

## 22.6 Prefix rules

Avoid identity collisions.

Example mappings:

```text
email claim:
    alice@example.com

Kubernetes username:
    oidc:alice@example.com
```

```text
groups claim:
    platform-admins

Kubernetes group:
    oidc:platform-admins
```

Do not configure prefixes containing `system:`. Kubernetes reserves the `system:` prefix for system identities.

## 22.7 Required claims

Required claims add an extra acceptance condition.

Example:

```yaml
requiredClaims:
  tenant: engineering
  cluster_access: platform-dev
```

The token must contain matching values.

Use required claims to reduce the risk that a token valid for the same client and issuer but intended for a different organizational context receives access.

## 22.8 Configure `kubectl`

EKS validates the token, but it does not implement your provider’s login user experience.

You need a kubeconfig credential mechanism that:

1. Starts the OIDC login.
2. Uses Authorization Code with PKCE where supported.
3. Obtains an ID token for the correct client/audience.
4. Refreshes or reacquires tokens.
5. Returns the credential to `kubectl` through an `exec` plugin.

Conceptual kubeconfig:

```yaml
apiVersion: v1
kind: Config

users:
  - name: corporate-oidc
    user:
      exec:
        apiVersion: client.authentication.k8s.io/v1
        command: kubectl
        args:
          - oidc-login
          - get-token
          - --oidc-issuer-url=https://login.example.com/realms/engineering
          - --oidc-client-id=kubernetes
          - --oidc-extra-scope=profile
          - --oidc-extra-scope=email
          - --oidc-extra-scope=groups
        interactiveMode: IfAvailable
```

The exact plugin and arguments depend on the provider and chosen credential helper.

---

# 23. OIDC authentication and Kubernetes RBAC

OIDC authenticates the user. Kubernetes RBAC authorizes actions.

## 23.1 Namespace-scoped developer access

Use a Role:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: application-developer
  namespace: development
rules:
  - apiGroups: [""]
    resources:
      - pods
      - pods/log
      - services
      - configmaps
    verbs:
      - get
      - list
      - watch
  - apiGroups: ["apps"]
    resources:
      - deployments
      - replicasets
    verbs:
      - get
      - list
      - watch
      - patch
      - update
```

Bind the OIDC group:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: oidc-developers
  namespace: development
subjects:
  - kind: Group
    name: oidc:developers
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: application-developer
  apiGroup: rbac.authorization.k8s.io
```

## 23.2 Reuse a built-in ClusterRole in one namespace

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: oidc-developers-edit
  namespace: development
subjects:
  - kind: Group
    name: oidc:developers
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: edit
  apiGroup: rbac.authorization.k8s.io
```

Even though `edit` is a ClusterRole, a RoleBinding scopes its permissions to the binding’s namespace.

## 23.3 Cluster-wide binding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: oidc-readers
subjects:
  - kind: Group
    name: oidc:cluster-readers
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
```

ClusterRoleBindings are cluster-wide. Use them carefully.

## 23.4 Test authorization

As an administrator:

```bash
kubectl auth can-i list pods \
  --namespace development \
  --as="oidc:alice@example.com" \
  --as-group="oidc:developers"
```

For cluster-wide checks:

```bash
kubectl auth can-i get nodes \
  --as="oidc:alice@example.com" \
  --as-group="oidc:developers"
```

## 23.5 Group-claim governance

A group claim is only safe for authorization if:

- The issuer reliably controls it.
- Users cannot self-assign protected groups.
- Group names are stable.
- Group removal propagates promptly.
- Token lifetime is short enough for revocation requirements.
- The relying party maps the intended claim, not an untrusted custom field.
- Administrative groups are reviewed and audited.

---

# 24. IAM-based EKS access and access entries

For AWS IAM principals, AWS documents EKS access entries as the best way to grant users access to the Kubernetes API.

This works well with IAM Identity Center:

```text
Corporate user
  -> IAM Identity Center
  -> permission set
  -> IAM role in AWS account
  -> EKS access entry
  -> EKS access policy or Kubernetes group
  -> Kubernetes permissions
```

## 24.1 Why this model is often preferred for AWS-centric organizations

- Centralized workforce access through IAM Identity Center.
- MFA and session controls at the identity-provider layer.
- Temporary IAM role credentials.
- CloudTrail visibility for AWS role use.
- EKS API-based access management.
- Infrastructure-as-code support.
- Recovery without editing the in-cluster `aws-auth` ConfigMap.
- Consistency between AWS account access and cluster access.

## 24.2 Access-entry example

Create an entry for an IAM role:

```bash
aws eks create-access-entry \
  --cluster-name platform-dev \
  --principal-arn arn:aws:iam::123456789012:role/AWSReservedSSO_PlatformEngineer_Example
```

Associate a managed EKS access policy at namespace scope:

```bash
aws eks associate-access-policy \
  --cluster-name platform-dev \
  --principal-arn arn:aws:iam::123456789012:role/AWSReservedSSO_PlatformEngineer_Example \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSEditPolicy \
  --access-scope type=namespace,namespaces=development
```

Alternatively, an access entry can map the IAM principal to Kubernetes groups, and standard Kubernetes RBAC can authorize those groups.

## 24.3 `aws-auth` ConfigMap

The legacy `aws-auth` ConfigMap method is deprecated for managing human IAM-principal access. New designs should prefer access entries where supported.

Do not delete existing `aws-auth` entries blindly. Managed node groups, Fargate profiles, and legacy clusters may have dependencies that require a controlled migration.

## 24.4 External OIDC versus Identity Center + access entries

Choose external OIDC direct to Kubernetes when:

- Users should authenticate directly to the Kubernetes API through the corporate OIDC provider.
- They should not require AWS IAM credentials for Kubernetes access.
- Provider-issued claims and Kubernetes RBAC are the desired control plane.

Choose Identity Center + IAM roles + EKS access entries when:

- Users already access AWS through IAM Identity Center.
- You want unified AWS and Kubernetes workforce access.
- You want EKS access managed through AWS APIs and infrastructure as code.
- CloudTrail and IAM role controls are central to your security model.

---

# 25. OIDC and AWS IAM Identity Center

A frequent misconception is:

> “My corporate provider supports OIDC, so I should create an IAM OIDC provider for IAM Identity Center workforce login.”

That is normally incorrect.

For an external workforce identity source, IAM Identity Center uses:

```text
SAML 2.0:
    User authentication and browser SSO.

SCIM 2.0:
    User and group provisioning into IAM Identity Center.
```

## 25.1 Standard workforce flow

```text
Employee
  |
  | opens AWS access portal
  v
IAM Identity Center
  |
  | redirects through SAML
  v
External identity provider
  |
  | authenticates user + MFA
  | returns signed SAML assertion
  v
IAM Identity Center
  |
  | resolves provisioned user and assignments
  v
Permission set
  |
  | provisions/uses IAM role in target AWS account
  v
AWS Console or CLI session
```

## 25.2 SCIM provisioning

SAML authenticates, but it does not provide a general way for Identity Center to query all users and groups.

SCIM synchronizes:

- Users.
- Groups.
- Memberships.
- Selected attributes.
- Lifecycle events such as deactivation.

Before users or groups can be assigned to AWS accounts and applications, IAM Identity Center must know about them through SCIM or manual provisioning.

## 25.3 General setup process

In IAM Identity Center:

```text
Settings
  -> Identity source
  -> Actions
  -> Change identity source
  -> External identity provider
```

High-level procedure:

1. Download IAM Identity Center service-provider metadata.
2. Configure an enterprise application in the external IdP.
3. Import or enter AWS SAML endpoints and identifiers in the IdP.
4. Export the IdP metadata.
5. Upload the IdP metadata into IAM Identity Center.
6. Configure SCIM provisioning.
7. Synchronize a test user and test group.
8. Create permission sets.
9. Assign groups to AWS accounts and permission sets.
10. Test non-administrative access.
11. Migrate administrative access with a break-glass plan.
12. Monitor sign-in and provisioning logs.

## 25.4 Identity Center OIDC APIs

IAM Identity Center exposes OIDC-related APIs used by supported clients and trusted identity propagation scenarios.

This does not mean external workforce sign-in is configured by creating a generic IAM OIDC provider. The protocol used for the standard external identity source remains SAML, with SCIM for provisioning.

---

# 26. Identity Center trusted token issuers

A **trusted token issuer** is an advanced IAM Identity Center feature for **trusted identity propagation**.

It solves a different problem from AWS account portal login.

## 26.1 Purpose

An application authenticates a user outside IAM Identity Center and obtains a token from an external OAuth 2.0 authorization server.

The application then needs to call an AWS managed application or supported AWS capability **on behalf of that user**, preserving the user identity for authorization and audit.

## 26.2 Architecture

```text
User
  |
  | signs in
  v
External OAuth 2.0 / OIDC authorization server
  |
  | issues signed user token
  v
Requesting application
  |
  | requests access on behalf of user
  v
IAM Identity Center trusted-token-issuer configuration
  |
  | validates issuer and token
  | maps token attribute to Identity Center user
  v
Receiving AWS application
  |
  | authorizes using propagated workforce identity
  v
AWS resource or data
```

## 26.3 Configuration

Console path:

```text
IAM Identity Center
  -> Settings
  -> Authentication
  -> Trusted token issuers
  -> Create trusted token issuer
```

You configure:

- Issuer URL.
- Trusted token issuer name.
- Attribute mapping between the external token and Identity Center identity store.
- Application-side audience and authorization configuration.

The issuer URL must match the token’s `iss` claim. AWS documentation instructs administrators to enter the issuer base URL up to, but not including, `/.well-known/openid-configuration`.

## 26.4 Token information

The token used in the flow includes information such as:

- Subject (`sub`).
- The mapped user attribute.
- Audience (`aud`) for the receiving application.

Other claims may exist, but IAM Identity Center uses the documented values needed for validation and user lookup.

## 26.5 What a trusted token issuer is not

It is not:

- The normal AWS access portal workforce sign-in configuration.
- A replacement for SAML and SCIM in the standard external IdP integration.
- A generic mechanism that makes every AWS service accept an arbitrary external JWT.
- The same as an IAM OIDC provider used by STS.

---

# 27. GitHub Actions OIDC federation with AWS

GitHub Actions can obtain temporary AWS credentials without storing a permanent AWS access key in GitHub secrets.

## 27.1 Architecture

```text
GitHub Actions job
    |
    | requests OIDC token
    v
GitHub OIDC issuer
    |
    | signed JWT with repository/workflow context
    v
IAM OIDC provider
    |
    v
IAM role trust policy
    |
    | checks aud and sub
    v
AWS STS
    |
    | temporary credentials
    v
AWS deployment APIs
```

## 27.2 Create the provider

Issuer:

```text
https://token.actions.githubusercontent.com
```

Audience commonly used for AWS:

```text
sts.amazonaws.com
```

CLI:

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com
```

Check whether it already exists before creating a duplicate.

## 27.3 Secure trust policy for one branch

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowMainBranchDeployment",
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:example-org/payments-api:ref:refs/heads/main"
        }
      }
    }
  ]
}
```

## 27.4 Environment-based trust

For production, GitHub environments can add deployment controls such as approvals and branch restrictions.

A subject may use an environment context, for example:

```text
repo:example-org/payments-api:environment:production
```

The exact subject must be verified against GitHub’s current OIDC claim documentation and the workflow context.

## 27.5 Workflow example

```yaml
name: Deploy to AWS

on:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v5
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubPaymentsDeployment
          aws-region: eu-west-1

      - name: Confirm identity
        run: aws sts get-caller-identity

      - name: Deploy
        run: |
          aws s3 sync ./dist s3://example-payments-static-site/
```

Review current major versions before implementation. Pinning by immutable commit SHA can reduce supply-chain risk for third-party actions.

## 27.6 Dangerous trust example

Avoid:

```json
"StringLike": {
  "token.actions.githubusercontent.com:sub": "repo:*"
}
```

That may trust repositories outside your organization.

A safer broad organization rule, when truly required, is still narrower:

```json
"StringLike": {
  "token.actions.githubusercontent.com:sub": "repo:example-org/*"
}
```

However, repository-level or environment-level trust is better for production roles.

## 27.7 Additional controls

- Use separate roles for development and production.
- Use GitHub environments for production.
- Restrict branches and tags.
- Require reviewers.
- Use short role-session duration.
- Limit IAM permissions.
- Add resource-policy controls.
- Protect workflow files with CODEOWNERS.
- Pin external actions.
- Review pull-request trust boundaries, especially for forks.
- Do not expose cloud credentials to untrusted pull-request code.

---

# 28. Other OIDC examples

## 28.1 Amazon Cognito application login

Amazon Cognito user pools can act as an OIDC provider for applications.

Typical use:

```text
Browser/mobile user
  -> Cognito hosted or custom login
  -> ID token and access token
  -> application session
  -> protected API
```

Cognito identity pools can also broker identities into temporary AWS credentials, but their trust and authorization model is distinct from direct generic IAM OIDC federation.

## 28.2 Keycloak and EKS human authentication

Keycloak can issue OIDC ID tokens with claims such as:

```json
{
  "iss": "https://keycloak.example.com/realms/engineering",
  "aud": "kubernetes",
  "preferred_username": "alice",
  "groups": ["developers"]
}
```

EKS can map:

```text
preferred_username -> Kubernetes username
groups              -> Kubernetes groups
```

Then Kubernetes RBAC controls cluster permissions.

## 28.3 GitLab CI/CD

GitLab can issue OIDC-compatible job tokens for workload federation. AWS trust policies should restrict project, namespace, branch, tag, ref type, or environment claims according to GitLab’s current token claim model.

## 28.4 HCP Terraform or another automation platform

A remote infrastructure automation platform can issue a workload token. AWS verifies it and grants a role only for a specific organization, project, workspace, or run phase.

The design principle is the same:

```text
Exact issuer
+ exact audience
+ controlled subject/context
+ temporary credentials
+ least-privilege role
```

## 28.5 Web application SSO

A web application can delegate login to an OIDC provider:

```text
User
  -> application
  -> provider login
  -> authorization code
  -> token endpoint
  -> ID-token validation
  -> local application session
```

The application should create its own secure session after validating the OIDC response rather than repeatedly exposing the ID token to browser components.

---

# 29. OIDC security rules and best practices

## Rule 1: Validate the exact issuer

Do not accept a token from an unconfigured issuer.

```text
Expected:
https://login.example.com/realms/engineering

Not automatically equivalent:
https://login.example.com
https://login.example.com/
https://login.example.com/realms/other
```

## Rule 2: Validate the audience

A token signed by the right issuer but issued for another application must be rejected.

For IRSA:

```text
aud = sts.amazonaws.com
```

For direct EKS human OIDC:

```text
aud = configured EKS OIDC client ID
```

## Rule 3: Restrict the subject or tenant context

For IRSA:

```text
system:serviceaccount:payments:invoice-reader
```

For GitHub:

```text
repo:example-org/payments-api:ref:refs/heads/main
```

For a private platform issuer:

```text
workload:platform:deployment-controller
```

## Rule 4: Treat shared issuers differently

When many customers use the same issuer URL, identify your tenant or resource through claims.

Trusting a shared issuer without tenant constraints can allow identities from another customer to request your role.

## Rule 5: Use short-lived tokens and credentials

Short lifetimes reduce the window after theft, removal from a group, repository compromise, or workload deletion.

## Rule 6: Never log bearer tokens

Redact:

```text
Authorization headers
ID tokens
Access tokens
Refresh tokens
Projected ServiceAccount tokens
AWS session tokens
```

## Rule 7: Use Authorization Code with PKCE

For interactive public clients, PKCE protects authorization codes against interception.

## Rule 8: Validate `state` and `nonce`

Generate high-entropy values, bind them to the request, and compare them on return.

## Rule 9: Register exact redirect URIs

Prefer:

```text
https://portal.example.com/oauth/callback
```

Avoid broad wildcards:

```text
https://portal.example.com/*
```

## Rule 10: Keep authorization separate

OIDC identifies. IAM policies, EKS access policies, Kubernetes RBAC, and application roles authorize.

## Rule 11: Do not use ID tokens as generic API tokens

Use the token type expected by the receiving component.

## Rule 12: Protect refresh tokens more strongly

Refresh tokens can maintain long-term access. Store them only in secure server-side or platform-protected storage when possible.

## Rule 13: Pin algorithms

Use an explicit algorithm allow-list. Do not let an attacker choose a weaker or unexpected validation path through the token header.

## Rule 14: Support key rotation

Cache JWKS with controlled refresh. On an unknown `kid`, refresh once and retry safely rather than accepting the token without verification.

## Rule 15: Use stable identifiers for authorization

Prefer controlled immutable IDs over mutable display names or email addresses when possible.

## Rule 16: Separate production and non-production trust

Use separate:

- IAM roles.
- OIDC clients.
- Audiences.
- GitHub environments.
- EKS clusters.
- Policies.
- Accounts where appropriate.

## Rule 17: Use one workload identity per permission boundary

Do not reuse one broadly privileged Kubernetes ServiceAccount for unrelated applications.

## Rule 18: Minimize node-role permissions

With IRSA or Pod Identity, application AWS permissions should move away from the worker-node role.

## Rule 19: Apply Kubernetes isolation controls

Use:

- Non-root containers.
- Read-only root filesystems when possible.
- Restricted Linux capabilities.
- Seccomp.
- Pod Security Admission.
- NetworkPolicy.
- Dedicated nodes for sensitive workloads.
- Admission policies.
- Runtime monitoring.

## Rule 20: Audit both sides of federation

Monitor:

- Identity-provider login and token events.
- IAM role-assumption events.
- CloudTrail.
- EKS control-plane audit logs.
- Kubernetes RBAC changes.
- GitHub workflow changes.
- IAM policy and trust-policy changes.
- Identity Center assignments and provisioning events.

## Rule 21: Protect trust-policy changes

An attacker who cannot assume a role today may gain access by weakening the trust policy.

Use:

- Infrastructure as code.
- Pull-request review.
- IAM Access Analyzer.
- AWS Config rules where appropriate.
- SCPs and permission boundaries.
- Change alerts.

## Rule 22: Test negative cases

Verify that these fail:

- Wrong issuer.
- Wrong audience.
- Wrong namespace.
- Wrong ServiceAccount.
- Wrong repository.
- Wrong branch.
- Expired token.
- Missing required claim.
- User removed from privileged group.
- Token from another tenant.

---

# 30. Common mistakes and misconceptions

## Mistake 1: “OIDC and OAuth are the same”

OIDC uses OAuth 2.0 but adds identity and authentication semantics.

## Mistake 2: “A JWT is automatically trustworthy”

A JWT is just a token format until its signature and claims are validated against a trusted issuer.

## Mistake 3: “Decoding verifies a token”

Base64URL decoding proves nothing about authenticity.

## Mistake 4: “Creating an IAM OIDC provider grants access”

The IAM role trust policy and permissions policy are still required.

## Mistake 5: “OIDC gives a pod AWS permissions directly”

The pod receives temporary credentials for an IAM role. That role’s policies provide AWS permissions.

## Mistake 6: “IRSA and EKS external OIDC are the same”

IRSA authenticates Kubernetes workloads to AWS STS.

External EKS OIDC authenticates human users to the Kubernetes API.

## Mistake 7: “IAM Identity Center uses OIDC for normal external workforce login”

The standard external IdP integration uses SAML 2.0 for authentication and SCIM for provisioning.

## Mistake 8: “A valid token for the issuer is enough”

The audience and identity/context claims must also match.

## Mistake 9: “Email is always a permanent identity”

Email addresses can change or be recycled.

## Mistake 10: “The node role is good enough for all pods”

This usually violates least privilege and increases lateral-movement risk.

## Mistake 11: “The `aws-auth` ConfigMap is the current best method”

AWS recommends EKS access entries for IAM principal access. `aws-auth` is deprecated for that use.

## Mistake 12: “The token is encrypted because it is signed”

A signed JWT payload is commonly readable.

## Mistake 13: “Any wildcard is harmless because permissions are narrow”

A wildcard in the trust policy may allow an unintended external identity to obtain the role’s permissions.

## Mistake 14: “Removing a group immediately invalidates every token”

Existing tokens may remain valid until expiration unless the architecture supports active revocation or introspection and uses it.

## Mistake 15: “OIDC replaces application sessions”

A web application normally validates OIDC and then creates a secure local session. It should not expose raw identity tokens unnecessarily.

---

# 31. Troubleshooting

## 31.1 General OIDC debugging order

Check in this order:

```text
1. Issuer URL
2. Discovery document
3. JWKS reachability
4. Token signature
5. Token algorithm and key ID
6. Audience
7. Subject
8. Expiration/not-before
9. Required claims
10. Role trust policy or EKS OIDC configuration
11. Authorization policy/RBAC
12. Network and proxy behavior
13. Audit logs
```

## 31.2 Decode a token safely

Do not paste production tokens into public websites.

Local Python example for inspection only:

```python
import base64
import json
import sys

token = sys.stdin.read().strip()
parts = token.split(".")

if len(parts) != 3:
    raise SystemExit("Not a three-part JWT")

def decode_part(value: str) -> dict:
    padding = "=" * (-len(value) % 4)
    raw = base64.urlsafe_b64decode(value + padding)
    return json.loads(raw)

print(json.dumps(decode_part(parts[0]), indent=2))
print(json.dumps(decode_part(parts[1]), indent=2))
```

This only decodes. It does **not** verify the signature.

## 31.3 IRSA: pod is using the node role

Check ServiceAccount:

```bash
kubectl get pod irsa-test \
  -n payments \
  -o jsonpath='{.spec.serviceAccountName}{"\n"}'
```

Check annotation:

```bash
kubectl get serviceaccount invoice-reader \
  -n payments \
  -o jsonpath='{.metadata.annotations.eks\.amazonaws\.com/role-arn}{"\n"}'
```

Check environment:

```bash
kubectl exec -n payments irsa-test -- env | \
  grep -E 'AWS_ROLE_ARN|AWS_WEB_IDENTITY_TOKEN_FILE'
```

Check identity:

```bash
kubectl exec -n payments irsa-test -- \
  aws sts get-caller-identity
```

Likely causes:

- Wrong ServiceAccount.
- Missing annotation.
- Pod was created before annotation and not restarted.
- Old SDK that does not support web-identity credentials.
- Application explicitly configured another credential source earlier in the chain.
- Host networking or metadata access exposes node credentials and the SDK selects them.
- Role trust-policy mismatch.

## 31.4 IRSA: `AccessDenied` on `AssumeRoleWithWebIdentity`

Inspect:

```bash
aws iam get-role \
  --role-name EksPaymentsInvoiceReader \
  --query Role.AssumeRolePolicyDocument
```

Compare exactly:

```text
Provider ARN
Issuer host/path
aud = sts.amazonaws.com
sub = system:serviceaccount:payments:invoice-reader
```

Common errors:

- Namespace typo.
- ServiceAccount typo.
- Provider from another cluster.
- `https://` incorrectly included in a condition-key prefix.
- Wrong AWS account ID.
- `StringEquals` value does not match.
- Role annotation points to another role.
- OIDC provider was never created.

## 31.5 IRSA: AWS API call denied after successful role assumption

If `aws sts get-caller-identity` returns the correct role, OIDC authentication succeeded.

Then investigate authorization:

- Role permissions policies.
- Permission boundaries.
- Resource policies.
- AWS Organizations SCPs.
- KMS key policies.
- VPC endpoint policies.
- Session policies.
- Explicit denies.
- Correct ARN and region.

## 31.6 EKS Pod Identity not working

Check agent:

```bash
kubectl get pods \
  -n kube-system \
  -l app.kubernetes.io/name=eks-pod-identity-agent
```

Check association:

```bash
aws eks list-pod-identity-associations \
  --cluster-name platform-dev
```

Inspect role trust:

```bash
aws iam get-role \
  --role-name EksPaymentsInvoiceReader \
  --query Role.AssumeRolePolicyDocument
```

Expected principal:

```json
"Service": "pods.eks.amazonaws.com"
```

Expected actions:

```json
[
  "sts:AssumeRole",
  "sts:TagSession"
]
```

Also verify:

- Namespace and ServiceAccount in the association.
- Supported SDK version.
- Default credential chain.
- Node networking for the agent.
- The pod was restarted.
- Cached credentials have not delayed a role change.

## 31.7 External EKS OIDC: login succeeds but Kubernetes returns forbidden

Authentication worked. RBAC denied the action.

Inspect identity mapping and bindings:

```bash
kubectl get rolebinding,clusterrolebinding -A
```

Test:

```bash
kubectl auth can-i list pods \
  -n development \
  --as="oidc:alice@example.com" \
  --as-group="oidc:developers"
```

Check:

- Username claim.
- Username prefix.
- Groups claim.
- Groups prefix.
- Exact group in RoleBinding.
- Namespace.
- Role verbs and resources.

## 31.8 External EKS OIDC: unauthorized

Investigate:

- Issuer URL mismatch.
- Issuer not publicly reachable from EKS control plane.
- Unsupported/self-signed certificate.
- Wrong client ID/audience.
- Expired ID token.
- Wrong token type.
- Missing required claim.
- Signature key rotation and JWKS reachability.
- Login helper returning an access token when EKS expects the configured ID-token semantics.
- Clock skew.

## 31.9 GitHub Actions cannot assume role

Inspect trust policy:

```bash
aws iam get-role \
  --role-name GitHubPaymentsDeployment \
  --query Role.AssumeRolePolicyDocument
```

Verify:

- Provider ARN.
- `aud`.
- Exact `sub`.
- Organization and repository spelling.
- Branch/tag/environment context.
- Workflow has:

```yaml
permissions:
  id-token: write
  contents: read
```

- The workflow is not running from an untrusted context excluded by policy.
- The action version is current and configured correctly.

## 31.10 IAM Identity Center SAML works, but assignments are missing

Check:

- User and group provisioning.
- SCIM status.
- Exact username attribute mapping.
- Group membership.
- Permission-set assignment.
- Account assignment provisioning status.
- Whether the identity source was recently changed.
- Whether the user exists twice with mismatched identifiers.

## 31.11 Useful logs

- AWS CloudTrail.
- EKS control-plane audit logs.
- Identity-provider system logs.
- GitHub Actions job logs, with tokens redacted.
- Kubernetes API audit logs.
- Application authentication logs.
- IAM Access Analyzer findings.
- AWS Config and Security Hub findings where configured.

---

# 32. Architecture decision guide

## 32.1 Pod needs AWS API access

Use:

```text
EKS Pod Identity
```

as the first option to evaluate for a new standard EKS design.

Use or retain:

```text
IRSA
```

when existing integrations, multi-platform compatibility, or organizational design make it preferable.

Do not use:

```text
Static IAM access keys stored in a Kubernetes Secret
```

except for a narrowly justified legacy scenario with a documented migration plan.

## 32.2 Employee needs AWS account access

Use:

```text
IAM Identity Center
+ corporate external IdP
+ SAML
+ SCIM
+ permission sets
```

## 32.3 Employee authenticated through Identity Center needs EKS

Use:

```text
IAM Identity Center role
+ EKS access entry
+ EKS access policy or Kubernetes RBAC
```

## 32.4 Employee needs direct corporate OIDC login to Kubernetes

Use:

```text
EKS external OIDC identity-provider association
+ kubectl credential plugin
+ Kubernetes RBAC
```

Remember that this direct OIDC identity does not automatically grant AWS API permissions.

## 32.5 GitHub Actions needs AWS access

Use:

```text
GitHub OIDC
+ IAM OIDC provider
+ exact trust-policy conditions
+ AWS STS temporary role
```

## 32.6 Application user needs login

Use an OIDC provider such as:

```text
Amazon Cognito
Microsoft Entra ID
Okta
Auth0
Keycloak
```

Use Authorization Code with PKCE and secure application sessions.

## 32.7 External application must preserve workforce identity into supported AWS applications

Evaluate:

```text
IAM Identity Center trusted token issuer
+ trusted identity propagation
```

---

# 33. Hands-on learning exercises

## Exercise 1: Inspect OIDC discovery

1. Choose a non-sensitive test issuer.
2. Fetch `/.well-known/openid-configuration`.
3. Identify the issuer, token endpoint, authorization endpoint, and JWKS URI.
4. Fetch the JWKS.
5. Identify key IDs and signing algorithms.

Success criteria:

- You can explain the relationship between discovery metadata and JWT verification.

## Exercise 2: Decode a test ID token locally

1. Obtain a test token.
2. Decode header and payload locally.
3. Identify `iss`, `sub`, `aud`, `exp`, and `nonce`.
4. Explain why decoding alone is not validation.

Success criteria:

- You can identify all mandatory validation decisions.

## Exercise 3: Deploy IRSA

1. Create a test S3 bucket.
2. Register the EKS OIDC provider.
3. Create a narrow read-only IAM policy.
4. Create role and ServiceAccount.
5. Run AWS CLI in a pod.
6. Verify the role ARN.
7. Confirm a denied write operation.

Success criteria:

- Read succeeds.
- Write fails.
- Pod uses the workload role rather than the node role.

## Exercise 4: Break IRSA deliberately

Change the trust policy subject from:

```text
system:serviceaccount:payments:invoice-reader
```

to a wrong name.

Recreate the pod and observe the error. Restore the policy.

Success criteria:

- You understand how the `sub` condition protects the role.

## Exercise 5: EKS Pod Identity comparison

1. Install Pod Identity Agent.
2. Create an equivalent Pod Identity role.
3. Create association.
4. Remove IRSA annotation in a test workload.
5. Confirm identity.
6. Compare CloudTrail and configuration objects.

Success criteria:

- You can explain the operational differences between the two mechanisms.

## Exercise 6: Kubernetes OIDC RBAC

1. Configure a test external provider.
2. Associate it with a non-production EKS cluster.
3. Map a test group.
4. Create namespace-only view access.
5. Confirm allowed and denied operations.

Success criteria:

- The user can list pods in one namespace but not read Secrets or access other namespaces.

## Exercise 7: GitHub OIDC

1. Create a non-production role.
2. Restrict trust to one repository and branch.
3. Run `aws sts get-caller-identity`.
4. Attempt from another branch and confirm denial.
5. Move production deployment to a protected environment.

Success criteria:

- No permanent AWS credential exists in GitHub secrets.
- Unapproved contexts cannot assume the role.

---

# 34. Production-readiness checklist

## OIDC provider

- [ ] Issuer is documented and owned by the expected organization or vendor.
- [ ] Discovery endpoint is reachable and monitored.
- [ ] JWKS endpoint is reachable and supports key rotation.
- [ ] TLS certificate chain is valid.
- [ ] Accepted signing algorithms are explicitly defined.
- [ ] Token lifetimes are documented.
- [ ] Incident and key-compromise procedures exist.

## Token validation

- [ ] Signature is verified.
- [ ] Exact issuer is validated.
- [ ] Audience is validated.
- [ ] Authorized party is validated when applicable.
- [ ] Expiration and not-before are validated.
- [ ] Nonce is validated for interactive OIDC.
- [ ] Required claims are validated.
- [ ] Token type is validated.
- [ ] Tokens are redacted from logs.

## AWS IAM OIDC federation

- [ ] IAM OIDC provider exists in the correct account.
- [ ] Role trust policy uses the correct provider ARN.
- [ ] `sts:AssumeRoleWithWebIdentity` is the intended action.
- [ ] Audience is restricted.
- [ ] Subject/tenant/repository context is restricted.
- [ ] Shared-provider identity controls are satisfied.
- [ ] Role permissions follow least privilege.
- [ ] Permission boundaries and SCPs are reviewed.
- [ ] CloudTrail is enabled and monitored.

## IRSA

- [ ] Correct EKS cluster issuer is registered.
- [ ] Exact namespace and ServiceAccount are in trust policy.
- [ ] ServiceAccount annotation has the correct role ARN.
- [ ] Pod uses `serviceAccountName`.
- [ ] SDK supports web identity.
- [ ] Application uses default credential chain.
- [ ] Node role does not retain unnecessary application permissions.
- [ ] Negative test with wrong ServiceAccount fails.

## EKS Pod Identity

- [ ] Pod Identity Agent is installed or platform-integrated.
- [ ] SDK version is supported.
- [ ] Association has correct cluster, namespace, ServiceAccount, and role.
- [ ] Role trusts `pods.eks.amazonaws.com`.
- [ ] Role permits `sts:AssumeRole` and `sts:TagSession`.
- [ ] Request-tag restrictions are applied where appropriate.
- [ ] Session-tag/ABAC design is reviewed.
- [ ] Cross-account target-role trust is reviewed.

## Human EKS authentication

- [ ] Identity source choice is documented: IAM access entries or external OIDC.
- [ ] External issuer is publicly reachable when direct EKS OIDC is used.
- [ ] Username and group claims are stable.
- [ ] Prefixes avoid collisions and do not use `system:`.
- [ ] RBAC is namespace-scoped by default.
- [ ] ClusterRoleBindings are minimized.
- [ ] Control-plane audit logging is enabled.
- [ ] Break-glass access exists and is tested.

## IAM Identity Center

- [ ] Standard external workforce authentication uses SAML 2.0.
- [ ] SCIM provisioning is configured or manual lifecycle ownership is documented.
- [ ] Permission sets are least privilege.
- [ ] Group-based assignments are preferred.
- [ ] Administrative and break-glass identities are protected.
- [ ] Identity-source migration plan is tested.
- [ ] Trusted token issuers are used only for a supported propagation use case.

## CI/CD

- [ ] No permanent AWS keys are stored when OIDC is supported.
- [ ] Trust is limited to expected repository/project.
- [ ] Branch, tag, or environment is restricted.
- [ ] Production approval controls exist.
- [ ] Workflow files are protected.
- [ ] External actions are reviewed and pinned.
- [ ] Pull-request execution boundaries are understood.
- [ ] Deployment role permissions are narrow.

---

# 35. Glossary

**Access token**
A credential used to access a protected API.

**Audience (`aud`)**
The intended recipient of a token.

**Authentication**
The process of verifying identity.

**Authorization**
The process of deciding what an identity may do.

**Authorization Code flow**
An OAuth/OIDC flow in which the client receives a short-lived authorization code and exchanges it at the token endpoint.

**Bearer token**
A token usable by whoever possesses it.

**Claim**
A name/value statement in a token.

**Client ID**
An identifier for an application registered with an authorization server.

**Confidential client**
A client capable of protecting credentials, commonly a server-side application.

**Discovery document**
OIDC metadata published at a well-known URL.

**EKS access entry**
An EKS resource that associates an IAM principal with Kubernetes permissions.

**EKS Pod Identity**
An EKS-managed mechanism that associates a Kubernetes ServiceAccount with an IAM role through the EKS Auth API and Pod Identity Agent.

**Federation**
Trusting an external identity system.

**ID token**
An OIDC security token containing claims about authentication and identity.

**Identity provider / IdP**
A system that authenticates identities. In OIDC terminology, the issuer is often called an OpenID Provider.

**IAM OIDC provider**
An AWS IAM resource representing trust in an external OIDC issuer.

**IRSA**
IAM Roles for Service Accounts.

**Issuer (`iss`)**
The authority that issued the token.

**JSON Web Key Set / JWKS**
A JSON document containing public keys used to verify JWT signatures.

**JSON Web Token / JWT**
A compact token format with header, payload, and signature.

**Nonce**
A request-bound random value used to mitigate token replay and substitution.

**OAuth 2.0**
An authorization framework for delegated access.

**OIDC**
OpenID Connect, an authentication protocol built on OAuth 2.0.

**OpenID Provider / OP**
An OIDC issuer that authenticates identities and issues ID tokens.

**Permission set**
An IAM Identity Center template used to create and assign AWS account permissions.

**PKCE**
Proof Key for Code Exchange, which binds authorization-code redemption to the initiating client.

**Projected ServiceAccount token**
A time-limited signed Kubernetes token mounted into a pod.

**Public client**
A client that cannot safely protect a permanent client secret, such as a CLI or native application.

**Relying Party / RP**
An application that trusts an OpenID Provider.

**Refresh token**
A sensitive token used to obtain new access tokens.

**RoleBinding**
A Kubernetes RBAC object granting Role or ClusterRole permissions within one namespace.

**SAML 2.0**
An XML-based enterprise identity-federation standard.

**SCIM 2.0**
A standard for provisioning and synchronizing users and groups.

**ServiceAccount**
A Kubernetes identity for processes running in pods.

**Subject (`sub`)**
The principal represented by a token.

**Trust policy**
The resource-based policy attached to an IAM role that defines who may assume it.

**Trusted identity propagation**
An IAM Identity Center capability that preserves workforce identity context across supported application and AWS service calls.

**Trusted token issuer**
An external OAuth 2.0 authorization server configured in IAM Identity Center for trusted identity propagation.

**Web identity federation**
Exchanging an external web identity token for temporary AWS role credentials.

---

# 36. Official references

The following sources were used to verify and extend this guide.

## OpenID and IETF standards

1. [OpenID Connect Core 1.0 incorporating errata set 2](https://openid.net/specs/openid-connect-core-1_0.html)
2. [OAuth 2.0 Authorization Framework — RFC 6749](https://www.rfc-editor.org/info/rfc6749)
3. [Proof Key for Code Exchange — RFC 7636](https://www.rfc-editor.org/info/rfc7636)
4. [OAuth 2.0 for Native Apps — RFC 8252](https://www.rfc-editor.org/info/rfc8252)
5. [OAuth 2.0 Security Best Current Practice — RFC 9700](https://www.rfc-editor.org/info/rfc9700)
6. [JSON Web Token — RFC 7519](https://www.rfc-editor.org/info/rfc7519)

## AWS IAM and STS

7. [OIDC federation in AWS IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html)
8. [Create an IAM OIDC identity provider](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)
9. [Create a role for OIDC federation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html)
10. [Identity-provider controls for shared OIDC providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc_secure-by-default.html)
11. [STS AssumeRoleWithWebIdentity API](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html)
12. [AWS CLI create-open-id-connect-provider](https://docs.aws.amazon.com/cli/latest/reference/iam/create-open-id-connect-provider.html)
13. [Obtain an OIDC provider thumbprint](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html)

## Amazon EKS

14. [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
15. [Create an IAM OIDC provider for an EKS cluster](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html)
16. [Assign IAM roles to Kubernetes service accounts](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html)
17. [Use IRSA with AWS SDKs](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts-minimum-sdk.html)
18. [Fetch EKS OIDC signing keys](https://docs.aws.amazon.com/eks/latest/userguide/irsa-fetch-keys.html)
19. [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)
20. [Set up the EKS Pod Identity Agent](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-agent-setup.html)
21. [Create the IAM role for EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html)
22. [Create a Pod Identity association](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-association.html)
23. [Compare Kubernetes workload access mechanisms](https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html)
24. [Grant users access to EKS with an external OIDC provider](https://docs.aws.amazon.com/eks/latest/userguide/authenticate-oidc-identity-provider.html)
25. [EKS access entries](https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html)
26. [Grant IAM users and roles access to Kubernetes APIs](https://docs.aws.amazon.com/eks/latest/userguide/grant-k8s-access.html)
27. [Amazon EKS identity and access management best practices](https://docs.aws.amazon.com/eks/latest/best-practices/identity-and-access-management.html)

## IAM Identity Center

28. [External identity providers in IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html)
29. [Connect an external identity provider](https://docs.aws.amazon.com/singlesignon/latest/userguide/how-to-connect-idp.html)
30. [SAML and SCIM identity federation](https://docs.aws.amazon.com/singlesignon/latest/userguide/other-idps.html)
31. [SCIM automatic provisioning](https://docs.aws.amazon.com/singlesignon/latest/userguide/provision-automatically.html)
32. [Trusted identity propagation overview](https://docs.aws.amazon.com/singlesignon/latest/userguide/trustedidentitypropagation-overview.html)
33. [Set up a trusted token issuer](https://docs.aws.amazon.com/singlesignon/latest/userguide/setuptrustedtokenissuer.html)
34. [Trusted token issuer configuration settings](https://docs.aws.amazon.com/singlesignon/latest/userguide/trusted-token-issuer-configuration-settings.html)

## Kubernetes

35. [Kubernetes authentication](https://kubernetes.io/docs/reference/access-authn-authz/authentication/)
36. [Kubernetes ServiceAccounts](https://kubernetes.io/docs/concepts/security/service-accounts/)
37. [Configure ServiceAccounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)
38. [Kubernetes RBAC authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

## GitHub Actions

39. [GitHub Actions OIDC concepts](https://docs.github.com/actions/concepts/security/openid-connect)
40. [Configure OIDC in AWS](https://docs.github.com/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)

## Terraform

41. [Terraform AWS IAM OIDC provider resource](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_openid_connect_provider)

---

## Final mental model

```text
OIDC provider
    proves identity by issuing a signed token

Relying party
    validates issuer, signature, audience, time, and claims

AWS IAM role trust policy
    decides whether that identity may assume the role

AWS STS
    exchanges the trusted token for temporary AWS credentials

IAM permissions policies
    decide what the role session may do in AWS

Kubernetes RBAC
    decides what an authenticated Kubernetes identity may do in the cluster
```

For Amazon EKS:

```text
Pod -> AWS:
    Prefer evaluating EKS Pod Identity for new EKS designs
    or use IRSA with the cluster OIDC issuer

Human -> Kubernetes:
    IAM role + EKS access entry
    or direct external OIDC + Kubernetes RBAC

Human -> AWS accounts:
    IAM Identity Center + SAML + SCIM + permission sets

CI/CD -> AWS:
    External OIDC issuer + narrow IAM trust + temporary STS credentials
```
