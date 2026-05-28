# -*- coding: utf-8 -*-
"""手作り用語解説エントリの共通ヘルパー。"""

from __future__ import annotations


def table(headers: list[str], rows: list[list[str]]) -> str:
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = []
    for row in rows:
        td = "".join(f"<td>{c}</td>" for c in row)
        trs.append(f"<tr>{td}</tr>")
    return (
        '<table class="seo-info-table"><thead>'
        f"<tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table>"
    )


def entry(
    *,
    term: str,
    category: str,
    short_def: str,
    definition: str,
    term_detail_body: str,
    exam_points: str,
    common_mistakes: str,
    memory_tip: str,
    explanation: str,
    article_lead: str,
    faq_1_question: str,
    faq_1_answer: str,
    faq_2_question: str,
    faq_2_answer: str,
    comparison_table: str = "",
    example_question: str = "",
    example_answer: str = "",
) -> dict[str, str]:
    out: dict[str, str] = {
        "short_def": short_def,
        "definition": definition,
        "term_detail_body": term_detail_body,
        "exam_points": exam_points,
        "common_mistakes": common_mistakes,
        "memory_tip": memory_tip,
        "explanation": explanation,
        "article_lead": article_lead,
        "faq_1_question": faq_1_question,
        "faq_1_answer": faq_1_answer,
        "faq_2_question": faq_2_question,
        "faq_2_answer": faq_2_answer,
    }
    if comparison_table.strip():
        out["comparison_table"] = comparison_table.strip()
    if example_question.strip():
        out["example_question"] = example_question.strip()
    if example_answer.strip():
        out["example_answer"] = example_answer.strip()
    return out
