# News

Short, dated briefs on artificial intelligence, technology, and the economy:
what happened, why it matters to people who build and run software, and what to
do about it. Each brief links to its original sources and has an expiry date,
after which it is history rather than current advice.

## How the news works

- **Scope and cadence:** a weekly roundup of developments that change what
  readers can do, must do, or should plan for. See the
  [news editorial policy](../../governance/news-editorial-policy.md).
- **Format:** briefs live in `news/YYYY/MM/` and use the
  [news brief template](../templates/news-brief-template.md). The decision is
  recorded in [ADR-0006](../decision-records/adr-0006-news-briefs.md).
- **Trust:** news is never marked `stable`. Lasting guidance moves into the
  related concept page, and the brief links to it.

## Briefs

### Latest week of 23 November 2026

- [Kubernetes 1.38 preview flags node and kubectl changes](2026/11/kubernetes-1-38-upgrade-preview.md) - Check runtime compatibility and rehearse remote commands.
- [Amazon EKS 1.31 reaches the end of extended support](2026/11/eks-1-31-extended-support-end.md) - Check remaining clusters and their upgrade readiness.

### Week of 16 November 2026

- [OpenAI releases GPT-6.2 Astra and Sol](2026/11/openai-gpt-6-2-astra-and-sol.md)
- [Patch the critical Java vulnerability CVE-2026-114938](2026/11/critical-java-vulnerability-cve-2026-114938.md)
- [Federal Reserve minutes point to possible rate increases](2026/11/fed-minutes-signal-possible-rate-increase.md)
- [EU AI Act changes take effect on a new timeline](2026/11/eu-ai-act-new-prohibitions-december-2026.md)

### Archive

- [2026](2026/index.md)

## Contribute a brief

1. Copy the [news brief template](../templates/news-brief-template.md) into
   `news/YYYY/MM/` for the publication month.
2. Add a year and month `index.md` if they do not exist, and list the brief in
   them and on this page.
3. Add any new source domains to the reviewed
   [domain allowlist](../../governance/policy/allowed-link-domains.txt).
4. Run the checks in [AGENTS.md](../../AGENTS.md) and open a pull request.

[Back to knowledge index](../index.md)
