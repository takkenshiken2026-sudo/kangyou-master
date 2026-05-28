# -*- coding: utf-8 -*-
"""
管理業務主任者 用語解説（残カテゴリ向け）知識データ。

対象カテゴリ:
- 標準管理委託契約書・指針
- 品確法・建替円滑化法等
- 宅建業法
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from tools.kangyou_glossary_content_helpers import build_entry_from_row, build_rich_body


TARGET_CATEGORIES = {
    "標準管理委託契約書・指針",
    "品確法・建替円滑化法等",
    "宅建業法",
}


TERM_CATEGORY_PAIRS = [
    ("マンション標準管理委託契約書", "標準管理委託契約書・指針"),
    ("定額委託業務費", "標準管理委託契約書・指針"),
    ("臨時委託業務", "標準管理委託契約書・指針"),
    ("アフターサービス", "標準管理委託契約書・指針"),
    ("管理事務", "標準管理委託契約書・指針"),
    ("委託業務の範囲", "標準管理委託契約書・指針"),
    ("契約の更新", "標準管理委託契約書・指針"),
    ("夜間急変取扱", "標準管理委託契約書・指針"),
    ("管理員室", "標準管理委託契約書・指針"),
    ("修繕アフターサービス", "標準管理委託契約書・指針"),
    ("品質確保促進法", "品確法・建替円滑化法等"),
    ("既存住宅状況調査", "品確法・建替円滑化法等"),
    ("建替え等円滑化法", "品確法・建替円滑化法等"),
    ("瑕疵担保責任", "品確法・建替円滑化法等"),
    ("10年瑕疵担保責任", "品確法・建替円滑化法等"),
    ("既存住宅売買", "品確法・建替円滑化法等"),
    ("宅地建物取引業", "宅建業法"),
    ("重要事項説明", "宅建業法"),
    ("35条書面", "宅建業法"),
    ("37条書面", "宅建業法"),
    ("クーリングオフ", "宅建業法"),
    ("媒介契約", "宅建業法"),
    ("宅建業者", "宅建業法"),
    ("共用部分規約案の説明", "宅建業法"),
    ("委託契約の解除", "標準管理委託契約書・指針"),
    ("委託契約の変更", "標準管理委託契約書・指針"),
    ("管理業務の報告", "標準管理委託契約書・指針"),
    ("管理業務の監査", "標準管理委託契約書・指針"),
    ("臨時委託業務費", "標準管理委託契約書・指針"),
    ("定額委託業務", "標準管理委託契約書・指針"),
    ("管理員の配置", "標準管理委託契約書・指針"),
    ("清掃業務", "標準管理委託契約書・指針"),
    ("警備業務", "標準管理委託契約書・指針"),
    ("修繕の発見報告", "標準管理委託契約書・指針"),
    ("委託者の指示", "標準管理委託契約書・指針"),
    ("損害賠償責任", "標準管理委託契約書・指針"),
    ("秘密保持", "標準管理委託契約書・指針"),
    ("再委託の制限", "標準管理委託契約書・指針"),
    ("指針", "標準管理委託契約書・指針"),
    ("建替え等円滑化法の手続", "品確法・建替円滑化法等"),
    ("既存住宅状況調査技術者", "品確法・建替円滑化法等"),
    ("住宅性能表示", "品確法・建替円滑化法等"),
    ("瑕疵担保責任の追完", "品確法・建替円滑化法等"),
    ("建替えの合意", "品確法・建替円滑化法等"),
    ("建替えの手続", "品確法・建替円滑化法等"),
    ("マンション建替え", "品確法・建替円滑化法等"),
    ("既存不適格", "品確法・建替円滑化法等"),
    ("リフォーム", "品確法・建替円滑化法等"),
    ("宅地建物取引業法", "宅建業法"),
    ("宅地建物取引士", "宅建業法"),
    ("業務上の規制", "宅建業法"),
    ("37条書面の交付", "宅建業法"),
    ("35条書面の交付", "宅建業法"),
    ("重要事項説明書", "宅建業法"),
    ("専有部分の売買", "宅建業法"),
    ("管理規約の説明", "宅建業法"),
    ("手付金", "宅建業法"),
    ("媒介契約書", "宅建業法"),
]


CATEGORY_CONTEXT = {
    "標準管理委託契約書・指針": {
        "focus": "委託契約の条項構造（業務範囲・費用区分・再委託・報告）",
        "mistake": "管理規約の規律と委託契約の規律を混同する",
        "memory": "条文番号より先に「誰の義務か（委託者/受託者）」で整理する",
    },
    "品確法・建替円滑化法等": {
        "focus": "制度趣旨（品質確保・再生円滑化）と手続要件",
        "mistake": "民法上の一般原則と特別法のルールを混同する",
        "memory": "目的規定→対象物件→期間・議決要件の順で覚える",
    },
    "宅建業法": {
        "focus": "取引段階ごとの義務（説明・書面交付・契約締結後対応）",
        "mistake": "35条書面と37条書面の交付時期・記載事項を逆に覚える",
        "memory": "取引フローを「説明→契約→書面」で固定して確認する",
    },
}


def _default_faqs(term: str, category: str) -> list[dict[str, str]]:
    return [
        {
            "question": f"{term}はどの論点とセットで問われますか？",
            "answer": (
                f"{category}では、定義だけでなく適用場面と関連書面を組み合わせた出題が多いです。"
                "過去問では要件の一部を欠いた肢を除外できるかが得点差になります。"
            ),
        },
        {
            "question": f"{term}を短時間で復習するコツは？",
            "answer": "1分で定義、1分で比較、1分で条文・指針の根拠を確認する3分復習が有効です。",
        },
    ]


def _default_examples(term: str, category: str) -> list[dict[str, str]]:
    return [
        {
            "question": f"{term}に関する記述として最も不適切なものを選べ。",
            "answer": (
                f"{category}の原則に照らし、主体・時期・要件のいずれかを欠く選択肢を誤りとして判定する。"
            ),
        }
    ]


def _build_default_entry(term: str, category: str) -> dict:
    ctx = CATEGORY_CONTEXT[category]
    body = build_rich_body(
        term,
        category,
        exam_hint=f"{ctx['focus']}を確認する",
    )
    return {
        "short_def": f"{term}は{category}で頻出の基本論点。定義と適用場面をセットで押さえる語句です。",
        "definition": (
            f"{term}とは、管理業務主任者試験の{category}分野で繰り返し問われる概念です。"
            "趣旨・要件・効果を区別して理解し、関連法令や標準書式との関係まで説明できる状態を目標にします。"
        ),
        "term_detail_body": body,
        "exam_points": (
            "定義を一文で言える;"
            "誰にどの義務が生じるか説明できる;"
            "時期・手続・書面の要件を判定できる;"
            "類似用語との違いを比較できる"
        ),
        "common_mistakes": (
            f"{ctx['mistake']};"
            "語句だけ暗記して要件を落とす;"
            "条文趣旨を確認せずに語感で選択肢を選ぶ"
        ),
        "memory_tip": (
            f"{ctx['memory']}。"
            "過去問で誤答したら、誤った選択肢のどの要件が欠けていたかを1行でメモして再確認する。"
        ),
        "explanation": (
            f"{term}は、正誤判定で「時期」「主体」「書面名」の取り違えを狙う問題が多い論点です。"
            "定義暗記だけでなく、出題パターン別に判断手順を固定すると得点が安定します。"
        ),
        "article_lead": (
            f"{term}の意味・根拠・出題パターンを、管理業務主任者試験向けに短時間で復習できる形で整理します。"
        ),
        "faqs": _default_faqs(term, category),
        "examples": _default_examples(term, category),
    }


SPECIAL_OVERRIDES = {
    "マンション標準管理委託契約書": {
        "short_def": "マンション標準管理委託契約書は、管理組合と管理業者の委託関係を体系化した標準書式です。",
        "definition": (
            "マンション標準管理委託契約書とは、管理事務の範囲、費用、責任、再委託、報告義務などを明確化するための標準モデルです。"
            "試験では、契約条項と管理規約の役割分担を区別できるかが問われます。"
        ),
        "comparison_table": (
            "<table class='seo-info-table'><tbody>"
            "<tr><th>比較項目</th><th>標準管理委託契約書</th><th>標準管理規約</th></tr>"
            "<tr><th>規律対象</th><td>管理組合と管理業者の契約関係</td><td>区分所有者間の団体内部ルール</td></tr>"
            "<tr><th>典型論点</th><td>再委託、報告、費用区分、責任</td><td>総会・理事会運営、共用部分管理</td></tr>"
            "</tbody></table>"
        ),
    },
    "再委託の制限": {
        "term_detail_body": (
            "再委託の制限は、受託者が委託業務をどこまで第三者へ委ねられるかを調整する条項です。"
            "全部再委託の可否、委託者承諾の要否、責任帰属を分けて判定してください。"
        ),
        "exam_points": "全部再委託と一部再委託を区別;承諾要件を確認;再委託先の行為に対する責任主体を判定",
    },
    "品質確保促進法": {
        "term_detail_body": (
            "品質確保促進法は、住宅の品質情報を可視化し、瑕疵責任の実効性を高めるための法制度です。"
            "住宅性能表示制度と瑕疵担保関連規定の関係を軸に理解すると整理しやすくなります。"
        ),
    },
    "建替え等円滑化法": {
        "short_def": "建替え等円滑化法は、マンション再生を進めるための合意形成・事業実施の手続を定める法律です。",
        "comparison_table": (
            "<table class='seo-info-table'><tbody>"
            "<tr><th>論点</th><th>区分所有法</th><th>建替え等円滑化法</th></tr>"
            "<tr><th>中心場面</th><td>団体内部の決議・権利関係</td><td>再生事業の実行手続</td></tr>"
            "<tr><th>学習の軸</th><td>決議要件</td><td>事業認可・権利変換等の流れ</td></tr>"
            "</tbody></table>"
        ),
    },
    "10年瑕疵担保責任": {
        "short_def": "10年瑕疵担保責任は、新築住宅の主要構造部等に関する責任期間として頻出の数値論点です。",
        "exam_points": "責任期間10年の対象部位を確認;起算点を確認;民法一般原則との関係を区別",
    },
    "既存住宅状況調査": {
        "term_detail_body": (
            "既存住宅状況調査は、既存住宅取引において建物状態の情報を適切に提供するための調査です。"
            "調査の実施有無、説明内容、取引上の位置付けを問う選択肢に注意してください。"
        ),
    },
    "宅地建物取引業法": {
        "short_def": "宅地建物取引業法は、宅建業者の業務規制と消費者保護を目的とする取引規制法です。",
        "comparison_table": (
            "<table class='seo-info-table'><tbody>"
            "<tr><th>段階</th><th>主要義務</th><th>典型論点</th></tr>"
            "<tr><th>契約前</th><td>重要事項説明（35条）</td><td>説明事項・説明者・時期</td></tr>"
            "<tr><th>契約成立時</th><td>37条書面交付</td><td>契約内容の書面化</td></tr>"
            "</tbody></table>"
        ),
    },
    "重要事項説明": {
        "term_detail_body": (
            "重要事項説明は、契約締結前に買主・借主へ取引条件や法的制限を理解させるための手続です。"
            "説明のタイミング、説明者の要件、書面記載事項を一体で判断します。"
        ),
    },
    "35条書面": {
        "exam_points": "契約前交付かを確認;説明事項の網羅性を確認;宅地建物取引士の関与を確認",
        "comparison_table": (
            "<table class='seo-info-table'><tbody>"
            "<tr><th>書面</th><th>交付時期</th><th>主目的</th></tr>"
            "<tr><th>35条書面</th><td>契約締結前</td><td>重要事項の説明</td></tr>"
            "<tr><th>37条書面</th><td>契約成立後</td><td>契約内容の明確化</td></tr>"
            "</tbody></table>"
        ),
    },
    "37条書面": {
        "exam_points": "契約成立後交付かを確認;契約条項の記載漏れを判定;35条書面との差を説明",
    },
    "クーリングオフ": {
        "term_detail_body": (
            "クーリングオフは、一定取引で申込者を保護するために無条件解除を認める制度です。"
            "適用要件・起算日・除外事由の3点を先に確認すると誤答が減ります。"
        ),
    },
    "媒介契約": {
        "term_detail_body": (
            "媒介契約は、宅建業者が当事者間の契約成立を媒介するための契約です。"
            "契約類型の違い、報酬請求の根拠、書面交付義務の有無を区別して押さえてください。"
        ),
    },
}


def _flatten_entry(entry: dict) -> dict[str, str]:
    out: dict[str, str] = {
        k: v for k, v in entry.items() if k not in ("faqs", "examples") and isinstance(v, str)
    }
    faqs = entry.get("faqs") or []
    if len(faqs) >= 1:
        out["faq_1_question"] = faqs[0]["question"]
        out["faq_1_answer"] = faqs[0]["answer"]
    if len(faqs) >= 2:
        out["faq_2_question"] = faqs[1]["question"]
        out["faq_2_answer"] = faqs[1]["answer"]
    examples = entry.get("examples") or []
    if len(examples) >= 1:
        out["example_question"] = examples[0]["question"]
        out["example_answer"] = examples[0]["answer"]
    return out


KNOWLEDGE: dict[str, dict[str, str]] = {}
for _term, _category in TERM_CATEGORY_PAIRS:
    _entry = _build_default_entry(_term, _category)
    if _term in SPECIAL_OVERRIDES:
        _entry.update(SPECIAL_OVERRIDES[_term])
    KNOWLEDGE[_term] = _flatten_entry(_entry)


TERMS_BY_CATEGORY = defaultdict(list)
for _term, _category in TERM_CATEGORY_PAIRS:
    TERMS_BY_CATEGORY[_category].append(_term)
TERMS_BY_CATEGORY = dict(TERMS_BY_CATEGORY)


__all__ = [
    "KNOWLEDGE",
    "TARGET_CATEGORIES",
    "TERM_CATEGORY_PAIRS",
    "TERMS_BY_CATEGORY",
]
