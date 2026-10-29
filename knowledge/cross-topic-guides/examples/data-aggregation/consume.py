import json
import os
from kafka import KafkaConsumer
from kafka import TopicPartition
from kafka.structs import OffsetAndMetadata
from aggregate import Aggregator

def consume(consumer, state):
    for message in consumer:
        outcome = state.apply(json.loads(message.value))
        # Commit only the processed position: committing all fetched positions can lose work.
        consumer.commit({TopicPartition(message.topic, message.partition):
                         OffsetAndMetadata(message.offset + 1, "", -1)})
        print(json.dumps({"outcome": outcome, **state.snapshot()}), flush=True)

if __name__ == "__main__":
    consumer = KafkaConsumer("orders", bootstrap_servers=os.environ["BOOTSTRAP_SERVERS"],
                             group_id="kb-aggregate-v1", enable_auto_commit=False,
                             auto_offset_reset="earliest")
    state = Aggregator("/state/aggregate.sqlite")
    try:
        consume(consumer, state)
    finally:
        state.close()
        consumer.close()
