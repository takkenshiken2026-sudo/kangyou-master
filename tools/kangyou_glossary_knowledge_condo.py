# -*- coding: utf-8 -*-
"""区分所有法・標準管理規約の用語知識辞書を構築する。"""

from __future__ import annotations

import csv
from pathlib import Path

from tools.kangyou_glossary_content_helpers import build_entry_from_row

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "glossary_terms.csv"
TARGET_CATEGORIES = {"区分所有法", "標準管理規約"}

BASE_KEYS = (
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


def _clean(value: str | None) -> str:
    return (value or "").strip()


def _paragraphize(text: str) -> str:
    """CSV の単文を最低2段落に分ける。"""
    clean_text = _clean(text)
    if not clean_text:
        return ""
    if "\n\n" in clean_text:
        return clean_text
    if "。" in clean_text:
        parts = [p for p in clean_text.split("。") if p]
        if len(parts) >= 2:
            first = parts[0] + "。"
            rest = "。".join(parts[1:])
            if rest and not rest.endswith("。"):
                rest += "。"
            return f"{first}\n\n{rest}"
    return f"{clean_text}\n\n過去問肢の主語・要件・決議割合をセットで確認してください。"


THRESHOLD_TABLE_HTML = (
    '<table class="seo-info-table">'
    "<thead><tr><th>決議ライン</th><th>典型論点</th><th>押さえ方</th></tr></thead>"
    "<tbody>"
    "<tr><td>5分の1</td><td>招集請求（少数区分所有者）</td>"
    "<td>議決権と人数要件の両方を条文で確認する。</td></tr>"
    "<tr><td>4分の3</td><td>規約の設定・変更・廃止（原則）</td>"
    "<td>「特別の影響」があるときは承諾要件が追加される。</td></tr>"
    "<tr><td>5分の4</td><td>建替え決議など高度な重大事項</td>"
    "<td>賛成割合と手続順序（招集通知・議事録）をセット暗記。</td></tr>"
    "</tbody></table>"
)

MEETING_TABLE_HTML = (
    '<table class="seo-info-table">'
    "<thead><tr><th>項目</th><th>総会</th><th>理事会</th></tr></thead>"
    "<tbody>"
    "<tr><td>位置付け</td><td>区分所有者全体の意思決定機関</td><td>業務執行の実務機関</td></tr>"
    "<tr><td>典型議題</td><td>規約変更・予算決算・重要修繕</td><td>日常管理・業者対応・総会準備</td></tr>"
    "<tr><td>試験の狙い</td><td>決議割合・招集手続・特別の影響</td><td>権限逸脱の有無・総会事項との峻別</td></tr>"
    "</tbody></table>"
)

PARTS_TABLE_HTML = (
    '<table class="seo-info-table">'
    "<thead><tr><th>区分</th><th>専有部分</th><th>共用部分</th></tr></thead>"
    "<tbody>"
    "<tr><td>帰属</td><td>各区分所有者</td><td>区分所有者全員の共有</td></tr>"
    "<tr><td>管理責任</td><td>所有者の専用使用・管理</td><td>管理組合が一体管理</td></tr>"
    "<tr><td>試験の軸</td><td>境界・立入り・専用使用権</td><td>持分・修繕費負担・規約共用</td></tr>"
    "</tbody></table>"
)

RESOLUTION_TABLE_HTML = (
    '<table class="seo-info-table">'
    "<thead><tr><th>決議種類</th><th>賛成割合</th><th>典型事項</th></tr></thead>"
    "<tbody>"
    "<tr><td>普通決議</td><td>過半数</td><td>予算・日常管理</td></tr>"
    "<tr><td>特別決議</td><td>4分の3</td><td>規約変更・重要修繕</td></tr>"
    "<tr><td>建替え決議</td><td>5分の4</td><td>建物の建替え</td></tr>"
    "</tbody></table>"
)

OVERRIDES: dict[str, dict[str, str]] = {
    "専有部分": {
        "short_def": "区分所有者が単独で所有する部分。境界・立入り・専用使用権の起点となる概念。",
        "definition": "専有部分とは、区分所有建物のうち各区分所有者が単独で所有する部分をいいます（区分所有法第2条）。試験では共用部分との境界、立入り、専用使用権との関係が頻出です。",
        "term_detail_body": (
            "専有部分は区分所有法の基本構造を成す概念で、各区分所有者が排他的に利用・管理する領域です。"
            "共用部分との境界が不明確だと修繕費負担や立入り権の議論が生じます。\n\n"
            "試験では「専有部分に該当するか」「専用使用権との違い」「立入りの可否」を問う肢が多く、"
            "条文第2条の定義と規約の具体規定をセットで確認する必要があります。\n\n"
            "バルコニー・専用庭等は規約や設計により専用部分・共用部分・専用使用権のいずれかに整理されるため、"
            "一律の暗記ではなく事案ごとの当てはめ練習が得点に直結します。"
        ),
        "exam_points": "区分所有法第2条の定義;共用部分との境界;専用使用権との区別;立入り（第64条）との関係",
        "comparison_table": PARTS_TABLE_HTML,
    },
    "共用部分": {
        "short_def": "区分所有者全員が共有する部分。管理組合が一体管理し、持分で負担を按分する。",
        "definition": "共用部分とは、区分所有建物のうち専有部分以外の部分で、区分所有者全員の共有に属する部分です（区分所有法第2条）。",
        "term_detail_body": (
            "共用部分は廊下・階段・エントランス等を含み、管理組合が一体として管理します。"
            "区分所有者は持分に応じて管理費・修繕積立金を負担します。\n\n"
            "規約共用部分・附属共用部分・一部共用部分など細分化された概念も出題され、"
            "「誰が管理責任を負うか」「修繕費の負担主体は誰か」を正確に判定することが得点の鍵です。"
        ),
        "exam_points": "区分所有法第2条;規約共用部分との区別;持分と負担按分;管理組合の一体管理",
        "comparison_table": PARTS_TABLE_HTML,
    },
    "管理組合": {
        "short_def": "区分所有者全員で構成する団体。共用部分の管理と区分所有者の共同利益を実現する。",
        "term_detail_body": (
            "管理組合は区分所有法第3条に基づき、区分所有者全員で構成される団体です。"
            "共用部分の管理、管理規約の設定・変更、総会・理事会の運営を担います。\n\n"
            "試験では管理組合の代表（理事長）、表示登記、存続、管理不全との関係が問われ、"
            "「管理組合＝管理業者」ではない点を常に意識してください。"
        ),
        "exam_points": "区分所有法第3条;団体性と意思決定機関;理事長の代表権;管理業者との役割分担",
    },
    "修繕積立金": {
        "short_def": "将来の大規模修繕に備える積立金。一般会計と区分して管理する。",
        "term_detail_body": (
            "修繕積立金は区分所有法第61条に基づき、将来の修繕に備えて区分所有者から徴収する積立金です。"
            "一般会計（管理費）と区分して会計処理し、目的外使用は原則認められません。\n\n"
            "積立金の額の決定、取崩し、長期修繕計画との整合が試験の定番論点です。"
            "「管理費と混同」「理事会だけで決められる」等の誤り肢に注意してください。"
        ),
        "exam_points": "区分所有法第61条;一般会計との区分;取崩し要件;長期修繕計画との関係",
    },
    "建替え": {
        "short_def": "区分所有建物を解体し新築する処分。5分の4の建替え決議が必要。",
        "term_detail_body": (
            "建替えは区分所有法第62条の建替え決議（5分の4）を経て行う重大な処分です。"
            "4分の3の規約変更や特別決議より高い賛成割合が要求されます。\n\n"
            "建替え等円滑化法との関係、特例部分的建替え、反対者の買取請求等も横断的に問われます。"
        ),
        "exam_points": "区分所有法第62条;5分の4決議;建替え等円滑化法との関係;反対者の権利",
        "comparison_table": THRESHOLD_TABLE_HTML,
    },
    "5分の1議決権": {
        "short_def": "少数区分所有者が集会招集請求に使う基準割合。人数要件と議決権要件を混同しない。",
        "exam_points": "5分の1は「何ができるか」を問う肢が頻出;請求主体（区分所有者）と対象（総会招集）を区別;4分の3・5分の4との比較で出題される",
        "common_mistakes": "5分の1を決議可決ラインと誤認する;人数要件だけで判断する;理事会決議にそのまま当てはめる",
        "memory_tip": "5分の1=『集めるための起点』、4分の3/5分の4=『決めるための賛成ライン』と整理する。",
        "comparison_table": THRESHOLD_TABLE_HTML,
    },
    "4分の3議決権": {
        "short_def": "規約変更等の重要事項で使う特別決議ライン（原則）。",
        "exam_points": "規約の設定・変更・廃止は4分の3が軸;特別の影響がある場合は承諾要件が追加;普通決議過半数との対比問題が頻出",
        "common_mistakes": "4分の3と5分の4の対象行為を取り違える;特別の影響の承諾を忘れる;『議決権』と『区分所有者数』の両建てを失念",
        "comparison_table": THRESHOLD_TABLE_HTML,
    },
    "5分の4議決権": {
        "short_def": "建替え等の極めて重大な処分・再編で要求される高い賛成割合。",
        "exam_points": "建替え決議は5分の4ラインを最優先で確認;4分の3事項との振り分けが最重要;通知・議事録など手続不備との組合せ肢に注意",
        "common_mistakes": "規約変更にも5分の4が必要と誤解する;割合のみ覚えて手続要件を落とす;総会事項と理事会事項を混同する",
        "comparison_table": THRESHOLD_TABLE_HTML,
    },
    "特別の影響": {
        "short_def": "規約変更が特定区分所有者に通常を超える不利益を与える場合に承諾を要する考え方。",
        "definition": "特別の影響とは、規約設定・変更・廃止の内容が、特定の区分所有者に対して受忍限度を超える不利益を課すと評価される場面を指します。標準管理規約論点として頻出です。",
        "term_detail_body": (
            "規約変更の成否は、まず決議割合（通常4分の3）を満たすかを確認し、その次に『特別の影響』の有無を検討します。\n\n"
            "特別の影響が認められる場合、当該区分所有者の承諾が必要になります。試験では、割合を満たしていても承諾欠缺で不適法となる肢が狙われます。"
        ),
        "exam_points": "割合要件→特別の影響→承諾要否の順で判断;単なる不便と法的な特別の影響を区別;総会決議要件とセットで頻出",
        "comparison_table": THRESHOLD_TABLE_HTML,
    },
    "総会": {
        "term_detail_body": (
            "総会は区分所有者全体の意思を形成する最高意思決定の場で、規約変更・予算決算・大規模修繕などを扱います。\n\n"
            "試験では決議割合（普通/特別）、招集手続、議事録、特別の影響の有無まで含めた総合問題として問われます。"
        ),
        "exam_points": "総会事項と理事会事項の線引き;普通決議と特別決議の割合;招集通知・議題限定・議決権行使方法",
        "comparison_table": MEETING_TABLE_HTML,
    },
    "理事会": {
        "term_detail_body": (
            "理事会は管理組合の業務執行を担う機関で、日常管理・業者対応・総会提出議案の準備を担います。\n\n"
            "総会専決事項を理事会のみで決めると権限逸脱となり得るため、試験では『理事会で足りるか』の判定が重要です。"
        ),
        "exam_points": "理事会の権限範囲と総会専決事項の区別;理事長の代表権との関係;緊急対応の可否と事後承認",
        "comparison_table": MEETING_TABLE_HTML,
    },
    "理事会の権限": {
        "comparison_table": MEETING_TABLE_HTML,
        "exam_points": "理事会決議で可能な事項を限定的に把握;総会決議事項を理事会で代替できない;条文と標準管理規約の文言比較が有効",
    },
    "総会決議要件": {
        "comparison_table": THRESHOLD_TABLE_HTML,
        "exam_points": "普通決議/特別決議/建替え決議の割合比較;5分の1招集請求との違い;特別の影響がある場合の承諾要件をセットで確認",
    },
    "普通決議": {
        "short_def": "総会の通常決議。過半数の賛成で成立する。",
        "comparison_table": RESOLUTION_TABLE_HTML,
        "exam_points": "過半数の意味（出席者か全体か）;特別決議との対比;標準管理規約の具体規定",
    },
    "特別決議": {
        "short_def": "重要事項を決める決議。原則4分の3の賛成が必要。",
        "comparison_table": RESOLUTION_TABLE_HTML,
        "exam_points": "4分の3の対象事項;特別の影響と承諾;普通決議との使い分け",
    },
    "管理規約": {
        "short_def": "区分所有者間の団体内部ルール。設定・変更・廃止には4分の3の特別決議が原則必要。",
        "term_detail_body": (
            "管理規約は区分所有法第13条に基づき、管理組合の組織・運営・共用部分の管理等を定める規約です。"
            "標準管理規約をモデルに策定されることが多く、試験では規約と委託契約書の役割分担が問われます。\n\n"
            "規約の設定・変更・廃止は原則4分の3の特別決議が必要で、特別の影響がある場合は承諾も必要です。"
        ),
        "exam_points": "区分所有法第13条;4分の3決議;特別の影響と承諾;標準管理規約との関係",
    },
    "マンション標準管理規約": {
        "short_def": "管理組合運営の標準モデル。総会・理事会・会計・修繕の実務ルールを体系化。",
        "term_detail_body": (
            "マンション標準管理規約は、管理組合の運営実務を具体化した標準書式です。"
            "区分所有法の条文を補完し、総会招集、理事会権限、修繕区分、会計処理等を詳細に定めます。\n\n"
            "試験では条文と標準管理規約の対応関係、普通決議・特別決議の具体規定、"
            "滞納者への措置等が頻出です。"
        ),
        "exam_points": "区分所有法との対応;決議種類と割合;理事会・総会の権限分担;会計・修繕の実務規定",
    },
}


def _build_knowledge() -> dict[str, dict[str, str]]:
    knowledge: dict[str, dict[str, str]] = {}
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if _clean(row.get("category")) not in TARGET_CATEGORIES:
                continue

            term = _clean(row.get("term"))
            if not term:
                continue

            item = build_entry_from_row(row)

            if _clean(row.get("importance")) == "A":
                q = _clean(row.get("example_question"))
                a = _clean(row.get("example_answer"))
                if q:
                    item["example_question"] = q
                if a:
                    item["example_answer"] = a

            if term in OVERRIDES:
                item.update(OVERRIDES[term])

            knowledge[term] = item

    return dict(sorted(knowledge.items(), key=lambda x: x[0]))


KNOWLEDGE: dict[str, dict[str, str]] = _build_knowledge()
