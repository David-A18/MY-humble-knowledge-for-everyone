# Retrieval-augmented generation (RAG)

Learn when retrieval helps, how evidence reaches a language model, and how to measure correctness. The runnable Python lab searches this repository with SQLite FTS5/BM25 and optionally calls a local Ollama model.

## Learning path

Read in order, or choose a task from the table.

| Guide | Use it for |
| --- | --- |
| [Purpose and use cases](purpose-and-use-cases.md) | Choose RAG, search, long context, or fine-tuning. |
| [Ingestion and chunking](ingestion-and-chunking.md) | Prepare traceable, bounded evidence. |
| [Retrieval and reranking](retrieval-and-reranking.md) | Compare lexical, vector, hybrid, and reranked retrieval. |
| [Grounded generation and citations](grounded-generation.md) | Build bounded prompts and handle missing evidence. |
| [Evaluation, security, and operations](evaluation-security-and-operations.md) | Separate retrieval quality from answer quality. |
| [Repository-based Python lab](repository-lab.md) | Run retrieval, golden questions, and optional generation. |

## Related links

- [Runnable example files](examples/index.md)

- [Back to parent index](../index.md)
- [Back to root index](../../../README.md)
