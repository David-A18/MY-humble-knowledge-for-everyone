"""Kafka offset ordering contract; requires the pinned kafka-python dependency."""
from contextlib import redirect_stdout
from io import StringIO
import json
from types import SimpleNamespace
import unittest
from aggregate import Aggregator
from consume import consume

class FakeConsumer:
    def __init__(self, messages, fail=False):
        self.messages, self.commits, self.fail = messages, [], fail
    def __iter__(self):
        return iter(self.messages)
    def commit(self, positions):
        self.commits.append(positions)
        if self.fail:
            raise RuntimeError('simulated offset-commit failure')

def message(offset, identity='a'):
    event={'id':identity,'ts':10,'region':'eu','amount_cents':100}
    return SimpleNamespace(topic='orders',partition=0,offset=offset,value=json.dumps(event).encode())

class OffsetContracts(unittest.TestCase):
    def test_only_processed_offsets_are_committed(self):
        state=Aggregator(':memory:')
        consumer=FakeConsumer([message(0),message(1,'b')])
        try:
            with redirect_stdout(StringIO()):
                consume(consumer,state)
            self.assertEqual([next(iter(x.values())).offset for x in consumer.commits],[1,2])
        finally:
            state.close()

    def test_replay_after_commit_failure_does_not_double_count(self):
        state=Aggregator(':memory:')
        try:
            with self.assertRaises(RuntimeError):
                consume(FakeConsumer([message(0)],fail=True),state)
            with redirect_stdout(StringIO()):
                consume(FakeConsumer([message(0)]),state)
            self.assertEqual(state.snapshot()['totals'][0]['count'],1)
        finally:
            state.close()

if __name__=='__main__':
    unittest.main()
