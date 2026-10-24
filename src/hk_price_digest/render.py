"""Render digest dict to markdown."""

from __future__ import annotations

from typing import Any


def render_markdown(digest: dict[str, Any]) -> str:
    week = digest.get("week") or "?"
    counts = digest.get("counts") or {}
    lines = [
        f"# HK price digest — {week}",
        "",
        f"Rows: **{counts.get('rows', 0)}** · Products: **{counts.get('products', 0)}** · Stores: **{counts.get('stores', 0)}**",
        "",
        "## Basket (products available at every store)",
    ]
    basket = digest.get("basket") or {}
    by_store = basket.get("by_store") or {}
    if by_store:
        for store, total in sorted(by_store.items(), key=lambda x: x[1]):
            mark = " ← cheapest" if store == basket.get("cheapest_store") else ""
            lines.append(f"- **{store}**: HKD {total:.2f}{mark}")
    else:
        lines.append("_No complete basket._")

    lines += ["", "## Top price gaps"]
    gaps = digest.get("top_gaps") or []
    if not gaps:
        lines.append("_No multi-store gaps._")
    else:
        for g in gaps:
            lines.append(
                f"- **{g['name']}** (`{g['product_id']}`): "
                f"{g['low_store']} HKD {g['low_price']:.2f} → "
                f"{g['high_store']} HKD {g['high_price']:.2f} "
                f"(**{g['gap_pct']}%**)"
            )

    wins = digest.get("store_win_counts") or {}
    lines += ["", "## Cheapest-store wins (by product)"]
    if wins:
        for store, n in wins.items():
            lines.append(f"- **{store}**: {n}")
    else:
        lines.append("_n/a_")

    caveats = digest.get("caveats") or []
    lines += ["", "## Caveats"]
    for c in caveats:
        lines.append(f"- {c}")
    lines.append("")
    return "\n".join(lines)
