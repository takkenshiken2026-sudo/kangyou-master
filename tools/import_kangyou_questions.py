#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管理業務主任者 — デスクトップ CSV → data/past_questions.csv / practice / ichimon

  python3 tools/import_kangyou_questions.py
  python3 tools/import_kangyou_questions.py --dry-run
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ARCHIVE = DATA / "imported"

_KANRI_DIR = Path.home() / "Desktop" / "管理業務主任者"
DEFAULT_PAST = _KANRI_DIR / "管理業務主任者過去問.csv"
DEFAULT_PRACTICE = _KANRI_DIR / "管理業務主任者実践演習.csv"
DEFAULT_ICHIMON = _KANRI_DIR / "管理業務主任者一問一答.csv"

DEFAULT_CATEGORY = "判例・横断総合"
KANA_BRANCH = {"ア": 1, "イ": 2, "ウ": 3, "エ": 4, "オ": 5, "カ": 6}

PAST_HEADER = [
    "exam_year",
    "exam_wareki",
    "question_no",
    "type",
    "category",
    "tags",
    "stem",
    "preamble",
    "statement_a",
    "statement_b",
    "statement_c",
    "statement_d",
    "choice_1",
    "choice_2",
    "choice_3",
    "choice_4",
    "correct",
    "is_exempt",
    "is_invalidated",
    "note",
    "explanation",
    "explanation_summary",
    "explanation_correct",
    "explanation_choices",
    "explanation_point",
    "related_links",
]

PRACTICE_HEADER = [
    "question_no",
    "type",
    "category",
    "tags",
    "stem",
    "preamble",
    "statement_a",
    "statement_b",
    "statement_c",
    "statement_d",
    "choice_1",
    "choice_2",
    "choice_3",
    "choice_4",
    "correct",
    "explanation",
]

ICHIMON_HEADER = [
    "id",
    "question",
    "answer",
    "explanation",
    "category",
    "tags",
    "source",
    "note",
]

FORMAT_TO_TYPE = {
    "single_choice": "single",
    "combination": "combination",
    "count": "count",
    "item_set": "single",
    "case_based": "single",
    "comparison_table": "single",
    "precedent_fill": "single",
    "accounting_table": "count",
}


def norm(s: str | None) -> str:
    return (s or "").strip()


def exam_code_to_year(code: str) -> int:
    code = norm(code).lower()
    base = code.split("_")[0]
    if base.startswith("h"):
        return 1988 + int(base[1:])
    if base.startswith("r"):
        return 2018 + int(base[1:])
    raise ValueError(f"未対応の exam_code: {code!r}")


def resolve_correct(raw: str, qfmt: str) -> str:
    raw = norm(raw)
    if raw.isdigit() and 1 <= int(raw) <= 4:
        return raw
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    nums = [int(p) for p in parts if p.isdigit()]
    if not nums or any(n < 1 or n > 4 for n in nums):
        raise ValueError(f"正答を解釈できません: {raw!r}")
    if qfmt == "count":
        return str(len(nums))
    return str(nums[-1])


def branch_label(raw: str) -> int:
    label = norm(raw)
    if label.isdigit():
        return int(label)
    if label in KANA_BRANCH:
        return KANA_BRANCH[label]
    return 1


def parse_numbered_choices(text: str, *, max_n: int = 4) -> list[str]:
    text = norm(text).replace(" / ", "\n")
    if not text:
        raise ValueError("選択肢が空です")
    positions = list(re.finditer(r"(?:^|\n)\s*(\d+)[:：]\s*", text))
    if not positions:
        raise ValueError(f"選択肢を解析できません: {text[:80]!r}…")
    out: dict[int, str] = {}
    for i, m in enumerate(positions):
        num = int(m.group(1))
        if num > max_n:
            continue
        start = m.end()
        end = positions[i + 1].start() if i + 1 < len(positions) else len(text)
        body = text[start:end].strip().replace("\n", " ")
        out[num] = body
    if not all(k in out for k in range(1, max_n + 1)):
        raise ValueError(f"選択肢1〜{max_n}が揃いません")
    return [out[k] for k in range(1, max_n + 1)]


