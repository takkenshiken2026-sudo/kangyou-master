# -*- coding: utf-8 -*-
"""用語解説 KNOWLEDGE モジュール向けの本文・比較表ヘルパー。"""

from __future__ import annotations

CATEGORY_FOCUS: dict[str, str] = {
    "区分所有法": "専有部分・共用部分・管理組合・決議要件",
    "標準管理規約": "総会・理事会・決議種類・会計・修繕",
    "建築・設備": "建築基準法・消防法・昇降機・設備の法定検査と保守",
    "会計・税務": "管理組合会計・修繕積立金会計・予算・決算・税務処理",
    "管理適正化法": "管理業務主任者・73条書面・登録制度・管理計画",
    "標準管理委託契約書・指針": "委託業務範囲・費用区分・再委託・報告義務",
    "品確法・建替円滑化法等": "住宅品質確保・建替え手続・瑕疵担保",
    "宅建業法": "35条書面・37条書面・重要事項説明・取引段階",
    "民法・借地借家法": "条文根拠・要件・効果・類似制度との区別",
    "判例・横断総合": "判例趣旨・複数分野の横断比較",
}

WEAK_COMPARISON_MARKERS = (
    "関連ページで対比",
    "<th>覚え方</th>",
)


def is_weak_comparison(html: str) -> bool:
    text = (html or "").strip()
    if not text:
        return False
    return any(m in text for m in WEAK_COMPARISON_MARKERS)


def split_related(related: str) -> list[str]:
    return [x.strip() for x in (related or "").split(";") if x.strip()]


def split_legal(legal: str) -> str:
    return (legal or "").replace(";", "・").strip()


def build_rich_body(
    term: str,
    category: str,
    *,
    legal_basis: str = "",
    related_terms: str = "",
    exam_hint: str = "",
) -> str:
    focus = CATEGORY_FOCUS.get(category, category)
    legal = split_legal(legal_basis) or focus
    related = split_related(related_terms)
    rel_txt = "、".join(related[:3]) if related else "関連用語"
    exam = exam_hint or f"{term}の定義・要件・効果を{legal}と照合して説明できる"

    p1 = (
        f"{term}は{category}分野で頻出の論点です。"
        f"{focus}を理解するうえで、{legal}を根拠に位置づけを確認します。"
    )
    p2 = (
        f"試験では「{exam}」が得点の軸になります。"
        f"選択肢は要件の一部欠落、主体の取り違え、時期・割合の誤りで構成されることが多いです。"
    )
    p3 = (
        f"{term}は{rel_txt}とセットで整理すると定着しやすくなります。"
        f"過去問・実践演習で{category}フィルタを使い、誤答した選択肢の不足要件をメモして復習してください。"
    )
    return f"{p1}\n\n{p2}\n\n{p3}"


def build_exam_points(
    term: str,
    category: str,
    *,
    legal_basis: str = "",
    exam_hint: str = "",
    related_terms: str = "",
) -> str:
    legal = split_legal(legal_basis) or category
    related = split_related(related_terms)
    rel_txt = "、".join(related[:2]) if related else "類似用語"
    exam = exam_hint or f"{term}の定義と適用場面を説明できる"
    return f"{exam};{legal}の根拠を明示できる;{rel_txt}との違いを区別できる"


def build_comparison_table(
    term: str,
    compare: str,
    *,
    term_note: str,
    compare_note: str,
) -> str:
    if not compare or compare == term:
        return ""
    return (
        '<table class="seo-info-table">'
        "<thead><tr><th>比較項目</th>"
        f"<th>{term}</th><th>{compare}</th></tr></thead>"
        "<tbody>"
        f"<tr><td>押さえ方</td><td>{term_note}</td><td>{compare_note}</td></tr>"
        "</tbody></table>"
    )


def build_entry_from_row(row: dict[str, str]) -> dict[str, str]:
    """CSV 行から最低品質の KNOWLEDGE エントリを生成する。"""
    term = (row.get("term") or "").strip()
    category = (row.get("category") or "").strip()
    legal = (row.get("legal_basis") or "").strip()
    related = row.get("related_terms") or ""
    importance = (row.get("importance") or "").strip()
    related_list = split_related(related)
    compare = related_list[0] if related_list else ""

    exam_hint = ""
    if (row.get("exam_points") or "").strip() and not (
        row.get("exam_points") or ""
    ).startswith("定義を一文で言える"):
        exam_hint = (row.get("exam_points") or "").split(";")[0].strip()

    body = build_rich_body(
        term,
        category,
        legal_basis=legal,
        related_terms=related,
        exam_hint=exam_hint,
    )
    entry: dict[str, str] = {
        "short_def": (
            row.get("short_def") or ""
        ).strip()
        or f"{term}は{category}分野の重要論点。{split_legal(legal) or focus_hint(category)}を根拠に整理します。",
        "definition": (
            row.get("definition") or ""
        ).strip()
        or f"{term}とは、{category}において試験で問われる基本概念です。定義・要件・効果を区別して理解します。",
        "term_detail_body": body,
        "exam_points": build_exam_points(
            term,
            category,
            legal_basis=legal,
            exam_hint=exam_hint,
            related_terms=related,
        ),
        "common_mistakes": (
            row.get("common_mistakes") or ""
        ).strip()
        or f"{term}を類似語と混同する;要件の一部だけ暗記して判断する;{split_legal(legal) or category}の根拠を外す",
        "memory_tip": (
            row.get("memory_tip") or ""
        ).strip()
        or f"{term}は「根拠→要件→効果→{compare or '関連語'}との違い」の順で30秒説明できる形にする。",
        "explanation": (
            row.get("explanation") or ""
        ).strip()
        or f"{term}は選択肢の言い換えと要件不足の消去が得点の近道です。",
        "article_lead": (
            row.get("article_lead") or ""
        ).strip()
        or f"{term}の意味と試験での判定ポイントを、{split_legal(legal) or category}の文脈で整理します。",
        "faq_1_question": (row.get("faq_1_question") or "").strip()
        or f"{term}はどの分野で出題されますか？",
        "faq_1_answer": (row.get("faq_1_answer") or "").strip()
        or f"主に{category}です。{split_legal(legal) or '関連法令'}とセットで確認してください。",
        "faq_2_question": (row.get("faq_2_question") or "").strip()
        or f"{term}と混同しやすい論点は？",
        "faq_2_answer": (row.get("faq_2_answer") or "").strip()
        or f"{compare or '関連用語'}との違いを比較表で整理すると定着しやすくなります。",
    }

    if compare:
        entry["comparison_table"] = build_comparison_table(
            term,
            compare,
            term_note=exam_hint or f"{term}の定義・要件を確認",
            compare_note=f"{compare}の定義・要件を確認",
        )

    if importance == "A":
        q = (row.get("example_question") or "").strip()
        a = (row.get("example_answer") or "").strip()
        entry["example_question"] = q or f"{term}に関する次の記述のうち、最も適切でないものはどれか。"
        entry["example_answer"] = a or (
            f"{exam_hint or term + 'の要件'}に照らし、条件を満たさない選択肢を選ぶ。"
        )

    return entry


def focus_hint(category: str) -> str:
    return CATEGORY_FOCUS.get(category, category)
