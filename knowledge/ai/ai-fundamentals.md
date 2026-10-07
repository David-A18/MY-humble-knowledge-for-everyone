---
type: Explanation
title: AI fundamentals
description: Distinguish AI systems, machine learning, generative AI, language models, assistants, and agents through one small library example.
tags: [ai, machine-learning, generative-ai, llm, agents, fundamentals, beginner]
status: draft
maturity: draft
audience: Curious learners and beginning engineers
maintainer: unassigned
sources:
  - id: oecd-ai-principles
    resource: https://oecd.ai/en/ai-principles
    title: OECD AI Principles - AI system definition
  - id: oecd-ai-definition-memo
    resource: https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/03/explanatory-memorandum-on-the-updated-oecd-definition-of-an-ai-system_3c815e51/623da898-en.pdf
    title: OECD - Explanatory memorandum on the updated definition of an AI system
  - id: google-what-is-ml
    resource: https://developers.google.com/machine-learning/intro-to-ml/what-is-ml
    title: Google for Developers - What is machine learning?
  - id: google-ml-glossary
    resource: https://developers.google.com/machine-learning/glossary
    title: Google for Developers - Machine Learning Glossary
  - id: google-llm-introduction
    resource: https://developers.google.com/machine-learning/crash-course/llm/transformers
    title: Google for Developers - What's a large language model?
  - id: anthropic-effective-agents
    resource: https://www.anthropic.com/engineering/building-effective-agents
    title: Anthropic - Building effective agents
  - id: nist-genai-profile
    resource: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
    title: NIST AI 600-1 - Generative AI Profile
  - id: anthropic-consumer-data-use
    resource: https://privacy.claude.com/en/articles/10023555-how-do-you-use-personal-data-in-model-training
    title: Anthropic Privacy Center - How do you use personal data in model training?
---

# AI fundamentals

## Purpose

Read this before choosing an AI tool or trusting an AI-written answer. You
should leave able to distinguish an AI system, machine learning, generative
AI, a large language model, an assistant, and an agent. You should also be
able to explain why building a model differs from using one.

