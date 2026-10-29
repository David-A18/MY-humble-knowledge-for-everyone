"""Check reconciliation and misleading-savings edge cases using synthetic inputs."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("cost_analysis", HERE / "cost-analysis.py")
cost = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cost
spec.loader.exec_module(cost)


class CostExamples(unittest.TestCase):
    def test_fixture_reconciles_with_credit_and_unallocated_cost(self):
        rows = cost.load_ledger(HERE / "synthetic-ledger.csv")
        report = cost.allocation_report(rows, {"payments": D(3), "data": D(1)})
        self.assertEqual(report["source_total"], D("675.01"))
        self.assertEqual(report["final_net"], {"payments": D("420.01"), "data": D("230.00"), "__unallocated__": D("25.00")})

    def test_remainder_is_deterministic_and_reconciles(self):
        result = cost.allocate_shared(D("100.01"), {"c": D(1), "b": D(1), "a": D(1)})
        self.assertEqual(result, {"a": D("33.34"), "b": D("33.34"), "c": D("33.33")})
        self.assertEqual(sum(result.values()), D("100.01"))

    def test_shared_credit_reconciles(self):
        result = cost.allocate_shared(D("-0.01"), {"b": D(1), "a": D(1)})
        self.assertEqual(result["a"], D("-0.01"))
        self.assertEqual(sum(result.values()), D("-0.01"))

    def test_zero_weight_owner_receives_no_cost(self):
        self.assertEqual(cost.allocate_shared(D("1.00"), {"a": D(0), "b": D(2)}), {"a": D(0), "b": D(1)})

    def test_invalid_weights_are_rejected(self):
        for weights in [{}, {"a": D(0)}, {"a": D(-1)}, {"__unallocated__": D(1)}]:
            with self.subTest(weights=weights), self.assertRaises(ValueError):
                cost.allocate_shared(D("1.00"), weights)

    def test_normalization_distinguishes_bill_from_unit_improvement(self):
        result = cost.normalized_comparison(D(600), D(10000), D(660), D(15000))
        self.assertEqual(result["raw_cost_change"], D(60))
        self.assertEqual(result["before_unit_cost"], D("0.06"))
        self.assertEqual(result["after_unit_cost"], D("0.044"))
        self.assertEqual(result["modeled_cost_avoidance"], D(240))

    def test_quantity_and_rate_are_not_double_counted(self):
        result = cost.decompose_quantity_and_rate(D(100), D(80), D(1), D("0.75"))
        self.assertEqual(result["quantity_effect"], D(20))
        self.assertEqual(result["rate_effect_after_quantity_change"], D(20))
        self.assertEqual(result["combined_difference"], D(40))
        self.assertEqual(result["before_cost"] - result["after_cost"], D(40))

    def test_zero_business_units_are_not_free_unit_cost(self):
        self.assertIsNone(cost.unit_cost(D(100), D(0)))
        with self.assertRaises(ValueError):
            cost.normalized_comparison(D(100), D(0), D(90), D(5))

    def test_run_rate_and_invalid_periods(self):
        self.assertEqual(cost.linear_run_rate(D(960), 12, 30), D(2400))
        for elapsed, total in [(0, 30), (31, 30), (1, 0)]:
            with self.subTest(elapsed=elapsed), self.assertRaises(ValueError):
                cost.linear_run_rate(D(960), elapsed, total)

    def test_anomaly_thresholds_and_cold_start(self):
        self.assertTrue(cost.anomaly_candidate(D(100), D(160), D(50), D("0.20"))["candidate"])
        self.assertFalse(cost.anomaly_candidate(D(100), D(130), D(50), D("0.20"))["candidate"])
        cold = cost.anomaly_candidate(D(0), D(60), D(50), D("0.20"))
        self.assertTrue(cold["cold_start"])
        self.assertIsNone(cold["relative_change"])

    def test_nonfinite_or_binary_float_inputs_are_rejected(self):
        for value in ["NaN", "Infinity", 0.1, True]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                cost.decimal(value)

    def test_bad_ledgers_are_rejected(self):
        text = (HERE / "synthetic-ledger.csv").read_text(encoding="utf-8")
        variants = [text + text.splitlines()[1] + "\n", text.replace("demo-002,2026-09", "demo-002,2026-10"),
                    text.replace("USD", "EUR", 1), text.replace("300.00", "300.001", 1),
                    text.replace("300.00", "NaN", 1), text.replace("direct", "unknown", 1),
                    text.splitlines()[0] + "\n"]
        with tempfile.TemporaryDirectory(prefix="kb-finops-") as directory:
            root = Path(directory).resolve()
            self.assertTrue(root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
            for value in variants:
                path = root / "invalid.csv"
                path.write_text(value, encoding="utf-8")
                with self.subTest(value=value[-60:]), self.assertRaises(ValueError):
                    cost.load_ledger(path)

    def test_cli_has_no_input_side_effects(self):
        fixture = HERE / "synthetic-ledger.csv"
        before = fixture.read_bytes()
        result = subprocess.run([sys.executable, str(HERE / "cost-analysis.py")], capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        self.assertEqual(report["source_total"], "675.01")
        self.assertTrue(report["synthetic_only"])
        self.assertEqual(fixture.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
