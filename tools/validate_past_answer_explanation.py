#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""過去問 CSV の正答列と解説本文の整合性を検証する。"""

from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.q_explanation import (
    build_choice_commentary,
    is_inverted_polarity,
    norm,
    question_polarity,
    split_legacy_explanation,
)

CSV_PATH = ROOT / "data" / "past_questions.csv"
PLACEHOLDER = "（解説は未入力です。）"


@dataclass
class Mismatch:
    year: int
    qno: int
    correct: int
    kind: str
    detail: str

    def key(self) -> str:
        return f"{self.year}-{self.qno:02d}"


def parse_correct(raw: str) -> int | None:
    raw = norm(raw)
    if not raw:
        return None
    m = re.match(r"^(\d+)", raw)
    return int(m.group(1)) if m else None


def extract_explicit_answer(text: str) -> int | None:
    m = re.search(r"^正解は\s*(\d+)\s*です", text)
    if m:
        return int(m.group(1))
    m = re.search(r"正答は\s*[（(]?(\d+)[）)]?", text)
    if m:
        return int(m.group(1))
    return None


def page_from_row(row: dict) -> dict:
    correct = parse_correct(row.get("correct", ""))
    opts = [norm(row.get(f"choice_{i}")) for i in range(1, 5)]
    return {
        "correct": correct,
        "opts": opts,
        "stem": norm(row.get("stem")),
        "stem_plain": norm(row.get("stem")),
        "category": norm(row.get("category")),
        "tags": [t.strip() for t in norm(row.get("tags")).split(";") if t.strip()],
        "is_invalidated": norm(row.get("is_invalidated")).upper() == "TRUE",
    }


def check_row(row: dict) -> list[Mismatch]:
    year = int(row["exam_year"])
    qno = int(row["question_no"])
    page = page_from_row(row)
    correct = page["correct"]
    stem = page["stem"]
    if page["is_invalidated"] or correct is None:
        return []

    exp = norm(row.get("explanation"))
    issues: list[Mismatch] = []

    if not exp or exp == PLACEHOLDER:
        return issues

    explicit = extract_explicit_answer(exp)
    if explicit is not None and explicit != correct:
        issues.append(
            Mismatch(
                year,
                qno,
                correct,
                "explicit_answer",
                f"解説の明示正答={explicit}、CSV correct={correct}",
            )
        )

    polarity = question_polarity(stem)

    # 「正しいもの」設問で正答肢を誤り扱い
    if polarity == "pick_correct":
        if re.search(rf"(?<![0-9]){correct}(?:は|が|も)(?:誤|不適切|正しくない)", exp):
            issues.append(
                Mismatch(
                    year,
                    qno,
                    correct,
                    "correct_marked_wrong",
                    "正しいものを選ぶ設問で正答肢を誤りと記述",
                )
            )
        for n in range(1, 5):
            if n == correct:
                continue
            if re.search(rf"(?<![0-9]){n}(?:は|が|も)正しい|{n}が正", exp):
                issues.append(
                    Mismatch(
                        year,
                        qno,
                        correct,
                        "wrong_marked_right",
                        f"正しいもの設問で誤答肢（{n}）を正しいと記述",
                    )
                )

    # 逆方向設問で「Nが誤り/不適切」と読める表現が残っている
    if is_inverted_polarity(stem):
        _, body = split_legacy_explanation(exp, stem=stem)
        if re.search(rf"(?<![0-9]){correct}(?:が|は|も)(?:誤り|不適切|正しくない)", body):
            issues.append(
                Mismatch(
                    year,
                    qno,
                    correct,
                    "inverted_phrasing",
                    "正答番号を『誤り/不適切』と短く表現（正答との辻褄が合わない）",
                )
            )

    wrong_items = build_choice_commentary(page, row)
    if correct in [n for n, _, _ in wrong_items]:
        issues.append(
            Mismatch(
                year,
                qno,
                correct,
                "commentary_includes_correct",
                "他の選択肢に正答肢が含まれている",
            )
        )

    return issues


def main() -> int:
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found", file=sys.stderr)
        return 2

    all_issues: list[Mismatch] = []
    total = 0
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            total += 1
            all_issues.extend(check_row(row))

    seen: set[tuple[str, str]] = set()
    unique: list[Mismatch] = []
    for m in all_issues:
        k = (m.key(), m.kind)
        if k in seen:
            continue
        seen.add(k)
        unique.append(m)

    unique.sort(key=lambda m: (m.year, m.qno, m.kind))

    print(f"Checked {total} past questions")
    print(f"Found {len(unique)} consistency issue(s)\n")

    for m in unique:
        print(f"[{m.kind}] {m.key()} correct={m.correct} — {m.detail}")

    return 1 if unique else 0


if __name__ == "__main__":
    raise SystemExit(main())