These words have overlapping uses. This page gives a beginner's working
model, grounded in the [OECD's AI system definition](https://oecd.ai/en/ai-principles).
The library example below is invented. No model was trained, queried, or
tested for it.

## What AI means here

An **AI system** takes input and works out an output for a goal. The output
may be a prediction, recommendation, decision, or new content. For example,
an email sorter predicts a category; a writing assistant produces a draft.
AI systems differ in how independently they operate.[^oecd-ai-principles]
An application built around a model may also include an interface,
instructions, data sources, tools, and a step where people review its output.

Not every AI system learns from examples. Some use explicit knowledge and
reasoning rules; many current systems use **machine learning (ML)**. In ML,
a training process uses data to build a **model** that can make predictions or
generate content on new input. **Inference** means using that model after it
has been built. During ordinary use, its learned internal values
(**parameters**, often called **weights**) usually stay
fixed; some systems are designed to adapt, and teams can train and release a
new version later.[^oecd-ai-definition-memo][^google-what-is-ml][^google-ml-glossary]

## Why the distinctions matter

If you treat every AI feature as the same thing, you can easily assume that
asking a question teaches the model, that a fluent sentence is a checked
fact, or that an agent can act without limits. Those assumptions change how
you protect data, review an answer, and decide which tools an application may
use. A generated answer can sound certain while being false; NIST calls this
**confabulation**.[^nist-genai-profile]

One request usually does not change the model you are using. That says
nothing about whether the application stores your input or whether a provider
may use it when training a future model. Product policies differ; check the
current data-use policy before submitting sensitive material. Anthropic's
consumer data-use notice is one concrete example of such a policy, not a
rule for every AI service.[^oecd-ai-definition-memo][^anthropic-consumer-data-use]

## The mental model: five different questions

| Question | Term | Plain meaning |
| --- | --- | --- |
| How was the model built? | Machine learning | Training uses data to build or adjust a model. Other AI approaches can use explicit knowledge and rules. |
| What does it produce? | Generative AI | A model creates content such as text, images, audio, or video. A classifier that only picks a label is ML, but not generative AI. |
| What kind of language model is it? | Large language model (LLM) | A model trained at large scale on language data. The generative LLMs here produce responses in tokens, small pieces of text or other encoded content. “Large” has no single cutoff in this guide. |
| How is a model presented in a conversation? | Assistant | An application presents a model through an interface and may add instructions, information, or tools. Other applications, such as a message router, need no chat assistant. |
| Who chooses the next step? | Agent | In one common meaning, the model directs a sequence of steps and tool calls instead of following only a fixed path. |

Generative AI includes more than LLMs. A model that generates an image is
generative too. Likewise, an LLM is a component of an assistant, not the whole
application. Anthropic distinguishes a fixed **workflow**, where code decides
the sequence, from an **agent**, where the model directs its next steps and
tool use. Other organizations use the word “agent” more broadly, so check
what a particular product actually lets it do.[^oecd-ai-definition-memo][^google-llm-introduction][^anthropic-effective-agents]

## An analogy: an apprentice sign painter

Imagine an apprentice who studies many examples of shop signs. Later a
customer asks for a new sign. The long study resembles **training**; making
this sign resembles **inference**. The apprentice can paint convincing words
without checking whether the shop really opens on Sunday. Giving the
apprentice access to the official shop-hours book gives them a way to check.
A ladder adds a tool for hanging a sign. Permission to use it on a real
shopfront is a separate decision. AI tool access and authorization are
separate too.

The analogy breaks in useful ways:

- A person may learn from each job. A deployed model's learned values usually
  do not change just because you asked a question. An application can retain
  a conversation or train a later model version; neither is the same as this
  inference call updating the model.[^oecd-ai-definition-memo]
- A person can visit the shop. A model cannot inspect a live record unless
  the application gives it a way to retrieve that record. A remembered
  pattern is not evidence for today's opening hours.
- A person chooses and uses physical tools directly. An AI agent acts only
  through the tools, permissions, and application flow people give it.
  More access changes the possible consequences of a mistake.[^anthropic-effective-agents]

## Example: the invented Riverside Library

The library wants to sort incoming messages and answer opening-hours
questions. These are two separate jobs:

1. **Build a sorter.** Staff label past messages as *membership*, *room
   booking*, or *lost item*. Training produces a classifier; staff check it
   on different messages it has not seen. It predicts one label and does not
   write a reply. This is ML, but it is not generative AI.
2. **Use the sorter.** A new message arrives. The classifier predicts *room
   booking* and the application routes it to the right queue. This is
   inference. That one prediction does not retrain the model. Staff can
   correct mistakes and use reviewed examples for a later training cycle.
3. **Draft an answer.** The library also uses a pre-trained LLM to draft a
   reply to a patron's web-form question about special-event hours. Without
   the current schedule, it might give plausible but wrong hours. The
   application fetches the published schedule, passes the relevant entry to
   the model, and shows staff a draft with a link to that entry. Staff verify
   the entry and answer before sending the reply. This is a fixed **workflow**:
   application code chooses when to fetch and review; the model does not
   choose those steps. A source link helps checking but does not guarantee
   that the draft interpreted it well.
4. **Consider an agent.** If the model instead chose when to call a
   read-only `get_schedule` tool, it could direct that lookup step. A separate
   `edit_booking` tool, if granted with write credentials, would let it
   change bookings. The library does not grant that tool in this example;
   any real write path would need its own access limits and human confirmation.

**End state:** the library trained one model for labels and used another for
draft text. Its fixed workflow checks the reply before sending it; the
optional agent path has only a read tool. This is a teaching example, not a claim about a real
library or a tested product.

## Visual: building a model and using it are separate

```mermaid
flowchart TD
    past[Past messages with staff labels] --> training[Train and check a classifier]
    training --> classifier[Saved classifier model]
    incoming[New message] --> classifier
    classifier --> category[Predicted category]
    category --> queue[Application routes message]
    visitor[Patron's hours question] --> assistant[Library application]
    assistant --> fetch[Fetch published schedule entry]
    fetch --> prompt[Question and entry form model input]
    assistant --> prompt
    prompt --> llm[Pre-trained language model]
    llm --> draft[Draft reply]
    draft --> show[Application shows draft and source link]
    fetch --> show
    show --> review[Staff compare answer with schedule]
    review --> send[Send checked reply]
```

**Text alternative:** Past labelled messages go through a training and
checking step to create a classifier. A new message goes through that saved
classifier, and the application routes its predicted category. Separately,
a patron's question reaches an application that fetches the published
schedule entry, sends the question and entry to a pre-trained language model,
then shows staff the draft and source link. Staff compare them before sending
a reply.
The diagram shows the fixed workflow, not the optional agent path. Use the two paths to decide whether a
task needs a newly trained model, an existing model, an up-to-date record,
or a human review step.

## Common misconceptions

- **“All AI is ML.”** Knowledge-based approaches can use explicit rules or
  representations instead of training a model from examples.[^oecd-ai-definition-memo]
- **“Generative AI is just chat.”** Images, audio, and video are also possible
  outputs.[^oecd-ai-definition-memo]
- **“The model learned my question.”** A normal inference call uses a model;
  it does not by itself change its learned values. Check the product's
  data-use policy separately.[^oecd-ai-definition-memo][^anthropic-consumer-data-use]
- **“A citation makes an answer true.”** Check that the source exists, is
  current for the question, and supports the exact claim.[^nist-genai-profile]
- **“An agent can do anything.”** Tools, credentials, and back-end checks
  bound its access. It can still make mistakes within that access, so grant
  only the capabilities it needs.[^anthropic-effective-agents]

## Check your understanding

1. Which Riverside model did staff train, and which did they only use?
2. Why is the message sorter ML but not generative AI?
3. Why can the assistant give wrong event hours even if its text is fluent?
4. Who chooses the schedule lookup in the library's fixed workflow? Who
   would choose it in the optional agent path, and what additional risk would
   `edit_booking` create?

## Next steps

- [AI tooling](ai-tooling/index.md) maps applications, tools, skills, and
  knowledge bases.
- [Model Context Protocol](ai-tooling/model-context-protocol.md) explains one
  way an AI application can reach tools and information.
- [Retrieval and context efficiency](ai-tooling/knowledge-bases/retrieval-and-context-efficiency.md)
  follows the search-to-source path behind a grounded answer.

The current AI section has no beginner hands-on tutorial for building either
library feature. Follow the official lessons below for guided ML practice.

## Official documentation for deeper study

- The [OECD AI Principles](https://oecd.ai/en/ai-principles) define an AI
  system; the [explanatory memorandum](https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/03/explanatory-memorandum-on-the-updated-oecd-definition-of-an-ai-system_3c815e51/623da898-en.pdf)
  explains learning-based and knowledge-based approaches, training, and use.
- Google's [introduction to ML](https://developers.google.com/machine-learning/intro-to-ml/what-is-ml)
  and [LLM lesson](https://developers.google.com/machine-learning/crash-course/llm/transformers)
  go deeper into trained models and text generation.
- [Anthropic's agent guide](https://www.anthropic.com/engineering/building-effective-agents)
  compares fixed workflows with model-directed tool use.
- [NIST's Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
  covers risks including confidently wrong output.
- [Anthropic's consumer data-use notice](https://privacy.claude.com/en/articles/10023555-how-do-you-use-personal-data-in-model-training)
  illustrates why input retention and future training are product-policy
  questions rather than properties of inference.

## Related links

- [AI index](index.md)
- [Start here](../start-here.md)
- [Root knowledge index](../index.md)

[^oecd-ai-principles]: [OECD AI Principles](https://oecd.ai/en/ai-principles), source record `oecd-ai-principles`.
[^oecd-ai-definition-memo]: [OECD explanatory memorandum on the AI system definition](https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/03/explanatory-memorandum-on-the-updated-oecd-definition-of-an-ai-system_3c815e51/623da898-en.pdf), source record `oecd-ai-definition-memo`.
[^google-what-is-ml]: [Google for Developers - What is machine learning?](https://developers.google.com/machine-learning/intro-to-ml/what-is-ml), source record `google-what-is-ml`.
[^google-ml-glossary]: [Google for Developers - Machine Learning Glossary](https://developers.google.com/machine-learning/glossary), source record `google-ml-glossary`.
[^google-llm-introduction]: [Google for Developers - What's a large language model?](https://developers.google.com/machine-learning/crash-course/llm/transformers), source record `google-llm-introduction`.
[^anthropic-effective-agents]: [Anthropic - Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), source record `anthropic-effective-agents`.
[^nist-genai-profile]: [NIST AI 600-1 - Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf), source record `nist-genai-profile`.
[^anthropic-consumer-data-use]: [Anthropic Privacy Center - How do you use personal data in model training?](https://privacy.claude.com/en/articles/10023555-how-do-you-use-personal-data-in-model-training), source record `anthropic-consumer-data-use`.
