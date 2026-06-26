#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared sitemap helpers with lastmod support."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape


@dataclass(frozen=True)
class SitemapEntry:
    loc: str
    lastmod: str | None = None
    changefreq: str = "monthly"

    def sort_key(self) -> tuple[str, str]:
        return (self.loc, self.lastmod or "")


def iso_date(value: str | None) -> str | None:
    text = (value or "").strip()
    if not text:
        return None
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        return text[:10]
    return None


def iso_from_mtime(path: Path) -> str | None:
    if not path.is_file():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()


@lru_cache(maxsize=None)
def git_lastmod_map(root: str) -> dict[str, str]:
    """{リポジトリ相対パス: 'YYYY-MM-DD'} を git 履歴から構築する。

    各ファイルの最終コミット日（author date）を返す。ファイル mtime と違い、
    fresh clone でも安定するため sitemap の lastmod 一次ソースに使う。
    全履歴が必要（CI は actions/checkout の fetch-depth: 0）。履歴が無い・
    git が無い等で失敗した場合は空 dict を返し、呼び出し側が mtime に退避する。
    """
    try:
        out = subprocess.run(
            ["git", "-C", root, "log", "--no-renames", "--name-only",
             "--pretty=format:\x01%cs"],
            capture_output=True, text=True, check=True, timeout=120,
        ).stdout
    except (subprocess.SubprocessError, OSError):
        return {}
    dates: dict[str, str] = {}
    cur = ""
    for line in out.splitlines():
        if line.startswith("\x01"):
            cur = line[1:].strip()
        elif line and cur and line not in dates:
            # git log は新しい順。最初に出た日付＝最終更新日。
            dates[line] = cur
    return dates


def lastmod_for(path: Path, root: Path) -> str | None:
    """git 最終コミット日を優先し、無ければ mtime にフォールバック。"""
    try:
        rel = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        rel = None
    if rel:
        git_date = git_lastmod_map(str(root)).get(rel)
        if git_date:
            return git_date
    return iso_from_mtime(path)


def iso_today() -> str:
    return date.today().isoformat()


def write_sitemap(entries: list[SitemapEntry], out: Path) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for entry in sorted({e.loc: e for e in entries}.values(), key=lambda e: e.loc):
        lines.append("  <url>")
        lines.append(f"    <loc>{xml_escape(entry.loc)}</loc>")
        if entry.lastmod:
            lines.append(f"    <lastmod>{xml_escape(entry.lastmod)}</lastmod>")
        lines.append(f"    <changefreq>{xml_escape(entry.changefreq)}</changefreq>")
        lines.append("  </url>")
    lines.append("</urlset>")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
