#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""学習系ガイドへ公開済み affiliate 比較記事の導線を追加する（管理業務主任者）。"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "guide_articles.csv"

AFFILIATE_TITLES = {
    "affiliate-textbooks-recommend": (
        "管理業務主任者のおすすめ参考書・テキスト3選【2026年度版・独学】"
    ),
    "affiliate-problem-books": (
        "管理業務主任者のおすすめ問題集3選【過去問·分野別2026】"
    ),
}

BODY = {
    "affiliate-textbooks-recommend": (
        "テキスト1冊は、affiliate-textbooks-recommend でTAC基本テキスト·LEC出る順速習·"
        "Wマスターテキストの3冊を比較してから固定すると、"
        "50問·5出題分野の演習計画に組み込みやすくなります。"
    ),
    "affiliate-problem-books": (
        "テキスト第1周後の演習1冊は、affiliate-problem-books でTAC項目別過去8年·"
        "LEC分野別過去問·Wマスター過去問集の3冊から選ぶと、"
        "50問120分通しの演習量を確保しやすくなります。"
    ),
}

GUIDE_AFFILIATE: dict[str, tuple[str, int]] = {
    "textbook-selection": ("affiliate-textbooks-recommend", 2),
    "study-plan": ("affiliate-textbooks-recommend", 3),
    "study-plan-beginner": ("affiliate-textbooks-recommend", 2),
    "study-plan-3months": ("affiliate-textbooks-recommend", 3),
    "study-plan-6months": ("affiliate-textbooks-recommend", 3),
    "study-plan-working": ("affiliate-textbooks-recommend", 3),
    "past-question-strategy": ("affiliate-problem-books", 2),
    "past-questions-by-field": ("affiliate-problem-books", 2),
    "mock-exam-how-to": ("affiliate-problem-books", 3),
}


def _split_related(value: str) -> list[str]:
    return [x.strip() for x in (value or "").split(";") if x.strip()]


def _append_related(value: str, token: str) -> str:
    parts = _split_related(value)
    slug = token.split(":", 1)[0]
    if any(p.split(":", 1)[0] == slug for p in parts):
        return ";".join(parts)
    parts.append(token)
    return ";".join(parts)


def _append_body(body: str, aff_slug: str) -> str:
    sentence = BODY[aff_slug]
    if aff_slug in (body or ""):
        return body
    text = (body or "").rstrip()
    if not text:
        return sentence
    if not text.endswith("。"):
        text += "。"
    return text + sentence


def apply_guide_updates(rows: list[dict[str, str]]) -> int:
    by_slug = {r["slug"]: r for r in rows}
    changed = 0
    for slug, (aff_slug, sec_n) in GUIDE_AFFILIATE.items():
        row = by_slug.get(slug)
        if not row or (row.get("content_status") or "").strip() != "published":
            continue
        body_key = f"section_{sec_n}_body"
        old_body = row.get(body_key, "")
        new_body = _append_body(old_body, aff_slug)
        if new_body != old_body:
            row[body_key] = new_body

        token = f"{aff_slug}:{AFFILIATE_TITLES[aff_slug]}"
        new_rl = _append_related(row.get("related_links", ""), token)
        if new_rl != row.get("related_links", "") or new_body != old_body:
            row["related_links"] = new_rl
            changed += 1
    return changed


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames:
        raise SystemExit("guide_articles.csv: no header")

    changed = apply_guide_updates(rows)

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Guide funnel: {len(GUIDE_AFFILIATE)} targets, {changed} row(s) updated")


if __name__ == "__main__":
    main()
