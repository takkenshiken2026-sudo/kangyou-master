#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用語ごとの試験向け本文を生成し glossary_terms.csv を更新する。"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "glossary_terms.csv"
JSON_PATH = ROOT / "data" / "kangyou_glossary_content.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.site_config import exam_name  # noqa: E402

EXAM = exam_name()
BRAND = "管業マスター"

# (term, core定義, 試験要点, 誤答パターン, 比較対象語)
SPECS: list[tuple[str, str, str, str, str]] = [
    ("同時履行の抗弁", "双務契約の当事者が、相手方の債務が弁済期にあり、その履行の提供があるまで、自己の債務の履行を拒むことができる抗弁権（民法533条）。", "弁済期・履行の提供・双務契約の3要件をセットで確認", "弁済期前や履行提供がないのに拒めるとする肢", "催告解除"),
    ("催告解除", "債務不履行により契約を解除する制度で、原則として相当期間を定めた催告が必要（民法541条）。", "催告→相当期間→解除の順序", "催告なしにいつでも解除できるとする肢", "無催告解除"),
    ("無催告解除", "催告を要せず直ちに解除できる法定事由がある場合の解除（民法542条各号）。", "各号の法定事由に厳密に当てはめる", "すべての不履行で無催告解除できるとする肢", "催告解除"),
    ("双務契約", "当事者が互いに対価関係にある給付を負担する契約。売買・賃貸借・請負などが典型。", "互いの給付が対価関係にあるかを確認", "単務契約と混同する", "単務契約"),
    ("債務不履行", "債務者が債務の本旨に従った履行をしない状態。解除・損害賠償の前提。", "履行遅滞・履行不能・不完全履行の区別", "軽微な遅滞ですぐ解除できるとする肢", "履行遅滞"),
    ("損害賠償", "債務不履行等により生じた損害を金銭で填補する制度（民法415条ほか）。", "損害・因果関係・相当因果関係", "同時履行の抗弁と混同して請求権が消滅すると誤解", "契約の解除"),
    ("契約の解除", "契約関係を将来に向かって消滅させる制度（民法540条）。", "解除原因・解除権者・解除意思表示", "解除と損害賠償請求が排他と誤解", "催告解除"),
    ("債務の承認", "時効完成後の債務を追認し、時効完成の効力を阻害する意思表示（民法152条）。", "時効完成後であること", "時効完成前の承認で時効が伸びると誤解", "消滅時効"),
    ("消滅時効", "一定期間権利を行使しないと消滅する制度（民法166条）。", "起算点・更新・完成", "すべての債権が2年で消滅すると誤解", "債務の承認"),
    ("無断転貸", "賃借人が貸主の承諾なく第三者に転貸すること（民法612条）。", "承諾の有無・解除原因", "転借人がいれば当然解除と誤解", "賃貸借契約"),
    ("賃貸借契約", "当事者の一方が物の使用収益をさせ、他方が賃料を支払う契約（民法601条）。", "使用収益対象・賃料・期間", "売買と混同", "使用貸借"),
    ("原状回復", "賃貸借終了時に物件を原状に戻す義務（民法621条・621条の2）。", "通常損耗と借主負担の線引き", "すべての修繕を借主負担とする肢", "明渡し"),
    ("敷金", "賃料等の担保として預けられる金銭。返還・控除のルールが問題化。", "返還時期・控除範囲", "敷金は賃料と同一視", "預り金"),
    ("連帯保証", "主たる債務者と連師して債務を負担する保証（民法454条）。", "連帯保証と普通保証の違い", "保証人は必ず連帯と誤解", "保証"),
    ("共有物", "数人が持分に従い単一の物を共有する状態（民法249条）。", "持分・管理・処分", "区分所有と混同", "区分所有者"),
    ("請負契約", "仕事の完成を約し報酬を受ける契約（民法632条）。", "完成・目的物・報酬", "委任・組合契約と混同", "委任契約"),
    ("委任契約", "法律行為を委託し報酬を受ける契約（民法643条）。", "法律行為・任意性", "請負・組合と混同", "請負契約"),
    ("寄託契約", "物の保管を委託する契約（民法657条）。", "保管・返還義務", "組合契約と混同", "組合契約"),
    ("組合契約", "共同事業の利益を分配する契約（民法675条）。", "共同事業・利益分配", "委任・請負と混同", "委任契約"),
    ("弁済期", "債務の履行をすべき時期（民法475条）。", "弁済期と同時履行の抗弁", "期限の利益喪失と混同", "履行遅滞"),
    ("履行遅滞", "弁済期経過後も履行がない状態（民法412条）。", "弁済期・催告の関係", "遅滞ですぐ無催告解除", "履行不能"),
    ("履行不能", "物理的・法律的に履行が不能な状態。", "当初不能と嗣後不能", "すべて不能で解除不要", "履行遅滞"),
    ("契約不適合責任", "引渡し時に種類・品質・数量が契約内容に適合しない場合の責任（民法562条）。", "追完・減額・解除", "瑕疵担保と旧称混同のみ", "損害賠償"),
    ("危険負担", "双務契約で一方の給付不能時に他方の給付義務が消滅する制度（民法536条）。", "給付不能の原因・不可帰性", "損害賠償と混同", "双務契約"),
    ("相殺", "互いに同種の債権を有する場合に対等額で消滅させる制度（民法505条）。", "同種・対立・弁済期", "任意相殺と混同", "債権譲渡"),
    ("債権譲渡", "債権を第三者に移転させる制度（民法466条）。", "対抗要件・制限", "債務承継と混同", "相殺"),
    ("使用貸借", "無償で物の使用収益をさせる契約（民法593条）。", "無償性", "賃貸借と混同", "賃貸借契約"),
    ("定期建物賃貸借", "更新がなく期間満了で終了する建物賃貸借（借地借家法38条）。", "更新なし・事前説明", "普通借家と混同", "賃貸借契約"),
    ("借地借家法", "借地・借家関係を規律する特別法。強行規定が多い。", "普通/定期・更新・正当事由", "民法のみで判断", "賃貸借契約"),
    ("賃貸借の対抗力", "建物引渡し・登記等により第三者に対抗できる要件（借地借家法31条）。", "引渡し・登記・占有", "契約だけで対抗", "明渡し"),
    ("明渡し", "賃貸借終了後に物件を明け渡す義務。", "終了原因・期間", "解除なしに明渡請求", "原状回復"),
    ("賃料", "賃貸借の対価。支払時期・増減・滞納が論点。", "支払期日・増減", "管理費と混同", "管理費"),
    ("借地権", "借地借家法上の借地に関する権利。", "普通借地・定期借地", "所有権と混同", "借家権"),
    ("借家権", "建物賃貸借に基づく借家の地位。", "普通借家・定期借家", "区分所有権と混同", "借地権"),
    ("地上権", "他人の土地に工作物・竹木を所有するため土地を使用する物権（民法265条）。", "物権性・対抗", "賃借権と混同", "地役権"),
    ("地役権", "他人の土地を自己の土地の便益のために使用する物権（民法280条）。", "要役地・承役地", "地上権と混同", "地上権"),
    ("表見代理", "無権代理でも見た目から有権と信じさせた場合の効果（民法109条）。", "基本表見・権限授与表見", "無権代理と混同", "無権代理"),
    ("無権代理", "代理権なしでなした代理（民法113条）。", "追認・催告", "表見代理と混同", "表見代理"),
    ("債務承継", "債務者の変更。相続・承継等。", "承認・包括承継", "債権譲渡と混同", "相続と区分所有"),
    ("占有", "物を実支配する事実（民法180条）。", "占有と所有の区別", "所有権と同一視", "区分所有者"),
    ("単務契約", "一方のみが給付を負担する契約。", "双務との対比", "双務契約と混同", "双務契約"),
    ("代位弁済", "第三者が債務者に代わって弁済すること（民法499条）。", "求償権", "相殺と混同", "相殺"),
    ("連帯債務", "数人が同一内容の債務を負担する制度（民法436条）。", "外部関係・内部関係", "連帯保証と混同", "連帯保証"),
    ("保証", "主たる債務者が履行しない場合に履行責任を負う制度（民法446条）。", "催告の抗弁・検索の抗弁", "連帯保証と混同", "連帯保証"),
    ("解除と損害賠償", "解除後も損害賠償請求が可能な場合がある（民法545条）。", "解除と損害賠償の并存", "解除すると賠償も消滅", "損害賠償"),
]

