"""Check declared fixture relationships; this does not prove a process is listening."""
import json
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).parent

def matches_teaching_fixture_contract(service, deployment):
    pod = deployment["spec"]["template"]
    selector = service["spec"]["selector"]
    matches = all(pod["metadata"]["labels"].get(key) == value for key,value in selector.items())
    ports = {p["containerPort"] for c in pod["spec"]["containers"] for p in c.get("ports", [])}
    return bool(selector) and matches and all(p.get("targetPort", p["port"]) in ports for p in service["spec"]["ports"])

class RoutingFixtures(unittest.TestCase):
    def test_semantic_difference_and_behavior_contract(self):
        good = json.loads((ROOT/"service.json").read_text())
        reordered = json.loads((ROOT/"service-reordered.json").read_text())
        bad = json.loads((ROOT/"service-broken.json").read_text())
        app = yaml.safe_load((ROOT/"app.yaml").read_text())
        self.assertEqual(good, reordered)
        self.assertNotEqual(good, bad)
        self.assertTrue(matches_teaching_fixture_contract(good, app))
        self.assertFalse(matches_teaching_fixture_contract(bad, app))
        bad_selector = json.loads(json.dumps(good))
        bad_selector["spec"]["selector"]["app"] = "missing"
        self.assertFalse(matches_teaching_fixture_contract(bad_selector, app))
        self.assertEqual(app["metadata"]["labels"]["team"], "platform")

if __name__ == "__main__":
    unittest.main()
