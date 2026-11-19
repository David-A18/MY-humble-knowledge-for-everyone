"""OTLP sender contract checks using a mocked receiver, not a running Collector."""
import importlib.util
from io import BytesIO, StringIO
from contextlib import redirect_stdout
import json
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("sender", Path(__file__).with_name("send-span.py"))
sender = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sender)

class SenderContracts(unittest.TestCase):
    def test_acceptance_and_payload(self):
        with patch.object(sender.urllib.request, "urlopen", return_value=BytesIO(b'{}')) as call:
            with redirect_stdout(StringIO()):
                sender.send()
            request = call.call_args.args[0]
            self.assertEqual(request.get_method(), "POST")
            span = json.loads(request.data)["resourceSpans"][0]["scopeSpans"][0]["spans"][0]
            self.assertEqual(len(span["traceId"]), 32)
            self.assertEqual(len(span["spanId"]), 16)
            self.assertGreater(int(span["endTimeUnixNano"]), int(span["startTimeUnixNano"]))

    def test_partial_rejection_is_failure(self):
        data = json.dumps({"partialSuccess": {"rejectedSpans": "1"}}).encode()
        with patch.object(sender.urllib.request, "urlopen", return_value=BytesIO(data)):
            with self.assertRaises(RuntimeError):
                sender.send()

    def test_connection_failure_propagates(self):
        with patch.object(sender.urllib.request, "urlopen", side_effect=sender.urllib.error.URLError("unavailable")):
            with self.assertRaises(sender.urllib.error.URLError):
                sender.send()

if __name__ == "__main__":
    unittest.main()
