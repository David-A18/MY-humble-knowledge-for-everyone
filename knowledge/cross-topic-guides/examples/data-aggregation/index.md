# Single-partition aggregation example

Use the [walkthrough](../../kubernetes-data-aggregation.md). `aggregate.py` implements durable deduplication and window totals; `consume.py` commits Kafka offsets after state. `test_aggregate.py` checks replay, lateness, boundaries, and conflicting IDs. `test_consume.py` checks per-message Kafka offsets and replay after a failed commit; it requires the pinned kafka-python dependency.

`kafka.yaml` is ephemeral/unsecured lab infrastructure. `consumer.yaml` uses one replica and a PVC; a default StorageClass is required. Do not scale replicas without redesigning partition/state ownership.

[Back to examples](../index.md) | [Back to root](../../../../README.md)
