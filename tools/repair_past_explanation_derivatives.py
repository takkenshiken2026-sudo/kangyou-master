#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""未入力解説行から派生列（他肢・要約）を除去し、誤混入テンプレをクリアする。"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.q_content_quality import (  # noqa: E402
    KANGYOU_CROSS_EXAM_PHRASES,
    is_placeholder_explanation,
    norm,
)

DERIVED_COLS = (
    "explanation_summary",
    "explanation_correct",
    "explanation_choices",
    "explanation_point",
)

_CROSS_EXAM_RE = re.compile("|".join(map(re.escape, KANGYOU_CROSS_EXAM_PHRASES)))


def needs_clear(row: dict[str, str]) -> tuple[bool, str]:
    exp = norm(row.get("explanation"))
    if is_placeholder_explanation(exp):
        if any(norm(row.get(c)) for c in DERIVED_COLS):
            return True, "placeholder_with_derivatives"
        return False, ""
    combined = " ".join(norm(row.get(c)) for c in DERIVED_COLS)
    if combined and _CROSS_EXAM_RE.search(combined):
        return True, "cross_exam_phrase"
    return False, ""


def repair_csv(path: Path, *, dry_run: bool) -> tuple[int, int]:
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
    if not rows:
        return 0, 0
    fieldnames = list(rows[0].keys())
    cleared = 0
    for row in rows:
        do, reason = needs_clear(row)
        if not do:
            continue
        cleared += 1
        if dry_run:
            continue
        for col in DERIVED_COLS:
            row[col] = ""
    if not dry_run and cleared:
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
    return cleared, len(rows)


def main() -> int:
    ap = argparse.ArgumentParser(description="未入力解説の派生列を除去")
    ap.add_argument("--csv", type=Path, default=ROOT / "data" / "past_questions.csv")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cleared, total = repair_csv(args.csv.resolve(), dry_run=args.dry_run)
    mode = "would clear" if args.dry_run else "cleared"
    print(f"{mode} {cleared}/{total} rows in {args.csv.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
