#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ビルド成果物のハッシュから site-asset-version.js と sw.js のキャッシュ名を更新する。"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HASH_TARGETS = (
    "exam-site-data-past.js",
    "exam-site-data-practice.js",
    "exam-site-data-ichimondou.js",
    "site-config.js",
    "site-theme.css",
    "site-pages.css",
    "site-analytics.js",
    "site-exam-data-loader.js",
)

OUT_JS = ROOT / "site-asset-version.js"
SW_JS = ROOT / "sw.js"


def compute_version() -> str:
    h = hashlib.sha256()
    for name in HASH_TARGETS:
        path = ROOT / name
        if path.is_file():
            h.update(path.name.encode())
            h.update(path.read_bytes())
    return h.hexdigest()[:12]


def write_site_asset_version(version: str) -> None:
    OUT_JS.write_text(
        f'window.__SITE_ASSET_VERSION__="{version}";\n',
        encoding="utf-8",
    )


def patch_sw_cache_version(version: str) -> None:
    text = SW_JS.read_text(encoding="utf-8")
    new = re.sub(
        r'var VERSION = "[^"]*";',
        f'var VERSION = "{version}";',
        text,
        count=1,
    )
    if new == text:
        if re.search(r'var VERSION = "[^"]*";', text):
            return
        raise RuntimeError("sw.js: VERSION 行が見つかりません")
    SW_JS.write_text(new, encoding="utf-8")


def main() -> int:
    version = compute_version()
    write_site_asset_version(version)
    patch_sw_cache_version(version)
    print(f"write_asset_version: {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
