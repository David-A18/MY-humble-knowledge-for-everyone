from pathlib import Path
import tempfile
import unittest
from aggregate import Aggregator

def event(identity, timestamp, amount=100):
    return {"id": identity, "ts": timestamp, "region": "eu", "amount_cents": amount}

class AggregationContracts(unittest.TestCase):
    def test_restart_replay_and_conflicting_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = str(Path(directory)/"state.sqlite")
            state = Aggregator(filename)
            self.assertEqual(state.apply(event("a", 10)), "accepted")
            state.close()
            state = Aggregator(filename)
            try:
                self.assertEqual(state.apply(event("a", 10)), "duplicate")
                self.assertEqual(state.snapshot()["totals"][0]["amount_cents"], 100)
                with self.assertRaises(ValueError):
                    state.apply(event("a", 10, 999))
                self.assertEqual(state.snapshot()["totals"][0]["count"], 1)
            finally:
                state.close()

    def test_windows_out_of_order_and_lateness(self):
        state = Aggregator(":memory:")
        try:
            self.assertEqual(state.apply(event("a", 50)), "accepted")
            self.assertEqual(state.apply(event("b", 40)), "accepted")
            self.assertEqual(state.apply(event("c", 60)), "accepted")
            self.assertEqual(state.apply(event("d", 90)), "accepted")
            self.assertEqual(state.apply(event("late", 59)), "late")
            snap = state.snapshot()
            self.assertEqual(snap["watermark"], 60)
            self.assertTrue(snap["totals"][0]["finalized"])
            self.assertEqual(snap["totals"][0]["count"], 2)
            self.assertEqual(snap["late_count"], 1)
            with self.assertRaises(ValueError):
                state.apply({"id": "bad", "ts": True})
        finally:
            state.close()

if __name__ == "__main__":
    unittest.main()
