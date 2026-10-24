"""Compute store gaps, basket totals, and digest JSON structure."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from hk_price_digest.parse import PriceRow


def build_digest(rows: list[PriceRow], *, week: str | None = None) -> dict[str, Any]:
    if week:
        rows = [r for r in rows if r.week == week]
    if not rows:
        return {
            "week": week,
            "counts": {"rows": 0, "products": 0, "stores": 0},
            "store_win_counts": {},
            "top_gaps": [],
            "basket": {"by_store": {}, "cheapest_store": None, "cheapest_total": None},
            "week_over_week": None,
            "caveats": ["no rows after filters"],
        }

    weeks = sorted({r.week for r in rows})
    active_week = week or weeks[-1]
    rows = [r for r in rows if r.week == active_week]

    by_product: dict[str, list[PriceRow]] = defaultdict(list)
    for r in rows:
        by_product[r.product_id].append(r)

    stores = sorted({r.store for r in rows})
    products = sorted(by_product.keys())

    # Basket: sum of each product's price at that store (only products present at store)
    # For fair basket across stores that carry all products:
    common = [
        pid
        for pid, plist in by_product.items()
        if set(stores).issubset({p.store for p in plist})
        or len({p.store for p in plist}) == len(stores)
    ]
    # Prefer products available at every store
    basket_pids = [
        pid for pid in products if {p.store for p in by_product[pid]} >= set(stores)
    ]
    if not basket_pids:
        basket_pids = products

    basket_by_store: dict[str, float] = {}
    for store in stores:
        total = 0.0
        ok = True
        for pid in basket_pids:
            hit = next((p for p in by_product[pid] if p.store == store), None)
            if hit is None:
                ok = False
                break
            total += hit.price
        if ok:
            basket_by_store[store] = round(total, 2)

    cheapest_store = None
    cheapest_total = None
    if basket_by_store:
        cheapest_store, cheapest_total = min(basket_by_store.items(), key=lambda x: x[1])

    store_wins: dict[str, int] = defaultdict(int)
    top_gaps: list[dict[str, Any]] = []
    for pid, plist in by_product.items():
        if len(plist) < 2:
            continue
        lo = min(plist, key=lambda p: p.price)
        hi = max(plist, key=lambda p: p.price)
        store_wins[lo.store] += 1
        if lo.price > 0:
            gap_pct = round((hi.price - lo.price) / lo.price * 100, 1)
        else:
            gap_pct = 0.0
        top_gaps.append(
            {
                "product_id": pid,
                "name": lo.name,
                "low_store": lo.store,
                "low_price": lo.price,
                "high_store": hi.store,
                "high_price": hi.price,
                "gap_pct": gap_pct,
            }
        )

    top_gaps.sort(key=lambda g: g["gap_pct"], reverse=True)

    return {
        "week": active_week,
        "counts": {
            "rows": len(rows),
            "products": len(products),
            "stores": len(stores),
        },
        "store_win_counts": dict(sorted(store_wins.items())),
        "top_gaps": top_gaps,
        "basket": {
            "product_ids": basket_pids,
            "by_store": basket_by_store,
            "cheapest_store": cheapest_store,
            "cheapest_total": cheapest_total,
        },
        "week_over_week": None,
        "caveats": [
            "Sample data is synthetic; not live supermarket prices.",
            "week_over_week requires a prior week in the same CSV (not in v0.1 sample).",
            "No scrapers or live network calls in v0.1.",
        ],
    }