def build_past_category_map(ichimon_path: Path) -> dict[tuple[str, str], str]:
    mapping: dict[tuple[str, str], str] = {}
    with ichimon_path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            code = norm(row.get("source_exam_code"))
            qno = norm(row.get("source_question_no"))
            subj = norm(row.get("subject"))
            if not code or not qno or not subj:
                continue
            key = (code, qno)
            if key not in mapping:
                mapping[key] = subj
    return mapping


def ichimon_id(row: dict[str, str], line_no: int) -> str:
    code = norm(row.get("source_exam_code"))
    qno_s = norm(row.get("source_question_no"))
    branch = branch_label(row.get("source_choice_label") or "1")
    if code and qno_s.isdigit():
        year = exam_code_to_year(code)
        return f"{year}-{int(qno_s):02d}-{branch}"
    if qno_s.isdigit():
        return f"2026-{int(qno_s):03d}-{branch}"
    return f"2026-{line_no:04d}-1"


def ichimon_answer(row: dict[str, str]) -> str:
    label = norm(row.get("answer_label"))
    if label in ("○", "〇"):
        return "○"
    if label in ("×", "✕", "╳"):
        return "×"
    raw = norm(row.get("answer_bool"))
    if raw in ("1", "true", "True"):
        return "○"
    if raw in ("0", "false", "False"):
        return "×"
    raise ValueError(f"answer を判定できません: record_id={row.get('record_id')!r}")


def import_past(src: Path, ichimon_src: Path) -> list[dict[str, str]]:
    cat_map = build_past_category_map(ichimon_src)
    rows_out: list[dict[str, str]] = []
    with src.open(encoding="utf-8-sig", newline="") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            code = norm(row.get("exam_code"))
            year = exam_code_to_year(code)
            qno = int(norm(row.get("question_no")))
            wareki = norm(row.get("exam_year"))
            qfmt = norm(row.get("question_format"))
            qtype = FORMAT_TO_TYPE.get(qfmt, "single")
            stem = norm(row.get("question_text"))
            if not stem:
                raise ValueError(f"past 行 {line_no}: question_text が空")
            choices = parse_numbered_choices(row.get("choices") or "")
            correct_raw = resolve_correct(row.get("correct_answer_text") or "", qfmt)
            category = cat_map.get((code, str(qno)), DEFAULT_CATEGORY)
            exp_col = norm(row.get("解説")) or norm(row.get("explanation"))
            tags = ";".join(
                p
                for p in (code, qfmt, norm(row.get("prompt_type")), norm(row.get("review_status")))
                if p
            )
            rows_out.append(
                {
                    "exam_year": str(year),
                    "exam_wareki": wareki,
                    "question_no": str(qno),
                    "type": qtype,
                    "category": category,
                    "tags": tags,
                    "stem": stem,
                    "preamble": "",
                    "statement_a": "",
                    "statement_b": "",
                    "statement_c": "",
                    "statement_d": "",
                    "choice_1": choices[0],
                    "choice_2": choices[1],
                    "choice_3": choices[2],
                    "choice_4": choices[3],
                    "correct": correct_raw,
                    "is_exempt": "FALSE",
                    "is_invalidated": "FALSE",
                    "note": norm(row.get("notes")),
                    "explanation": exp_col or "（解説は未入力です。）",
                    "explanation_summary": "",
                    "explanation_correct": "",
                    "explanation_choices": "",
                    "explanation_point": "",
                    "related_links": "",
                }
            )
    return rows_out


