"""Load price CSV and dedupe to min price per (week, product_id, store)."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class PriceRow:
    week: str
    observed_on: str
    product_id: str
    barcode: str
    name: str
    brand: str
    category: str
    pack_qty: str
    pack_unit: str
    store: str
    price: float
    currency: str
    source: str


def load_prices(path: str | Path) -> list[PriceRow]:
    rows: list[PriceRow] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            try:
                price = float(raw.get("price") or 0)
            except ValueError:
                continue
            if price <= 0:
                continue
            rows.append(
                PriceRow(
                    week=(raw.get("week") or "").strip(),
                    observed_on=(raw.get("observed_on") or "").strip(),
                    product_id=(raw.get("product_id") or "").strip(),
                    barcode=(raw.get("barcode") or "").strip(),
                    name=(raw.get("name") or "").strip(),
                    brand=(raw.get("brand") or "").strip(),
                    category=(raw.get("category") or "").strip(),
                    pack_qty=(raw.get("pack_qty") or "").strip(),
                    pack_unit=(raw.get("pack_unit") or "").strip(),
                    store=(raw.get("store") or "").strip(),
                    price=price,
                    currency=(raw.get("currency") or "HKD").strip() or "HKD",
                    source=(raw.get("source") or "").strip(),
                )
            )
    return dedupe_min(rows)


def dedupe_min(rows: Iterable[PriceRow]) -> list[PriceRow]:
    """For same (week, product_id, store), keep the row with minimum price."""
    best: dict[tuple[str, str, str], PriceRow] = {}
    for row in rows:
        key = (row.week, row.product_id, row.store)
        prev = best.get(key)
        if prev is None or row.price < prev.price:
            best[key] = row
    return sorted(best.values(), key=lambda r: (r.week, r.product_id, r.store))
