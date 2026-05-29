#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用語解説・比較・数値・誤答ハブの一覧列（定義/概要）用テキスト生成."""

from __future__ import annotations

import re
from typing import Literal

INDEX_TEXT_MAX = 160

# 一覧に載せない定型末尾（glossary enrich）
_GENERIC_GLOSSARY_SUFFIXES = (
    "に関わる用語です。",
    "を整理する際に使われます。",
    "と関係します。",
    "を確認します。",
    "を確認するために使われます。",
    "を考える場面で出てきます。",
    "につながる経営課題として捉えます。",
    "を説明する際に使われます。",
    "を検討します。",
)

# short_def / definition 内のテンプレ句
_GENERIC_GLOSSARY_MARKERS = (
    "で頻出となる基礎用語で、",
    "管理業務主任者試験で要件・効果と誤答肢の見抜き方まで",
    "判断基準になりやすい論点で、",
    "実務運用の接続が求められる。",
    "手続・判断基準を押さえる論点です。",
)

# 記事リード・FAQ から除去するボイラープレート
_BOILERPLATE_RE = re.compile(
    "|".join(
        re.escape(p)
        for p in (
            "数値・日程・合格基準はマンション管理業協会（www.mankan.or.jp）の試験要項で必ずご確認ください。",
            "数値・日程・合格基準はマンション管理業協会（www.mankan.or.jp）の試験要項で必ずご確認ください",
            "管業試験では用語集と条文の対応づけが得点の鍵になります。",
            "賃管試験では用語集と条文の対応づけが得点の鍵になります。",
            "過去問で正誤の型を分類し、試験要項で数値・期限を照合してください。",
            "最新の試験要項もあわせて確認してください。",
            "用語集→本ページ→過去問の順で往復し、正誤理由をメモに残してください。",
        )
    )
)

# summary 列のテンプレ（hub diversify 等）
_GENERIC_HUB_SUMMARY_RES = (
    re.compile(r"を整理します。?$"),
    re.compile(r"の5軸で違いを比較します。?$"),
    re.compile(r"4型に分けて整理します。?$"),
    re.compile(r"表に整理します。?$"),
    re.compile(r"同一視する典型誤り。?$"),
    re.compile(r"典型パターンを整理します。?$"),
    re.compile(r"典型誤りを整理します。?$"),
)

_GENERIC_LEAD_MARKERS = (
    "数値だけでなく義務主体・実施条件・記録保存まで一体で確認してください",
    "管理組合・総会・管業の権限を表で整理してください",
    "正しい整理を表にまとめてください",
    "関連制度との違いを横断マップにまとめ",
    "直前総仕上げに使ってください",
    "同一視する典型誤り",
    "典型パターンを整理します",
    "用語の定義と義務主体を先に固定し",
)

_PLACEHOLDER_VALUES = frozenset(
    {
        "数値は試験要項・省令で確認",
        "数値は試験要項・省令で確認。",
        "試験要項参照",
        "要項参照",
        "要項確認",
        "規約・法で定める",
    }
)

HubKind = Literal["compare", "numbers", "mistakes"]


def split_semicolon(s: str) -> list[str]:
    return [p.strip() for p in re.split(r"[;；]", s or "") if p.strip()]


def _clip(text: str, *, limit: int = INDEX_TEXT_MAX) -> str:
    t = re.sub(r"\s+", " ", (text or "").strip())
    if not t:
        return ""
    if len(t) <= limit:
        return t if t.endswith(("。", "！", "？")) else f"{t}。"
    cut = t[:limit]
    for sep in ("。", "、", " "):
        pos = cut.rfind(sep)
        if pos >= limit // 2:
            cut = cut[: pos + (1 if sep == "。" else 0)]
            break
    cut = cut.rstrip("、 ")
    return cut if cut.endswith(("。", "！", "？")) else f"{cut}。"


def _strip_boilerplate(text: str) -> str:
    t = (text or "").strip()
    if not t:
        return ""
    prev = None
    while prev != t:
        prev = t
        t = _BOILERPLATE_RE.sub("", t).strip()
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" 　。")


def _sentences(text: str) -> list[str]:
    parts = [p.strip() for p in re.split(r"(?<=[。！？])", text or "") if p.strip()]
    return parts


