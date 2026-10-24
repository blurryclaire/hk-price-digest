# hk-price-digest

[![tests](https://github.com/deedade/hk-price-digest/actions/workflows/ci.yml/badge.svg)](https://github.com/deedade/hk-price-digest/actions/workflows/ci.yml)

Hong Kong supermarket **price digests you can run locally** — CSV in, markdown / JSON out. **No scrapers**, no accounts, no live network.

This repository is a **Grok Bot** local tool (deedade). It reads a price CSV on your machine and writes a digest. It is not an xAI API client.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
hk-price-digest examples/sample_prices.csv --week 2026-W43
```

Write files:

```bash
hk-price-digest examples/sample_prices.csv \
  --json-out examples/digest-2026-W43.json \
  --md-out examples/sample_digest.md
```

## Input CSV

| Column | Notes |
|--------|--------|
| `week` | ISO week `YYYY-Www` |
| `observed_on` | `YYYY-MM-DD` |
| `product_id` | Stable id |
| `store` | Store label (sample uses `StoreA` / `StoreB` / `StoreC`) |
| `price` | HKD; `≤ 0` rows dropped |
| optional | `barcode`, `name`, `brand`, `category`, `pack_qty`, `pack_unit`, `currency`, `source` |

Deduping: same `(week, product_id, store)` keeps the **minimum** price.

## Output

JSON fields: `counts`, `store_win_counts`, `top_gaps`, `basket`, `week_over_week` (null until you add a prior week), `caveats`.

On the bundled synthetic sample (`2026-W43`): toilet paper **P003** shows a **~31%** gap; the four-item basket is cheapest at **StoreC (HKD 143.30)**.

## Privacy

Sample rows are **synthetic** (`source=synthetic-sample`). Do not commit real loyalty, bank, or store-account credentials. Bring your own exports.

## Layout

```
src/hk_price_digest/      # parse, digest, markdown/JSON render, CLI
examples/                 # synthetic sample CSV, markdown, JSON
tests/
.github/workflows/ci.yml  # pytest on push and pull_request
```

## What v0.1 does **not** include

- Supermarket scrapers / logins
- Push notifications
- Historical database or hosting
- Live network fetches or xAI API calls

## License

MIT
