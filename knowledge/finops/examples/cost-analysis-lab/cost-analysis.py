"""Calculate synthetic FinOps examples; never reads credentials or calls a provider."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_FLOOR
from pathlib import Path

CENT = Decimal("0.01")
ZERO = Decimal("0")
UNALLOCATED = "__unallocated__"


def decimal(value: str | int | Decimal) -> Decimal:
    if isinstance(value, (float, bool)):
        raise ValueError("Use decimal strings or integers, not floats or booleans")
    try:
        result = Decimal(value)
    except (InvalidOperation, TypeError, ValueError) as error:
        raise ValueError("Invalid decimal value") from error
    if not result.is_finite():
        raise ValueError("Non-finite values are not supported")
    return result


@dataclass(frozen=True)
class Line:
    line_id: str
    period: str
    currency: str
    cost_basis: str
    owner: str
    scope: str
    amount: Decimal


def load_ledger(path: Path) -> list[Line]:
    required = {"line_id", "period", "currency", "cost_basis", "owner", "scope", "amount"}
    rows: list[Line] = []
    seen: set[str] = set()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or []) != required or len(reader.fieldnames or []) != len(required):
            raise ValueError("Unexpected ledger columns")
        for raw in reader:
            if None in raw or any(value is None for value in raw.values()):
                raise ValueError("Incomplete or extra CSV fields")
            item = {key: value.strip() for key, value in raw.items()}
            if not item["line_id"] or item["line_id"] in seen:
                raise ValueError("Missing or duplicate line_id")
            seen.add(item["line_id"])
            try:
                datetime.strptime(item["period"], "%Y-%m")
            except ValueError as error:
                raise ValueError("Invalid monthly period") from error
            if len(item["period"]) != 7:
                raise ValueError("Monthly period must be YYYY-MM")
            if item["currency"] != "USD" or item["cost_basis"] != "synthetic-amortized":
                raise ValueError("This teaching ledger requires USD and one synthetic-amortized basis")
            if item["scope"] not in {"direct", "shared"} or item["owner"] == UNALLOCATED:
                raise ValueError("Invalid scope or reserved owner")
            amount = decimal(item["amount"])
            if amount != amount.quantize(CENT):
                raise ValueError("Teaching ledger amounts must already be normalized to cents")
            rows.append(Line(**{**item, "amount": amount}))
    if not rows or len({line.period for line in rows}) != 1:
        raise ValueError("Provide exactly one non-empty monthly ledger")
    return rows


def allocate_shared(amount: Decimal, weights: dict[str, Decimal]) -> dict[str, Decimal]:
    """Distribute integer cents by largest remainder; alphabetical tie-break."""
    amount = decimal(amount)
    if amount != amount.quantize(CENT) or not weights:
        raise ValueError("A cent-normalized amount and non-empty weights are required")
    values = {name: decimal(weight) for name, weight in weights.items()}
    if any(not name or name == UNALLOCATED or weight < ZERO for name, weight in values.items()):
        raise ValueError("Weights require valid owners and non-negative values")
    total = sum(values.values(), ZERO)
    if total <= ZERO:
        raise ValueError("At least one allocation weight must be positive")
    cents = int(abs(amount) / CENT)
    exact = {name: Decimal(cents) * weight / total for name, weight in values.items()}
    whole = {name: int(value.to_integral_value(rounding=ROUND_FLOOR)) for name, value in exact.items()}
    remaining = cents - sum(whole.values())
    order = sorted(values, key=lambda name: (-(exact[name] - whole[name]), name))
    for name in order[:remaining]:
        whole[name] += 1
    sign = Decimal("-1") if amount < ZERO else Decimal("1")
    result = {name: sign * Decimal(value) * CENT for name, value in whole.items()}
    if sum(result.values(), ZERO) != amount:
        raise ValueError("Allocation failed to reconcile")
    return result


def allocation_report(rows: list[Line], weights: dict[str, Decimal]) -> dict:
    direct: dict[str, Decimal] = {}
    shared = ZERO
    for line in rows:
        if line.scope == "shared":
            shared += line.amount
        else:
            owner = line.owner or UNALLOCATED
            direct[owner] = direct.get(owner, ZERO) + line.amount
    allocations = allocate_shared(shared, weights)
    final = dict(direct)
    for owner, value in allocations.items():
        final[owner] = final.get(owner, ZERO) + value
    source = sum((line.amount for line in rows), ZERO)
    if sum(final.values(), ZERO) != source:
        raise ValueError("Source and allocated totals differ")
    return {"period": rows[0].period, "currency": "USD", "cost_basis": "synthetic-amortized",
            "source_total": source, "direct_net": direct, "shared_pool_net": shared,
            "shared_allocations": allocations, "final_net": final, "reconciled": True}


def unit_cost(cost: Decimal, units: Decimal) -> Decimal | None:
    cost, units = decimal(cost), decimal(units)
    if units < ZERO:
        raise ValueError("Business units cannot be negative")
    return None if units == ZERO else cost / units


def normalized_comparison(before_cost: Decimal, before_units: Decimal,
                          after_cost: Decimal, after_units: Decimal) -> dict:
    before_cost, before_units, after_cost, after_units = map(decimal, (before_cost, before_units, after_cost, after_units))
    if before_cost < ZERO or after_cost < ZERO or before_units <= ZERO or after_units <= ZERO:
        raise ValueError("Comparison needs non-negative costs and positive comparable units")
    baseline_unit = before_cost / before_units
    normalized = baseline_unit * after_units
    return {"before_unit_cost": baseline_unit, "after_unit_cost": after_cost / after_units,
            "raw_cost_change": after_cost - before_cost,
            "baseline_at_after_demand": normalized,
            "modeled_cost_avoidance": normalized - after_cost}


def decompose_quantity_and_rate(before_quantity: Decimal, after_quantity: Decimal,
                                before_rate: Decimal, after_rate: Decimal) -> dict:
    q0, q1, r0, r1 = map(decimal, (before_quantity, after_quantity, before_rate, after_rate))
    if min(q0, q1, r0, r1) < ZERO:
        raise ValueError("Quantities and rates must be non-negative")
    quantity_effect = (q0 - q1) * r0
    rate_effect = q1 * (r0 - r1)
    return {"before_cost": q0 * r0, "after_cost": q1 * r1,
            "quantity_effect": quantity_effect, "rate_effect_after_quantity_change": rate_effect,
            "combined_difference": quantity_effect + rate_effect}


def linear_run_rate(accrued: Decimal, elapsed_days: int, period_days: int) -> Decimal:
    accrued = decimal(accrued)
    if accrued < ZERO or not 0 < elapsed_days <= period_days:
        raise ValueError("Run-rate needs non-negative accrued cost and valid elapsed days")
    return accrued / Decimal(elapsed_days) * Decimal(period_days)


def anomaly_candidate(baseline: Decimal, observed: Decimal,
                      absolute_threshold: Decimal, relative_threshold: Decimal) -> dict:
    baseline, observed, absolute_threshold, relative_threshold = map(decimal, (baseline, observed, absolute_threshold, relative_threshold))
    if min(baseline, observed, absolute_threshold, relative_threshold) < ZERO:
        raise ValueError("Toy anomaly inputs must be non-negative")
    delta = observed - baseline
    relative = None if baseline == ZERO else delta / baseline
    flagged = delta >= absolute_threshold and (relative is None or relative >= relative_threshold)
    return {"delta": delta, "relative_change": relative, "candidate": flagged,
            "cold_start": baseline == ZERO, "method": "illustrative fixed baseline; not statistical anomaly detection"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=Path(__file__).with_name("synthetic-ledger.csv"))
    args = parser.parse_args()
    report = allocation_report(load_ledger(args.ledger), {"payments": Decimal(3), "data": Decimal(1)})
    report["synthetic_only"] = True
    report["comparison"] = normalized_comparison(Decimal(600), Decimal(10000), Decimal(660), Decimal(15000))
    report["quantity_and_rate"] = decompose_quantity_and_rate(Decimal(100), Decimal(80), Decimal(1), Decimal("0.75"))
    report["illustrative_month_end_run_rate"] = linear_run_rate(Decimal(960), 12, 30)
    report["anomaly_example"] = anomaly_candidate(Decimal(100), Decimal(160), Decimal(50), Decimal("0.20"))
    print(json.dumps(report, default=str, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