# 区分所有法・規約など — 続きは CATEGORY_DEFAULTS + 個別 SPECS で補完
CATEGORY_DEFAULTS: dict[str, str] = {
    "区分所有法": "マンション等の区分所有関係を定める基本法。専用部分・共用部分・管理組合が柱。",
    "標準管理規約": "管理組合の運営ルールのモデル。総会・理事会・決議要件が頻出。",
    "建築・設備": "建築基準法・消防法・昇降機規則等に基づく建物・設備の安全と維持。",
    "会計・税務": "管理組合の会計処理・財務報告・税務上の取扱い。",
    "管理適正化法": "マンション管理の適正化を推進する法律。資格・73条書面・管理計画。",
    "標準管理委託契約書・指針": "管理委託契約の標準条項。委託費・業務範囲・再委託。",
    "品確法・建替円滑化法等": "住宅品質確保と建替え手続の関連法令。",
    "宅建業法": "不動産取引の規制。35条書面・重要事項説明。",
    "判例・横断総合": "判例・複数分野を横断する論点。比較整理が得点の鍵。",
}


def split_legal(legal: str) -> str:
    return legal.replace(";", "・") if legal else ""


def spec_map() -> dict[str, tuple[str, str, str, str, str]]:
    m: dict[str, tuple[str, str, str, str, str]] = {}
    for item in SPECS:
        m[item[0]] = item
    return m