def _first_substantive_sentences(text: str, *, max_chars: int = INDEX_TEXT_MAX) -> str:
    cleaned = _strip_boilerplate(text)
    if not cleaned:
        return ""
    buf: list[str] = []
    total = 0
    for sent in _sentences(cleaned):
        if _is_generic_lead(sent):
            continue
        buf.append(sent)
        total += len(sent)
        if total >= max_chars * 0.6:
            break
    if not buf:
        first = _sentences(cleaned)
        buf = first[:1] if first else []
    return _clip("".join(buf), limit=max_chars)


def _is_generic_glossary_suffix(text: str, term: str) -> bool:
    t = (text or "").strip()
    if not t or not term or not t.startswith(term):
        return False
    return any(t.endswith(suffix) for suffix in _GENERIC_GLOSSARY_SUFFIXES)


def _is_generic_glossary_text(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return True
    if any(m in t for m in _GENERIC_GLOSSARY_MARKERS):
        return True
    if _is_generic_glossary_suffix(t, t.split("は")[0] if "は" in t[:20] else ""):
        return True
    return False


def _is_generic_hub_summary(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return True
    if any(rx.search(t) for rx in _GENERIC_HUB_SUMMARY_RES):
        return True
    if "同一視する典型誤り" in t:
        return True
    if re.search(r"（[^）]+）で.+を同一視する典型誤り", t):
        return True
    if len(t) < 45 and ("整理" in t or "比較" in t):
        return True
    return False


def _is_generic_lead(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return True
    if any(m in t for m in _GENERIC_LEAD_MARKERS):
        return True
    if _is_generic_hub_summary(t):
        return True
    return False


def _is_placeholder_value(value: str) -> bool:
    v = (value or "").strip().rstrip("。")
    return not v or v in _PLACEHOLDER_VALUES or "試験要項" in v and len(v) < 25


def _exam_points_overview(title: str, exam_points: str) -> str:
    pts = split_semicolon(exam_points)
    if not pts:
        return ""
    if len(pts) >= 2:
        return _clip(f"「{title}」では{pts[0]}に加え、{pts[1]}も試験で問われます。")
    return _clip(f"「{title}」の要点は{pts[0]}。")


def _definition_clause(entry: dict) -> str:
    term = (entry.get("term") or "").strip()
    definition = (entry.get("definition") or "").strip()
    short = (entry.get("short_def") or "").strip()
    if not definition:
        return ""

    m = re.search(r"まず「([^」]+)」", definition)
    if m:
        clause = m.group(1).strip()
        if clause and not _is_generic_glossary_suffix(clause, term) and not _is_generic_glossary_text(clause):
            if clause.startswith(term):
                return clause if clause.endswith("。") else f"{clause}。"
            body = clause.rstrip("。")
            return f"{term}は、{body}。" if body else ""

    m2 = re.search(rf"{re.escape(term)}とは、(.+?)。", definition)
    if m2:
        body = m2.group(1).strip()
        if body and not _is_generic_glossary_text(body):
            return f"{term}とは、{body}。"

    for part in _sentences(definition):
        if part != short and not _is_generic_glossary_suffix(part, term) and not _is_generic_glossary_text(part):
            return _clip(part)
    return ""


def terms_index_snippet(entry: dict) -> str:
    """用語一覧の「定義」列。詳細本文・リードから固有の要約を優先する。"""
    term = (entry.get("term") or "").strip()
    short = (entry.get("short_def") or "").strip()
    candidates: list[str] = []

    body = (entry.get("term_detail_body") or "").strip()
    if body:
        first_para = body.split("\n\n")[0].strip()
        sent = _first_substantive_sentences(first_para)
        if sent and not _is_generic_glossary_text(sent):
            candidates.append(sent)

    lead = _first_substantive_sentences(entry.get("article_lead") or "")
    if lead and not _is_generic_glossary_text(lead):
        candidates.append(lead)

    def_clause = _definition_clause(entry)
    if def_clause:
        candidates.append(def_clause)

    pts = split_semicolon(entry.get("exam_points") or "")
    if pts:
        overview = _exam_points_overview(term, entry.get("exam_points") or "")
        if overview:
            candidates.append(overview)

    for cand in candidates:
        c = _clip(cand)
        if c and not _is_generic_glossary_text(c):
            return c

    if short and not _is_generic_glossary_text(short):
        return _clip(short)
    return _clip(short or term)


def _compare_rows_overview(entry: dict) -> str:
    labels = entry.get("col_labels") or []
    rows = entry.get("compare_rows") or []
    if len(labels) < 2 or not rows:
        return ""
    l1, l2 = labels[0], labels[1]
    chunks: list[str] = []
    for row in rows[:2]:
        axis = (row.get("axis") or "").strip()
        cols = row.get("cols") or []
        if not axis or len(cols) < 2:
            continue
        c0, c1 = cols[0], cols[1]
        if len(c0) > 36 or len(c1) > 36:
            c0, c1 = c0[:34] + "…", c1[:34] + "…"
        chunks.append(f"{axis}では{l1}が「{c0}」、{l2}が「{c1}」")
    if chunks:
        return _clip("。".join(chunks) + "。")
    return _clip(f"{l1}と{l2}の目的・主体・手続の違いを比較表で解説した記事です。")


def _numbers_rows_overview(entry: dict) -> str:
    rows = entry.get("detail_rows") or []
    highlight = (entry.get("highlight") or "").strip()
    if highlight and not _is_generic_lead(highlight) and "確認テーマ" not in highlight:
        parts = [p for p in re.split(r"[／/]", highlight) if p.strip()]
        if parts and len(parts[0]) <= 40:
            return _clip(f"{parts[0]}の代表数値と条件を早見表でまとめた記事です。")

    items: list[str] = []
    for row in rows[:3]:
        item = (row.get("item") or "").strip()
        value = (row.get("value") or "").strip()
        if not item or not value or _is_placeholder_value(value):
            continue
        if "確認テーマ" in item:
            continue
        note = (row.get("note") or "").strip()
        if note and len(note) <= 20:
            items.append(f"{item}は{value}（{note}）")
        else:
            items.append(f"{item}は{value}")
    if items:
        return _clip("。".join(items[:2]) + "。")
    return ""


def _mistake_title_angle(title: str) -> str:
    m = re.search(r"（([^）]+)）\s*$", title or "")
    return m.group(1).strip() if m else ""


def _mistake_topic_short(title: str) -> str:
    t = re.sub(r"（[^）]+）\s*$", "", title or "").strip()
    if "：" in t:
        return t.split("：", 1)[0].strip()
    return t


def _is_generic_confusion_point(cp: str) -> bool:
    cp = (cp or "").strip().rstrip("。")
    if not cp or len(cp) < 10:
        return True
    return cp.endswith("の混同") and len(cp) <= 30


def _mistakes_rows_overview(entry: dict) -> str:
    title = (entry.get("title") or "").strip()
    angle = _mistake_title_angle(title)
    topic = _mistake_topic_short(title)
    rows = entry.get("detail_rows") or []

    lines: list[str] = []
    for row in rows[:2]:
        axis = (row.get("topic") or "").strip()
        wrong = (row.get("wrong") or "").strip()
        correct = (row.get("correct") or "").strip()
        if axis and wrong and correct and wrong != correct:
            lines.append(f"{axis}は「{wrong}」と誤りやすく、正しくは「{correct}」")

    if lines:
        body = "。".join(lines) + "。"
        if angle and topic:
            return _clip(f"（{angle}）{topic}では{body}")
        if topic:
            return _clip(f"{topic}では{body}")
        return _clip(body)

    cp = (entry.get("confusion_point") or "").strip()
    if cp and not _is_generic_confusion_point(cp):
        return _clip(cp)

    tip = (entry.get("memory_tip") or "").strip()
    if tip and not _is_generic_lead(tip):
        return _clip(tip)
    return ""


def hub_index_overview(entry: dict, kind: HubKind) -> str:
    """比較・数値・誤答一覧の「概要」列。"""
    title = (entry.get("title") or "").strip()
    candidates: list[str] = []

    if kind == "compare":
        row_text = _compare_rows_overview(entry)
        if row_text:
            candidates.append(row_text)
    elif kind == "numbers":
        row_text = _numbers_rows_overview(entry)
        if row_text:
            candidates.append(row_text)
    elif kind == "mistakes":
        row_text = _mistakes_rows_overview(entry)
        if row_text:
            candidates.append(row_text)

    lead = _first_substantive_sentences(entry.get("article_lead") or "")
    if lead and not _is_generic_lead(lead):
        candidates.append(lead)

    exam = _exam_points_overview(title, entry.get("exam_points") or "")
    if exam:
        candidates.append(exam)

    summary = (entry.get("summary") or "").strip()
    if summary and not _is_generic_hub_summary(summary):
        candidates.append(_clip(summary))

    for cand in candidates:
        c = _clip(cand)
        if c and not _is_generic_hub_summary(c) and not _is_generic_lead(c):
            return c

    if summary:
        return _clip(summary)
    return _clip(title)
