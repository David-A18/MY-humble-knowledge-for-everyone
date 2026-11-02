# Knowledge-quality test data

- [Retrieval cases](retrieval-cases.yaml) - Human task questions with their
  expected concept paths and evidence identifiers.

- [Unanswerable questions](unanswerable-questions.yaml) - Off-topic and near-miss
  questions the corpus cannot answer, used to test refusal.

[`validate-retrieval-cases.py`](../scripts/validate-retrieval-cases.py) checks that
the cases point at real concepts. [`evaluate-retrieval.py`](../scripts/evaluate-retrieval.py)
runs them through the [RAG lab](../knowledge/llm/rag/repository-lab.md) and fails CI
below the agreed floors:

```bash
python3 scripts/evaluate-retrieval.py --unanswerable tests/unanswerable-questions.yaml --min-hit-at-3 0.9 --min-refused 0.8
```

Hit@3 means an expected concept is among the first three distinct concepts. The
retrieval cases use wording close to the pages, so read a high score as a regression
guard, not as proof of natural-language quality.

[Back to repository index](../README.md)
