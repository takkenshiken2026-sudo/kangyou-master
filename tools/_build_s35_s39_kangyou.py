#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate write_kangyou_hub_s35-s39_content.py."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
from _hub_content_emit import emit_cmp, emit_mis, emit_num, fix_entry  # noqa: E402

with (ROOT / "data/glossary_terms.csv").open(encoding="utf-8-sig") as _f:
    GLOSS = {r["term"] for r in csv.DictReader(_f)}

_TAIL = "管業試験では用語集と条文の対応づけが得点の鍵になります。最新の試験要項もあわせて確認してください。"


def _rel(*terms: str) -> str:
    ok = [t for t in terms if t in GLOSS]
    for d in ("管理規約", "総会", "区分所有法", "管理組合", "修繕積立金", "長期修繕計画"):
        if len(ok) >= 2:
            break
        if d in GLOSS and d not in ok:
            ok.append(d)
    return ";".join(ok[:3])


def _t(title: str, batch: str) -> str:
    return title


def _faq(qa):
    return [(q, a if len(a) >= 100 else a + _TAIL) for q, a in qa]


THEMES = [
    ("kumiai-unyou", "管理組合運営", "K", ("管理組合", "管理者"), "管理組合;管理者", "組合の基本決定（区分所有法）", ("管理組合", "管理会社")),
    ("shuzen-tumitate", "修繕積立", "K", ("修繕積立金", "長期修繕計画"), "修繕積立金;長期修繕計画", "12年目安（見直し・ガイド）", ("修繕積立金", "修繕費")),
    ("sokai-unyou", "総会運営", "K", ("総会", "理事会"), "総会;理事会", "招集通知は規約で定める", ("総会", "理事会")),
    ("kanri-itaku", "管理委託", "K", ("マンション標準管理委託契約書", "管理組合"), "管理組合;管理費", "委託契約は組合が締結", ("管理組合", "マンション管理業者")),
    ("tekiseika-hou", "適正化法", "T", ("管理業務主任者", "管理業務主任者の届出"), "管理業務主任者;更新登録", "5年ごとに更新（登録・要項）", ("管理業務主任者の届出", "マンション管理業者")),
    ("kubun-shoyu", "区分所有", "K", ("区分所有者", "専有部分"), "区分所有者;専有部分", "床面積割合（規約・目安）", ("区分所有者", "共用部分")),
    ("kanrinin", "管理員", "T", ("管理員", "管理員の配置"), "管理員;管理員の配置", "一定規模以上（施行規則確認）", ("管理員", "管理業務主任者")),
    ("kaikei-kansa", "会計監査", "K", ("監査", "監査報告"), "監査;管理組合会計", "規約・実務で定める", ("監査", "管理組合会計")),
    ("tatekae", "建替え", "K", ("建替え", "建替え決議"), "建替え;5分の4議決権", "5分の4以上（建替え・条文確認）", ("建替え", "特別決議")),
    ("kangyou-shiken", "管業試験", "B", ("管理業務主任者試験", "管理業務主任者"), "管理業務主任者試験;管理業務主任者", "50問（マークシート・要項確認）", ("管理業務主任者試験", "マンション管理士")),
]

BATCH_ANGLE = {
    "S35": "基礎整理", "S36": "実務連動", "S37": "試験頻出", "S38": "判例・ガイド", "S39": "横断総合",
}


def _cmp(slug, title, cat, t1, t2, summary):
    return fix_entry({
        "slug": slug, "title": title, "cat": cat, "tags": f"{t1};{t2}",
        "summary": summary, "labels": f"{t1};{t2}",
        "axes": [
            ("主体", [f"{t1}中心", f"{t2}中心"]),
            ("手続", ["総会・理事会", "届出・規約"]),
            ("数値", ["5分の4等", "規約・条文"]),
            ("試験", [f"「{t1}＝{t2}」", "「同一決議」"]),
            ("混同", ["管業決定", "管理会社決定"]),
        ],
        "article_title": f"{title}｜管業",
        "lead": summary + "管理組合・総会・管業の権限を表で整理してください。",
        "points": f"{t1}と{t2}を分離;決議要件;管業は支援;試験の正誤肢に注意",
        "mistakes": f"{t1}＝{t2};管業が決定;過半数で規約変更;試験の正誤肢に注意",
        "tip": f"「{t1}と{t2}を分ける」。", "related": _rel(t1, t2),
        "qa": _faq([
            (f"{t1}の要点は？", f"{summary}{t1}の主体・手続を用語集で確認してください。"),
            (f"{t2}との違いは？", f"{t2}は別枠です。比較表を作成してください。"),
            ("試験対策の進め方は？", "決議四段表・機関表を作成し、過去問を反復してください。"),
            ("確認先はどこですか？", "区分所有法・適正化法・用語集を参照してください。"),
        ]),
    })


