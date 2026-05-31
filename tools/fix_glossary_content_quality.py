#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用語 CSV の term_detail_body を定義中心の短文に整える。"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.knowledge_hub_seo import glossary_definition_body_text

CSV_PATH = ROOT / "data" / "glossary_terms.csv"

BLOATED_MARKERS = (
    "失点差がつきやすい",
    "試験対策では",
    "過去問演習では",
    "実務目線では",
    "条文根拠と実務場面を往復",
    "【専門家の視点】",
)


def needs_fix(row: dict[str, str]) -> bool:
    body = row.get("term_detail_body") or ""
    if any(m in body for m in BLOATED_MARKERS):
        return True
    if "<table" in body.lower():
        return True
    return len(body.replace("\n", "")) >= 600


def fix_row(row: dict[str, str]) -> tuple[dict[str, str], bool]:
    term = (row.get("term") or "").strip()
    if not term:
        return row, False
    if not needs_fix(row):
        return row, False
    cleaned = glossary_definition_body_text(row)
    if not cleaned or cleaned == (row.get("term_detail_body") or "").strip():
        return row, False
    new_row = dict(row)
    new_row["term_detail_body"] = cleaned
    return new_row, True


def main() -> None:
    if not CSV_PATH.is_file():
        raise SystemExit(f"missing: {CSV_PATH}")

    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        header = list(reader.fieldnames or [])
        rows = list(reader)

    changed = 0
    new_rows: list[dict[str, str]] = []
    for row in rows:
        fixed, did = fix_row(row)
        if did:
            changed += 1
        new_rows.append(fixed)

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        writer.writeheader()
        writer.writerows(new_rows)

    print(f"updated {changed}/{len(new_rows)} rows in {CSV_PATH.name}")


if __name__ == "__main__":
    main()
