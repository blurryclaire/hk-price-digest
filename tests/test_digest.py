from pathlib import Path

from hk_price_digest.digest import build_digest
from hk_price_digest.parse import load_prices
from hk_price_digest.render import render_markdown

SAMPLE = Path(__file__).resolve().parents[1] / "examples" / "sample_prices.csv"


def test_sample_gap_and_basket():
    rows = load_prices(SAMPLE)
    digest = build_digest(rows, week="2026-W43")
    assert digest["counts"]["rows"] == 12
    assert digest["counts"]["products"] == 4
    assert digest["counts"]["stores"] == 3

    p003 = next(g for g in digest["top_gaps"] if g["product_id"] == "P003")
    assert p003["gap_pct"] == 31.0
    assert p003["low_store"] == "StoreA"
    assert p003["high_store"] == "StoreB"

    basket = digest["basket"]
    assert basket["cheapest_store"] == "StoreC"
    assert basket["cheapest_total"] == 143.30
    assert basket["by_store"]["StoreC"] == 143.30


def test_render_contains_week():
    rows = load_prices(SAMPLE)
    md = render_markdown(build_digest(rows))
    assert "2026-W43" in md
    assert "StoreC" in md
