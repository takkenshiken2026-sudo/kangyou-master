#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-shot generator for kangyou S31 hub batch files."""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
S30_DATA = TOOLS / "write_kangyou_hub_s30_data.py"


def extract_s30_content() -> str:
    src = S30_DATA.read_text(encoding="utf-8")
    start = src.index("_OFFICIAL = ")
    end = src.index("\n\n\ndef write_csv")
    body = src[start:end]
    header = '''# -*- coding: utf-8 -*-
"""管理業務主任者 知識ハブ S30 行データ."""

from __future__ import annotations

from tools.write_kangyou_hub_s30 import _faq, _rows

'''
    return header + body + "\n"


def write_s30_content() -> None:
    (TOOLS / "write_kangyou_hub_s30_content.py").write_text(extract_s30_content(), encoding="utf-8")


def write_s31_content() -> None:
    text = (TOOLS / "_kangyou_s31_body.py").read_text(encoding="utf-8")
    header = '''# -*- coding: utf-8 -*-
"""管理業務主任者 知識ハブ S31 追加分（各10件）."""

from tools.write_kangyou_hub_s30_content import _OFFICIAL, cmp, mis, num

T, K, B = "管理適正化法", "区分所有法", "判例・横断総合"

'''
    (TOOLS / "write_kangyou_hub_s31_content.py").write_text(header + text, encoding="utf-8")


def _expand_answer(q: str, a: str, points: str, official: bool) -> str:
    base = a.strip()
    if len(base) < 100:
        extra = points.split(";")[0] if points else ""
        base = f"{base} 試験では{extra}をセットで確認し、条文・管理規約の定めと照合しながら過去問を分類してください。"
    if official and "mankan.or.jp" not in base:
        base += " 数値・日程・合格基準はマンション管理業協会（www.mankan.or.jp）の試験要項で必ずご確認ください。"
    return base


def write_premium_faqs() -> None:
    sys_path = str(ROOT)
    import sys

    if sys_path not in sys.path:
        sys.path.insert(0, sys_path)
    from tools.write_kangyou_hub_s30_content import (  # noqa: WPS433
        COMPARISONS,
        MISTAKES,
        NUMBERS,
        _OFFICIAL,
    )

    lines = [
        "# -*- coding: utf-8 -*-",
        '"""管理業務主任者 知識ハブ：試験特化FAQ."""',
        "",
        "from tools.write_kangyou_hub_s30_content import _OFFICIAL",
        "",
        "PREMIUM_FAQS: dict[str, list[tuple[str, str]]] = {",
    ]
    official_slugs = {
        "goukaku-mondai", "juken-tesuryou", "shiken-jikan", "shiken-nittei-2026",
        "goukaku-ritsu", "kan-gyou-touroku", "menjo-gokai", "manshi-kan-gyou-kongou",
        "kan-gyou-manshi",
    }
    for rows in (COMPARISONS, NUMBERS, MISTAKES):
        for row in rows:
            slug = row["slug"]
            lines.append(f'    "{slug}": [')
            pts = row.get("exam_points", "")
            for n in range(1, 5):
                q = row.get(f"faq_{n}_question", "")
                a = row.get(f"faq_{n}_answer", "")
                if not q:
                    continue
                ans = _expand_answer(q, a, pts, slug in official_slugs or "試験" in slug)
                if len(ans) < 100:
                    ans += " 本ページは学習整理用です。出題・制度変更は必ず公式情報で確認してください。"
                q_esc = q.replace('"', '\\"')
                a_esc = ans.replace('"', '\\"')
                lines.append(f'        ("{q_esc}", "{a_esc}"),')
            lines.append("    ],")
    lines.append("}")
    text = "\n".join(lines)
    footer = '''


def apply_premium_faqs(row: dict[str, str]) -> dict[str, str]:
    slug = row.get("slug", "")
    if slug not in PREMIUM_FAQS:
        return row
    row = dict(row)
    for i, (q, a) in enumerate(PREMIUM_FAQS[slug], start=1):
        row[f"faq_{i}_question"] = q
        row[f"faq_{i}_answer"] = a
    return row


def apply_all(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [apply_premium_faqs(r) for r in rows]
'''
    (TOOLS / "write_kangyou_hub_premium_faqs.py").write_text(text + footer, encoding="utf-8")


def write_hub_data() -> None:
    content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""管理業務主任者 知識ハブ CSV 統合出力（S30 + S31 …）."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.hub_merge_data import merge  # noqa: E402
from tools.write_kangyou_hub_s30 import DATA, HEADER_COMPARE, HEADER_MISTAKES, HEADER_NUMBERS  # noqa: E402
from tools.write_kangyou_hub_s30_content import COMPARISONS as C30, MISTAKES as M30, NUMBERS as N30  # noqa: E402
from tools.write_kangyou_hub_s31_content import COMPARISONS_ADD, MISTAKES_ADD, NUMBERS_ADD  # noqa: E402
from tools.write_kangyou_hub_premium_faqs import apply_all as apply_premium_faqs  # noqa: E402


def write_csv(path: Path, header: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, lineterminator="\\n")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    comparisons = apply_premium_faqs(merge(C30, COMPARISONS_ADD))
    numbers = apply_premium_faqs(merge(N30, NUMBERS_ADD))
    mistakes = apply_premium_faqs(merge(M30, MISTAKES_ADD))
    write_csv(DATA / "comparisons.csv", HEADER_COMPARE, comparisons)
    write_csv(DATA / "numbers.csv", HEADER_NUMBERS, numbers)
    write_csv(DATA / "mistakes.csv", HEADER_MISTAKES, mistakes)
    print(f"wrote compare={len(comparisons)} numbers={len(numbers)} mistakes={len(mistakes)}")


if __name__ == "__main__":
    main()
'''
    (TOOLS / "write_kangyou_hub_data.py").write_text(content, encoding="utf-8")


def write_s30_data_wrapper() -> None:
    content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate kangyou hub S30 rows and write all CSVs (legacy entry)."""

from tools.write_kangyou_hub_data import main

if __name__ == "__main__":
    main()
'''
    (TOOLS / "write_kangyou_hub_s30_data.py").write_text(content, encoding="utf-8")


if __name__ == "__main__":
    write_s30_content()
    write_s31_content()
    write_premium_faqs()
    write_hub_data()
    write_s30_data_wrapper()
    print("kangyou S31 batch files generated")