def _num(slug, title, cat, tag, summary, highlight, rel):
    return fix_entry({
        "slug": slug, "title": title, "cat": cat, "tags": tag, "summary": summary,
        "highlight": highlight,
        "items": [
            ("数値", highlight.split("（")[0], "試験頻出"),
            ("根拠", "区分所有法等", "条文確認"),
            ("主体", "管理組合", "管業は支援"),
            ("試験", "混同肢", "正誤確認"),
            ("確認", "用語集", "最新要項"),
        ],
        "article_title": f"{title}｜管業",
        "lead": summary + "数値は条文・規約で確認してください。",
        "points": f"{highlight};条文確認;決議と区別;試験の正誤肢に注意",
        "mistakes": "数値固定暗記;管業が決定;決議混同;試験の正誤肢に注意",
        "tip": f"「{highlight.split('（')[0]}を確認」。", "related": rel,
        "qa": _faq([
            ("数値の要点は？", f"{summary}条文・規約で最新を確認してください。"),
            ("試験の引っかけは？", "普通・特別・建替え決議と混同しないでください。"),
            ("試験対策の進め方は？", "数値一覧表を作成し、過去問を反復してください。"),
            ("確認先はどこですか？", "区分所有法・適正化法・www.mankan.or.jpを参照してください。"),
        ]),
    })


def _mis(slug, title, cat, t1, t2, summary):
    return fix_entry({
        "slug": slug, "title": title, "cat": cat, "tags": f"{t1};{t2}",
        "summary": summary, "confusion": f"{t1}と{t2}の混同。",
        "patterns": [
            ("決議", "過半数", "5分の4", "決議誤"),
            ("主体", "管業", "管理組合", "主体誤"),
            ("機関", "理事会", "総会", "機関誤"),
            ("費用", "同一", "別枠", "費用誤"),
        ],
        "article_title": f"{title}｜管業",
        "lead": summary + "正しい整理を表にまとめてください。",
        "points": f"{t1}≠{t2};総会・理事会;管業は支援;試験の正誤肢に注意",
        "mistakes": "同一視;管業決定;理事会のみ;試験の正誤肢に注意",
        "tip": f"「{t1}と{t2}は別」。", "related": _rel(t1, t2),
        "qa": _faq([
            ("誤りの内容は何ですか？", f"{summary}典型誤答として頻出です。"),
            ("正しい理解は何ですか？", f"{t1}と{t2}を機関・決議・主体で分けてください。"),
            ("試験対策の進め方は？", "誤答パターン表を作成し、過去問を反復してください。"),
            ("確認先はどこですか？", "区分所有法・用語集を参照してください。"),
        ]),
    })


def _build(batch: str) -> None:
    sfx = f"-{batch.lower()}"
    angle = BATCH_ANGLE[batch]
    cmps, nums, miss = [], [], []
    for slug_base, theme, cat, (t1, t2), tag, highlight, (m1, m2) in THEMES:
        cmps.append(_cmp(
            f"{slug_base}-cmp{sfx}", _t(f"{theme}：{t1}と{t2}の比較", batch), cat, t1, t2,
            f"{theme}（{angle}）として{t1}と{t2}の関係を整理します。",
        ))
        nums.append(_num(
            f"{slug_base}-num{sfx}", _t(f"{theme}：{highlight.split('（')[0]}の数値", batch), cat, tag,
            f"{theme}（{angle}）の数値・要件を整理します。", highlight, _rel(*tag.split(";")),
        ))
        miss.append(_mis(
            f"{slug_base}-mis{sfx}", _t(f"{theme}：{m1}と{m2}の混同誤り", batch), cat, m1, m2,
            f"{theme}（{angle}）で{m1}と{m2}を同一視する典型誤り。",
        ))
    header = f'''# -*- coding: utf-8 -*-
"""管理業務主任者 知識ハブ {batch} 追加分（各10件）."""

from tools.write_kangyou_hub_s30_content import _OFFICIAL, cmp, mis, num

T, K, B = "管理適正化法", "区分所有法", "判例・横断総合"

'''
    out = TOOLS / f"write_kangyou_hub_{batch.lower()}_content.py"
    parts = [header, "COMPARISONS_ADD = [\n"] + [emit_cmp(c) for c in cmps]
    parts += ["]\n\nNUMBERS_ADD = [\n"] + [emit_num(n) for n in nums]
    parts += ["]\n\nMISTAKES_ADD = [\n"] + [emit_mis(m) for m in miss]
    parts.append("]\n")
    out.write_text("".join(parts), encoding="utf-8")
    print("wrote", out)


def main() -> None:
    for batch in ("S35", "S36", "S37", "S38", "S39"):
        _build(batch)


if __name__ == "__main__":
    main()
