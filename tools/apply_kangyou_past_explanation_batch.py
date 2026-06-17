#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
レビュー済みバッチ CSV から past_questions.csv の explanation を安全に反映する。

  python3 tools/apply_kangyou_past_explanation_batch.py \\
    ~/Projects/scripts/_question_review_kangyou_2008_batch.csv

  python3 tools/apply_kangyou_past_explanation_batch.py batch.csv --dry-run

バッチ CSV 列: id (2008-1 形式), explanation, status (approved のみ反映)
反映後: enrich (--only-empty) → validate_question_explanations
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAST_CSV = ROOT / "data" / "past_questions.csv"
_ID_RE = re.compile(r"^(\d{4})-(\d+)$")


def parse_id(raw: str) -> tuple[str, str] | None:
    m = _ID_RE.match((raw or "").strip())
    if not m:
        return None
    return m.group(1), str(int(m.group(2)))


def load_batch(path: Path, *, require_approved: bool) -> dict[tuple[str, str], str]:
    out: dict[tuple[str, str], str] = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            qid = (row.get("id") or "").strip()
            exp = (row.get("explanation") or "").strip()
            status = (row.get("status") or "").strip().lower()
            if not qid or not exp:
                continue
            if require_approved and status not in ("approved", "done", "ok"):
                continue
            key = parse_id(qid)
            if not key:
                raise ValueError(f"行 {line_no}: id 形式が不正です: {qid!r}")
            if key in out:
                raise ValueError(f"行 {line_no}: 重複 id {qid}")
            out[key] = exp
    return out


def apply(batch: dict[tuple[str, str], str], *, dry_run: bool) -> tuple[int, int]:
    with PAST_CSV.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if not rows:
        raise SystemExit("past_questions.csv が空です")
    updated = 0
    missing: list[str] = []
    for key, exp in sorted(batch.items()):
        year, qno = key
        match = None
        for row in rows:
            if row.get("exam_year") == year and row.get("question_no") == qno:
                match = row
                break
        if not match:
            missing.append(f"{year}-{qno}")
            continue
        if match.get("explanation") == exp:
            continue
        match["explanation"] = exp
        for col in (
            "explanation_summary",
            "explanation_correct",
            "explanation_choices",
            "explanation_point",
        ):
            match[col] = ""
        updated += 1

    if missing:
        print(f"WARN: CSV に存在しない id {len(missing)} 件: {', '.join(missing[:5])}", file=sys.stderr)

    if dry_run:
        print(f"dry-run: {updated} 問を更新予定（バッチ {len(batch)} 件）")
        return updated, len(missing)

    if updated:
        with PAST_CSV.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        print(f"updated: {updated} 問 → {PAST_CSV.relative_to(ROOT)}")

    return updated, len(missing)


def run_post_pipeline() -> None:
    py = sys.executable
    steps = [
        [py, "tools/enrich_past_explanation_choices.py", "--only-empty", "--refresh-boilerplate"],
        [py, "tools/validate_question_explanations.py"],
    ]
    for cmd in steps:
        print("+", " ".join(cmd))
        subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("batch_csv", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--any-status",
        action="store_true",
        help="status 列を無視（執筆中ドラフトのローカル確認用）",
    )
    ap.add_argument("--skip-enrich", action="store_true")
    args = ap.parse_args()

    if not args.batch_csv.is_file():
        print(f"ファイルがありません: {args.batch_csv}", file=sys.stderr)
        return 1
    if not PAST_CSV.is_file():
        print(f"past_questions.csv がありません: {PAST_CSV}", file=sys.stderr)
        return 1

    batch = load_batch(args.batch_csv, require_approved=not args.any_status)
    if not batch:
        print("反映対象行がありません（explanation 空、または status≠approved）", file=sys.stderr)
        return 1

    updated, _ = apply(batch, dry_run=args.dry_run)
    if args.dry_run or updated == 0:
        return 0

    if not args.skip_enrich:
        run_post_pipeline()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
