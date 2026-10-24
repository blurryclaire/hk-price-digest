# hk-price-digest

[![tests](https://github.com/deedade/hk-price-digest/actions/workflows/ci.yml/badge.svg)](https://github.com/deedade/hk-price-digest/actions/workflows/ci.yml)

**Compare HK supermarket prices from your CSV** — local digests, no scrapers.

## Why

Hong Kong supermarket prices for the same item often differ by store, and the gap is real. Comparing those prices by hand, or in a spreadsheet, is error-prone: one wrong row or a mixed-up week changes the result. This tool is for people who bring their own price CSV, from a store export or from their own notes. They do not want scrapers, store logins, or to hand a store account to a cloud service. It is not a live Hong Kong price tracker.

## Purpose

On your machine, it works out which store is cheaper, how large the gaps are, and which store wins a small basket. The output is markdown and/or JSON for you to read, or for **any agent that can run a shell command and read files** (Grok Bot, Hermes, OpenClaw, Cursor agents, Claude Code, and others). This repository is a small local CLI under deedade. Grok Bot is one intended consumer, not a hard dependency. It is not an xAI API client.

## Workflow

1. Prepare or export a price CSV. Bring your own; the sample in this repo is synthetic.
2. Run `hk-price-digest` locally.
3. Read the markdown and/or JSON. Optionally hand the digest to an agent (Grok Bot, Hermes, OpenClaw, …) or keep reading it yourself.

### Agents

Install and run the CLI locally. The agent invokes `hk-price-digest`, then reads `--json-out` and `--md-out`. There is no Grok- or Hermes-specific protocol, and this is not the grok-hermes-webhook contract. Once installed, it works offline. Any agent runtime with a local shell can use it.

v0.1 stops at the local digest: no push notifications, no database, no scrapers, and no Hermes-style four-part async report.

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
