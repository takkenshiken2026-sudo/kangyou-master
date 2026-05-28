#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KNOWLEDGE モジュールの手作り品質を検証する。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST = ROOT / "data" / "kangyou_glossary_manifest.json"
HANDCRAFTED_DIR = ROOT / "data" / "kangyou_glossary_handcrafted"
HANDCRAFTED_FILES = ["civil.json", "condo.json", "ops.json", "misc.json"]
MODULES = [
    "kangyou_glossary_knowledge_civil.py",
    "kangyou_glossary_knowledge_condo.py",
    "kangyou_glossary_knowledge_ops.py",
    "kangyou_glossary_knowledge_misc.py",
]

REQUIRED = (
    "short_def",
    "definition",
    "term_detail_body",
    "exam_points",
    "common_mistakes",
    "memory_tip",
    "explanation",
    "article_lead",
    "faq_1_question",
    "faq_1_answer",
    "faq_2_question",
    "faq_2_answer",
)

FORBIDDEN = (
    "一次情報と照合しながら覚えてください",
    "意味と試験での使われ方を整理します",
    "関連ページで対比",
    "横断論点として、関連用語・過去問・実践演習を",
    "定義を一文で言える;適用場面",
    "過去問・実践演習で",
    "セットで復習すると定着率が上がります",
)


def load_knowledge() -> dict[str, dict[str, str]]:
    if HANDCRAFTED_DIR.is_dir():
        merged: dict[str, dict[str, str]] = {}
        for name in HANDCRAFTED_FILES:
            path = HANDCRAFTED_DIR / name
            if not path.is_file():
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            for term, payload in data.items():
                if term in merged:
                    raise SystemExit(f"duplicate: {term}")
                merged[term] = payload
        if merged:
            return merged
    merged: dict[str, dict[str, str]] = {}
    for name in MODULES:
        path = ROOT / "tools" / name
        spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
        if not spec or not spec.loader:
            raise SystemExit(f"missing module: {name}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        data = getattr(mod, "KNOWLEDGE", {})
        for term, payload in data.items():
            if term in merged:
                raise SystemExit(f"duplicate: {term}")
            merged[term] = payload
    return merged


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    knowledge = load_knowledge()
    errors: list[str] = []
    warnings: list[str] = []

    for term, meta in manifest.items():
        if term not in knowledge:
            errors.append(f"missing: {term}")
            continue
        entry = knowledge[term]
        for key in REQUIRED:
            if not str(entry.get(key) or "").strip():
                errors.append(f"{term}: missing {key}")
        body = str(entry.get("term_detail_body") or "")
        if len(body) < 280:
            errors.append(f"{term}: body too short ({len(body)} chars)")
        if body.count("\n\n") < 2:
            errors.append(f"{term}: body needs 3+ paragraphs")
        blob = json.dumps(entry, ensure_ascii=False)
        for marker in FORBIDDEN:
            if marker in blob:
                errors.append(f"{term}: forbidden marker '{marker}'")
        if meta["importance"] == "A":
            if not str(entry.get("example_question") or "").strip():
                errors.append(f"{term}: A-rank missing example_question")
            if not str(entry.get("example_answer") or "").strip():
                errors.append(f"{term}: A-rank missing example_answer")
        ep = str(entry.get("exam_points") or "")
        if ep.count(";") < 2:
            warnings.append(f"{term}: exam_points has fewer than 3 items")

    extra = set(knowledge) - set(manifest)
    if extra:
        errors.append(f"extra terms: {', '.join(sorted(extra)[:5])}")

    bodies = [str(v.get("term_detail_body") or "") for v in knowledge.values()]
    dup = len(bodies) - len(set(bodies))

    print(f"manifest: {len(manifest)}")
    print(f"knowledge: {len(knowledge)}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")
    print(f"duplicate bodies: {dup}")
    for e in errors[:30]:
        print("ERROR:", e)
    if len(errors) > 30:
        print(f"... and {len(errors)-30} more")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
