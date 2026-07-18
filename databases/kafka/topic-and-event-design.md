# Topic and event design

## Purpose

Use this page to design Kafka topics and events that are understandable, replayable, and operable.

## Topic design checklist

| Decision | Guidance | Risk if ignored |
| --- | --- | --- |
| Event boundary | Model one business fact per event. | Consumers receive ambiguous or overloaded data. |
| Key | Choose a key that matches ordering needs. | Related events may be processed out of order. |
| Partitions | Start from throughput and consumer parallelism needs. | Too few limits scaling; too many increases cost and complexity. |
| Retention | Set retention from replay and compliance needs. | Data disappears before consumers can recover. |
| Schema | Version event contracts intentionally. | Producers and consumers break each other silently. |

## Event contract habits

- Include stable identifiers, timestamps, event type, schema version, and producer name.
- Treat events as immutable facts.
- Add fields compatibly when possible.
- Avoid making consumers depend on undocumented producer internals.

## Delivery and replay

Kafka supports replay by keeping records for a retention window. Replay is useful for rebuilding projections, recovering consumers, and testing new consumers. It also means consumers must be idempotent when duplicate processing is possible.

> [!IMPORTANT]
> At-least-once processing can produce duplicate side effects unless the consumer uses idempotency keys, transactions, or another duplicate-safe design.

## Related links

- [Kafka fundamentals](fundamentals.md)
- [Kafka operations](operations.md)
- [Apache Kafka documentation](https://kafka.apache.org/documentation/)
- [Back to Kafka index](README.md)
- [Back to databases index](../README.md)
- [Back to root index](../../README.md)