def build_article(row: dict[str, str], spec: tuple[str, str, str, str, str] | None) -> dict[str, str]:
    term = row["term"].strip()
    cat = row["category"].strip()
    legal = row["legal_basis"].strip()
    imp = row["importance"].strip()
    related = [x.strip() for x in row.get("related_terms", "").split(";") if x.strip()]
    rel_txt = "、".join(related[:3]) if related else "関連用語"

    if spec:
        _, core, exam, trap, compare = spec
    else:
        core = f"{term}は{cat}分野で{split_legal(legal) or '関連法令'}上の重要概念です。"
        exam = f"{term}の定義と適用場面を条文・規約と照合して確認"
        trap = f"{term}を似た用語と混同する"
        compare = related[0] if related else ""

    p1 = f"{core} {EXAM}では、{split_legal(legal) or cat}を根拠に定義・要件・効果を問う問題が出ます。"
    p2 = (
        f"実務・試験ともに「{exam}」が判断の軸になります。"
        f"選択肢では{trap}肢が多いため、要件の欠けた肢を消去する思考が有効です。"
    )
    p3 = (
        f"{term}は{rel_txt}とセットで整理すると理解が定着します。"
        f"管業マスターの過去問・実践演習で{cat}フィルタを使い、関連問題を解き直してください。"
    )

    compare_html = ""
    if compare and compare in row.get("related_terms", ""):
        compare_html = (
            '<table class="seo-info-table"><thead><tr><th>比較</th>'
            f"<th>{term}</th><th>{compare}</th></tr></thead><tbody>"
            f"<tr><th>覚え方</th><td>{exam}</td><td>関連ページで対比</td></tr>"
            "</tbody></table>"
        )

    article = {
        "short_def": core if core.endswith("。") else core + "。",
        "definition": f"{term}は、{core.rstrip('。')}。{CATEGORY_DEFAULTS.get(cat, cat + 'の重要論点')}。",
        "term_detail_body": f"{p1}\n\n{p2}\n\n{p3}",
        "exam_points": f"{exam};{split_legal(legal) or cat}の根拠を明示できる;関連語（{rel_txt}）との違いを説明できる",
        "common_mistakes": f"{trap};要件の一部だけ暗記して判断する;最新の改正・規約改定を見落とす",
        "memory_tip": f"{term}＝{split_legal(legal) or cat}。{compare or rel_txt}と表で対比。",
        "explanation": f"過去問では{exam}が問われます。{trap}選択肢に注意してください。",
        "article_lead": f"{term}の意味と{EXAM}での判定ポイントを、{split_legal(legal) or cat}の文脈で整理します。",
        "faq_1_question": f"{term}の定義を試験用に一言で言うと？",
        "faq_1_answer": core.rstrip("。") + "。",
        "faq_2_question": f"{term}と混同しやすい論点は？",
        "faq_2_answer": f"{compare or rel_txt}との違いを比較表で整理すると定着しやすくなります。",
    }
    if compare_html:
        article["comparison_table"] = compare_html
    if imp == "A":
        article["example_question"] = f"{term}に関する次の記述のうち、最も適切でないものはどれか。"
        article["example_answer"] = f"{exam}。{trap}とする記述が誤りになりやすい。"
    return article


def load_extra_specs() -> None:
    """CSV にあって SPECS にない語向けの追加定義（区分所有・規約・会計等）。"""
    extra_path = ROOT / "tools" / "kangyou_glossary_specs_extra.json"
    if not extra_path.is_file():
        return
    data = json.loads(extra_path.read_text(encoding="utf-8"))
    for term, payload in data.items():
        if term not in {s[0] for s in SPECS}:
            SPECS.append(
                (
                    term,
                    payload["core"],
                    payload["exam"],
                    payload.get("trap", f"{term}の要件を見落とす"),
                    payload.get("compare", ""),
                )
            )


def main() -> int:
    load_extra_specs()
    sm = spec_map()
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        term = row["term"].strip()
        article = build_article(row, sm.get(term))
        out[term] = article
        for k, v in article.items():
            row[k] = v
        if not row.get("article_title"):
            row["article_title"] = f"{term}とは？{EXAM}で押さえる意味と試験ポイント"

    JSON_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    header = list(rows[0].keys()) if rows else []
    if "comparison_table" not in header:
        header.append("comparison_table")
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"updated {len(rows)} terms -> {CSV_PATH}")
    print(f"wrote {JSON_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
