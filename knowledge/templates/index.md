# Templates

Reusable templates for adding focused lessons, procedures, references,
troubleshooting guides, and decisions without changing the knowledge
bundle's structure.

Use these templates together with the canonical [authoring instructions](../../instructions.md). They define page types, evidence rules, warning placement, and navigation rules.

| Reader needs to... | Template | New page `type` |
| --- | --- | --- |
| Understand how something works, or complete one known task. | [Knowledge article](knowledge-article-template.md): copy one of its two skeletons. | `Explanation` or `How-to Guide` |
| Learn by completing a disposable exercise. | [Tutorial](practical-example-template.md) | `Tutorial` |
| Look up command syntax and side effects. | [Command reference](command-reference-template.md) | `Reference` |
| Diagnose a visible symptom safely. | [Troubleshooting](troubleshooting-template.md) | `Troubleshooting Guide` |
| Understand why a repository or architecture choice was made. | [Architecture decision record](architecture-decision-record-template.md) | `Decision Record` |

## Add a topic that fits

1. Write down one reader question and the result the page should give.
   Choose the matching `type` from the [authoring
   instructions](../../instructions.md#choose-the-reader-outcome).
2. Find the closest topic in the [knowledge index](../index.md). Read
   its `index.md` and related concepts before adding another page. If
   no route fits, use the [source-ingestion route
   guide](../../sources/AGENTS.md) to decide whether an existing
   parent needs a new child directory.
3. Copy **one fenced skeleton** from a template into a lowercase
   kebab-case concept file. Replace every placeholder, audience, and
   title. The template page itself has `type: Template`; the copyable
   skeleton has the new concept's type. Create an `index.md` with no
   frontmatter for any new child directory. List the new page in its
   direct parent index. If that directory is new, list it in its own
   parent index too.
4. Explain the idea in plain language, then link specific official
   documentation for deeper study. Record sources, review dates, and
   execution evidence only when real; keep an incomplete page `draft`.
5. Rebuild the [catalog](../../generated/README.md) and run the
   repository's [required checks](../../AGENTS.md#validation-and-publication).

When a page needs two different reader outcomes, make two linked
concepts. For example, explain **what a tool does** in an Explanation
and show **how to complete one task** in a How-to Guide.

These templates do not yet include a dedicated Learning Path, Glossary
entry, or non-command Reference skeleton. Use the [authoring
instructions](../../instructions.md#choose-the-reader-outcome) and a
nearby concept of that type as a starting point for those cases.

[Back to knowledge index](../index.md) | [Repository README](../../README.md)
