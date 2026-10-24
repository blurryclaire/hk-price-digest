"""CLI: CSV in → digest JSON + markdown out."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hk_price_digest.digest import build_digest
from hk_price_digest.parse import load_prices
from hk_price_digest.render import render_markdown


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Build an HK supermarket price digest from local CSV.")
    p.add_argument("csv", type=Path, help="Input prices CSV")
    p.add_argument("--week", default=None, help="Filter ISO week, e.g. 2026-W43")
    p.add_argument("--json-out", type=Path, default=None, help="Write digest JSON")
    p.add_argument("--md-out", type=Path, default=None, help="Write markdown digest")
    args = p.parse_args(argv)

    rows = load_prices(args.csv)
    digest = build_digest(rows, week=args.week)
    md = render_markdown(digest)

    if args.json_out:
        args.json_out.write_text(json.dumps(digest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.md_out:
        args.md_out.write_text(md, encoding="utf-8")

    if not args.json_out and not args.md_out:
        print(md)


if __name__ == "__main__":
    main()
