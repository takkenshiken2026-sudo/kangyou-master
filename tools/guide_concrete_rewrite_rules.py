#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""試験ガイド手書きリライト：具体性＋文中例示の追加ルール（v1.1）。"""

from __future__ import annotations

import re

from tools.editorial_quality import norm

# 文中の例示・場面描写（いずれか1つ以上を節本文に入れる）
EXAMPLE_MARKERS_RE = re.compile(
    r"例えば|たとえば|たとえ|例として|イメージ(?:として|すると)|好比|想像すると|"
    r"具体(?:例|的)には|一例として|場面として|ケース(?:として|例)|"
    r"たとえば[、,]?[0-9０-９月火水木金土日曜]|"
    r"「[^」]{6,48}」(?:の|と|なら|では)"
)

# 節本文の最低例示数（5節中）
MIN_SECTIONS_WITH_EXAMPLE = 3

# 1節あたりの具体アンカー（数字・日付・固有名詞など）—表の行は除く簡易判定
CONCRETE_ANCHOR_RE = re.compile(
    r"\d+[％%]|"
    r"\d+[問時間分]|"
    r"\d+:\d+|"
    r"[0-9０-９]+月[0-9０-９]+日|"
    r"令和[0-9０-９]+年度|"
    r"第[0-9０-９]+章|"
    r"P\.[0-9０-９]+|"
    r"区分所有法|管理組合|修繕積立|総会|マン管"
)

PIPE_TABLE_ROW_RE = re.compile(r"^\|", re.M)

# 分野別記事に載せない学習運用ジャargon（v1.1 テンプレ混入防止）
FIELD_GUIDE_FORBIDDEN_RE = re.compile(
    r"5行表|7行表|/terms/|Day3解き直し|11/22新規0|9月通し\d+/50"
)

# 分野別記事に最低1つは試験論点語が必要
FIELD_GUIDE_SUBSTANCE_RE = re.compile(
    r"条文|論点|制度|法第|借地|借家|契約|権利|義務|規定|敷金|更新|正当事由|保証|賃貸|"
    r"規約|総会|決議|管理組合|理事会|普通決議|特別決議|"
    r"修繕|点検|長期修繕|設備|建築基準|維持修繕|積立|"
    r"専有部分|共用部分|区分所有|集会|議決|"
    r"管理費|収支|決算|按分|会計報告|監査|"
    r"適正化|登録|届出|遵守規定|適正原価|管理業者|"
    r"品確|建替|認定|円滑化|"
    r"判例|横断|分野またぎ|"
    r"委託|受託|報酬|指針|宅建|重要事項|媒介"
)


def _body_without_table(body: str) -> str:
    lines = [ln for ln in body.split("\n") if ln.strip() and not PIPE_TABLE_ROW_RE.match(ln.strip())]
    return "\n".join(lines)


def section_has_example(body: str) -> bool:
    prose = _body_without_table(norm(body))
    return bool(prose and EXAMPLE_MARKERS_RE.search(prose))


def section_concrete_anchor_count(body: str) -> int:
    prose = _body_without_table(norm(body))
    if not prose:
        return 0
    return len(CONCRETE_ANCHOR_RE.findall(prose))


def validate_concrete_rewrite(slug: str, patch: dict[str, str]) -> list[str]:
    """REWRITES 1件分の具体性＋例示チェック。ERROR 文言の list を返す。"""
    errors: list[str] = []
    prefix = f"{slug}:"

    lead = norm(patch.get("lead"))
    if lead and not EXAMPLE_MARKERS_RE.search(lead) and not re.search(r"\d+週|\d+か月", lead):
        errors.append(
            f"{prefix} lead needs a micro-scenario (例えば/たとえば or 残り○週 など)"
        )

    example_sections = 0
    for n in range(1, 6):
        bcol = f"section_{n}_body"
        body = norm(patch.get(bcol))
        if not body:
            continue
        if section_has_example(body):
            example_sections += 1
        elif section_concrete_anchor_count(body) < 2:
            errors.append(
                f"{prefix} {bcol} needs 例えば/たとえば scene OR 2+ concrete anchors outside the table"
            )

    if example_sections < MIN_SECTIONS_WITH_EXAMPLE:
        errors.append(
            f"{prefix} need {MIN_SECTIONS_WITH_EXAMPLE}+ sections with 例えば/たとえば "
            f"(got {example_sections})"
        )

    errors.extend(validate_field_guide_genre(slug, patch))

    return errors


def validate_field_guide_genre(slug: str, patch: dict[str, str]) -> list[str]:
    """分野別 field-* 記事のジャンル適合（学習計画テンプレ混入を ERROR）。"""
    if not slug.startswith("field-"):
        return []
    errors: list[str] = []
    prefix = f"{slug}:"
    prose_cols = (
        ["lead", "user_intent"]
        + [f"section_{n}_body" for n in range(1, 6)]
        + [f"faq_{n}_answer" for n in range(1, 4)]
    )
    combined = ""
    for col in prose_cols:
        combined += norm(patch.get(col)) + "\n"
    if FIELD_GUIDE_FORBIDDEN_RE.search(combined):
        errors.append(
            f"{prefix} field guide must not use study-schedule jargon "
            f"(5行表, /terms/, Day3, 9月通し34/50 等). Link to study-plan instead."
        )
    section_bodies = "".join(norm(patch.get(f"section_{n}_body")) for n in range(1, 6))
    if section_bodies and not FIELD_GUIDE_SUBSTANCE_RE.search(section_bodies):
        errors.append(
            f"{prefix} field guide section bodies need exam substance "
            f"(条文/論点/借地借家法/契約 等)"
        )
    return errors