def import_practice(src: Path) -> list[dict[str, str]]:
    rows_out: list[dict[str, str]] = []
    with src.open(encoding="utf-8-sig", newline="") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            gno = int(norm(row.get("global_no") or row.get("question_no")))
            qfmt = norm(row.get("question_format"))
            qtype = FORMAT_TO_TYPE.get(qfmt, "single")
            stem = norm(row.get("question_text_draft"))
            if not stem:
                raise ValueError(f"practice 行 {line_no}: question_text_draft が空")
            choices = parse_numbered_choices(row.get("choices_summary") or "")
            correct_raw = norm(row.get("correct_answer_text_draft"))
            if not correct_raw.isdigit() or not (1 <= int(correct_raw) <= 4):
                raise ValueError(f"practice 行 {line_no}: correct={correct_raw!r}")
            category = norm(row.get("subject"))
            if not category:
                raise ValueError(f"practice 行 {line_no}: subject が空")
            tags = ";".join(
                p
                for p in (
                    norm(row.get("set_code")),
                    norm(row.get("topic")),
                    norm(row.get("difficulty")),
                    norm(row.get("question_format")),
                )
                if p
            )
            exp = norm(row.get("explanation_draft")) or "（解説は未入力です。）"
            rows_out.append(
                {
                    "question_no": str(gno),
                    "type": qtype,
                    "category": category,
                    "tags": tags or "実践演習",
                    "stem": stem,
                    "preamble": "",
                    "statement_a": "",
                    "statement_b": "",
                    "statement_c": "",
                    "statement_d": "",
                    "choice_1": choices[0],
                    "choice_2": choices[1],
                    "choice_3": choices[2],
                    "choice_4": choices[3],
                    "correct": correct_raw,
                    "explanation": exp,
                }
            )
    rows_out.sort(key=lambda r: int(r["question_no"]))
    return rows_out


def import_ichimon(src: Path) -> list[dict[str, str]]:
    rows_out: list[dict[str, str]] = []
    seen: set[str] = set()
    with src.open(encoding="utf-8-sig", newline="") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            rid = ichimon_id(row, line_no)
            if rid in seen:
                rid = f"2026-{line_no:04d}-1"
            seen.add(rid)
            category = norm(row.get("subject"))
            if not category:
                raise ValueError(f"ichimon 行 {line_no}: subject が空")
            question = norm(row.get("statement_text"))
            if not question:
                raise ValueError(f"ichimon 行 {line_no}: statement_text が空")
            exp = norm(row.get("explanation_text")) or "（解説は未入力です。）"
            tags = ";".join(
                p
                for p in (
                    norm(row.get("record_id")),
                    norm(row.get("topic")),
                    norm(row.get("source_kind")),
                )
                if p
            )
            rows_out.append(
                {
                    "id": rid,
                    "question": question,
                    "answer": ichimon_answer(row),
                    "explanation": exp,
                    "category": category,
                    "tags": tags or "一問一答",
                    "source": norm(row.get("source_file")) or norm(row.get("source_kind")),
                    "note": norm(row.get("rewrite_note")),
                }
            )
    return rows_out


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def archive_source(src: Path, name: str) -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = ARCHIVE / f"{name}_{stamp}.csv"
    shutil.copy2(src, dest)
    print(f"archived: {dest.relative_to(ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--past", type=Path, default=DEFAULT_PAST)
    ap.add_argument("--practice", type=Path, default=DEFAULT_PRACTICE)
    ap.add_argument("--ichimon", type=Path, default=DEFAULT_ICHIMON)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for p in (args.past, args.practice, args.ichimon):
        if not p.is_file():
            print(f"ファイルがありません: {p}", file=sys.stderr)
            return 1

    past_rows = import_past(args.past, args.ichimon)
    practice_rows = import_practice(args.practice)
    ichimon_rows = import_ichimon(args.ichimon)

    past_cats = Counter(r["category"] for r in past_rows)
    print(f"past: {len(past_rows)} 問（分野: {len(past_cats)}、既定分野 {past_cats.get(DEFAULT_CATEGORY, 0)} 問）")
    print(f"practice: {len(practice_rows)} 問")
    print(f"ichimon: {len(ichimon_rows)} 問")

    if args.dry_run:
        return 0

    for src, label in (
        (args.past, "kangyou_past"),
        (args.practice, "kangyou_practice"),
        (args.ichimon, "kangyou_ichimon"),
    ):
        archive_source(src, label)

    write_csv(DATA / "past_questions.csv", PAST_HEADER, past_rows)
    write_csv(DATA / "practice_questions.csv", PRACTICE_HEADER, practice_rows)
    write_csv(DATA / "ichimon_questions.csv", ICHIMON_HEADER, ichimon_rows)
    print("wrote data/past_questions.csv, practice_questions.csv, ichimon_questions.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
