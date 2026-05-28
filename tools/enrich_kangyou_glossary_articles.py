#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
glossary_terms.csv の用語解説記事を試験向けの詳細本文に更新する。

  python3 tools/enrich_kangyou_glossary_articles.py
  python3 tools/enrich_kangyou_glossary_articles.py --dry-run
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.kangyou_glossary_content_helpers import is_weak_comparison  # noqa: E402
from tools.site_config import brand_name, exam_name  # noqa: E402

CSV_PATH = ROOT / "data" / "glossary_terms.csv"
HANDCRAFTED_DIR = ROOT / "data" / "kangyou_glossary_handcrafted"
HANDCRAFTED_FILES = [
    "civil.json",
    "condo.json",
    "ops.json",
    "misc.json",
]
KNOWLEDGE_MODULES = [
    "kangyou_glossary_knowledge_civil.py",
    "kangyou_glossary_knowledge_condo.py",
    "kangyou_glossary_knowledge_ops.py",
    "kangyou_glossary_knowledge_misc.py",
]

# 上記モジュールが無い場合は generate_kangyou_glossary_content.py を使う
GENERATE_SCRIPT = ROOT / "tools" / "generate_kangyou_glossary_content.py"

HEADER = [
    "term",
    "category",
    "tags",
    "short_def",
    "definition",
    "related_terms",
    "legal_basis",
    "importance",
    "explanation",
    "article_title",
    "article_lead",
    "term_detail_body",
    "comparison_table",
    "exam_points",
    "common_mistakes",
    "memory_tip",
    "example_question",
    "example_answer",
    "faq_1_question",
    "faq_1_answer",
    "faq_2_question",
    "faq_2_answer",
]

GENERIC_MARKERS = (
    "一次情報と照合しながら覚えてください",
    "意味と試験での使われ方を整理します",
    "定義を一文で説明できる;適用場面",
)


def load_handcrafted() -> dict[str, dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}
    for name in HANDCRAFTED_FILES:
        path = HANDCRAFTED_DIR / name
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for term, payload in data.items():
            if term in merged:
                raise SystemExit(f"duplicate handcrafted term: {term} in {name}")
            merged[term] = payload
    return merged


def load_knowledge() -> dict[str, dict[str, str]]:
    handcrafted = load_handcrafted()
    if handcrafted:
        return handcrafted
    merged: dict[str, dict[str, str]] = {}
    for name in KNOWLEDGE_MODULES:
        path = ROOT / "tools" / name
        if not path.is_file():
            continue
        spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
        if not spec or not spec.loader:
            continue
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        data = getattr(mod, "KNOWLEDGE", {})
        for term, payload in data.items():
            if term in merged:
                raise SystemExit(f"duplicate KNOWLEDGE term: {term} in {name}")
            merged[term] = payload
    return merged


def article_title(term: str) -> str:
    return f"{term}とは？{exam_name()}で押さえる意味と試験ポイント"


def apply_knowledge(row: dict[str, str], knowledge: dict[str, dict[str, str]]) -> bool:
    term = (row.get("term") or "").strip()
    payload = knowledge.get(term)
    if not payload:
        return False

    for key, value in payload.items():
        if key == "comparison_table":
            continue
        if value is None:
            continue
        text = str(value).strip()
        if not text:
            continue
        row[key] = text

    comp = str(payload.get("comparison_table") or "").strip()
    if comp:
        row["comparison_table"] = comp
    elif is_weak_comparison(row.get("comparison_table") or ""):
        row["comparison_table"] = ""

    if not (row.get("article_title") or "").strip():
        row["article_title"] = article_title(term)
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    knowledge = load_knowledge()
    if not knowledge and GENERATE_SCRIPT.is_file():
        import subprocess
        subprocess.run([sys.executable, str(GENERATE_SCRIPT)], check=True)
        rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
        print(f"generated via {GENERATE_SCRIPT.name}: {len(rows)} terms")
        return 0 if not args.dry_run else 0

    if not knowledge:
        print("error: no KNOWLEDGE modules loaded", file=sys.stderr)
        return 1

    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    updated = 0
    missing: list[str] = []
    for row in rows:
        term = (row.get("term") or "").strip()
        if apply_knowledge(row, knowledge):
            updated += 1
            body = row.get("term_detail_body") or ""
            if any(m in body for m in GENERIC_MARKERS):
                print(f"warn: {term} may still contain generic boilerplate")
        else:
            missing.append(term)

    print(f"knowledge entries: {len(knowledge)}")
    print(f"csv terms: {len(rows)}")
    print(f"updated: {updated}")
    if missing:
        print(f"missing ({len(missing)}): {', '.join(missing[:8])}{'…' if len(missing) > 8 else ''}")

    if args.dry_run:
        return 0 if not missing else 1

    if missing:
        print("error: enrich all terms before writing CSV", file=sys.stderr)
        return 1

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {CSV_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
