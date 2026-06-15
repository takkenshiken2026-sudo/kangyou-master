#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write affiliate mock-exam + beginner-set briefs + CSV rows for kangyou-master."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML が必要です") from exc

ROOT = Path(__file__).resolve().parents[1]
BRIEFS = ROOT / "data" / "affiliate-briefs"
CSV_PATH = ROOT / "data" / "guide_articles.csv"
TAG = "ue083093-22"
OFFICIAL = "管理業務主任者試験センター（公式）"


def amazon(asin: str) -> str:
    return f"https://www.amazon.co.jp/dp/{asin}/ref=nosim?tag={TAG}"


def img(asin: str) -> str:
    return f"kangyou-book-{asin.lower()}.webp"


def book(
    rank: int,
    name: str,
    publisher: str,
    asin: str,
    *,
    edition: str = "2026年度版",
    price_yen: int = 0,
    pages: int = 0,
    for_who: str = "",
    highlights: list[str],
) -> dict:
    return {
        "rank": rank,
        "offer_type": "book",
        "name": name,
        "publisher": publisher,
        "edition": edition,
        "price_yen": price_yen,
        "price_note": "Amazon税込参考・送料別",
        "pages": pages,
        "format": "B5判",
        "asin": asin,
        "image_file": img(asin),
        "amazon_url": amazon(asin),
        "for_who": for_who,
        "highlights": highlights,
    }


def set_book(
    rank: int,
    name: str,
    publisher: str,
    asin: str,
    *,
    workbook_name: str,
    workbook_asin: str,
    price_yen: int,
    price_label: str,
    price_note: str,
    pages: int = 0,
    for_who: str = "",
    highlights: list[str],
) -> dict:
    return {
        "rank": rank,
        "offer_type": "book",
        "name": name,
        "publisher": publisher,
        "edition": "2026年度版",
        "price_yen": price_yen,
        "price_label": price_label,
        "price_note": price_note,
        "pages": pages,
        "format": "B5判×2冊",
        "asin": asin,
        "image_file": img(asin),
        "amazon_url": amazon(asin),
        "workbook_name": workbook_name,
        "workbook_amazon_url": amazon(workbook_asin),
        "for_who": for_who,
        "highlights": highlights,
    }


BRIEFS_DATA = {
    "affiliate-mock-exam-materials": {
        "slug": "affiliate-mock-exam-materials",
        "theme_key": "mock-exam-materials",
        "search_intent": "管理業務主任者試験の一問一答·速習教材を比較して選びたい",
        "title": "管理業務主任者の一問一答·速習3選【セレクト1000·2026】",
        "layout": "product-comparison",
        "asp_primary": "amazon",
        "comparison_kind": "books",
        "comparison_title": "一問一答·速習3選（比較）",
        "price_disclaimer": (
            "価格は執筆時点（2026-06-15）のAmazon税込参考です。"
            "試験形式は要項で必ず確認してください。"
        ),
        "products": [
            book(
                1,
                "2026年度版 管理業務主任者 一問一答セレクト1000",
                "TAC出版",
                "4300120293",
                price_yen=2200,
                pages=516,
                for_who="通勤·隙間時間で短問演習量を確保したい人",
                highlights=[
                    "管業専用セレクト1000問で演習効率を上げやすい",
                    "基本テキスト·項目別過去8年との併用向き",
                    "直前期の穴埋め演習にも使える",
                ],
            ),
            book(
                2,
                "2026年版 出る順管理業務主任者 速習テキスト",
                "LEC",
                "4844974314",
                edition="2026年版",
                price_yen=4400,
                for_who="要点整理から演習比重を上げたい人",
                highlights=[
                    "頻出論点をコンパクトに整理",
                    "分野別過去問題集との縦串が明確",
                    "社会人の週次計画に組み込みやすい",
                ],
            ),
            book(
                3,
                "2026年度版 管理業務主任者 項目別過去8年問題集",
                "TAC出版",
                "4300120285",
                price_yen=2860,
                for_who="50問120分通し前の分野別·年度別 drill に使いたい人",
                highlights=[
                    "過去8年を項目別に整理し弱点を切り出しやすい",
                    "セレクト1000の誤答分野へ戻る演習量を確保",
                    "10月以降の通し模試の本丸候補",
                ],
            ),
        ],
        "related_links": [
            "past-question-strategy:過去問の使い方",
            "timed-practice:時間計測演習",
            "pass-score:合格基準",
            "affiliate-textbooks-recommend:おすすめテキスト",
            "affiliate-problem-books:おすすめ問題集",
            "study-plan-beginner:初学者向け学習計画",
        ],
        "operator_note": "Amazon tag=ue083093-22。4300120293 / 4844974314 / 4300120285。2026-06-15価格確認。",
    },
    "affiliate-beginner-material-set": {
        "slug": "affiliate-beginner-material-set",
        "theme_key": "beginner-material-set",
        "search_intent": "管理業務主任者初学者が最初に揃えるテキスト+問題集セットを比較したい",
        "title": "管理業務主任者試験の初学者向け教材セット3選【2026年度版·テキスト+問題集】",
        "genre": "学習計画",
        "layout": "product-comparison",
        "asp_primary": "amazon",
        "comparison_kind": "books",
        "comparison_title": "初学者向け教材セット3選（比較）",
        "price_disclaimer": (
            "価格·在庫は執筆時点（2026-06-15）のAmazon税込参考です。"
            "購入前に必ず販売ページで最新版を確認してください。"
        ),
        "products": [
            set_book(
                1,
                "TAC2冊セット（基本テキスト+項目別過去8年）",
                "TAC出版",
                "4300120277",
                workbook_name="2026年度版 管理業務主任者 項目別過去8年問題集",
                workbook_asin="4300120285",
                price_yen=6050,
                price_label="約6,050円（2冊合計·税込参考）",
                price_note="テキスト3,190円+問題集2,860円·送料別",
                pages=860,
                for_who="管業初受験でTAC系列の縦串を揃えたい人",
                highlights=[
                    "基本テキストと過去8年の章·項目対応が取りやすい",
                    "3セットの中で合計予算を抑えやすい",
                    "5出題分野を丁寧に1周する初学者向け",
                ],
            ),
            set_book(
                2,
                "Wマスター2冊セット（テキスト+過去問集）",
                "Wマスター",
                "484715343X",
                workbook_name="2026年度版 Wマスター過去問集",
                workbook_asin="4847153448",
                price_yen=8030,
                price_label="約8,030円（2冊合計·税込参考）",
                price_note="テキスト3,630円+過去問4,400円·送料別",
                for_who="マン管併用·解説厚めの2冊を縦串で揃えたい人",
                highlights=[
                    "Wマスターテキストと過去問の章立て相性がよい",
                    "マン管合格者の45問演習にも使い分けやすい",
                    "適正化法·委託契約の横断整理に向く",
                ],
            ),
            set_book(
                3,
                "LEC出る順2冊セット（速習テキスト+分野別過去問）",
                "LEC",
                "4844974314",
                workbook_name="2026年版 出る順管理業務主任者 分野別過去問題集",
                workbook_asin="4844974321",
                price_yen=7150,
                price_label="約7,150円（2冊合計·税込参考）",
                price_note="テキスト4,400円+過去問2,750円·送料別",
                for_who="論点整理から分野別演習へ進みたい人",
                highlights=[
                    "出る順テキストと分野別過去問の縦串が明確",
                    "週15問の分野別 drill と相性がよい",
                    "TAC·Wマスターとの比較選択肢",
                ],
            ),
        ],
        "related_links": [
            "study-plan:学習計画",
            "study-plan-beginner:初学者向け学習計画",
            "affiliate-textbooks-recommend:おすすめテキスト",
            "affiliate-problem-books:おすすめ問題集",
            "textbook-selection:テキストの選び方",
            "pass-score:合格基準",
        ],
        "operator_note": "Amazon tag=ue083093-22。6 ASIN URL確定。合計 6,050 / 8,030 / 7,150円（税込参考）。",
    },
}


CSV_ROWS = {
    "affiliate-mock-exam-materials": {
        "title": "管理業務主任者の一問一答·速習3選【セレクト1000·2026】",
        "meta_description": (
            "管理業務主任者の一問一答·速習3選。"
            "TACセレクト1000·LEC出る順速習·項目別過去8年を比較。"
            "50問120分との役割分担と演習順を解説。"
        ),
        "lead": (
            "管理業務主任者試験では、テキスト·問題集に加えて一問一答や速習で短問演習量を確保する受験生が多いです。"
            "本番は50問·120分·5出題分野、令和8年度試験日2026年12月6日（日）13:00、受験手数料8,900円（要項で再確認）です。"
            "本記事では2026年度版の補助教材3冊を比較します。価格は購入前にAmazonで必ずご確認ください。"
        ),
        "priority": "360",
        "original_note": f"Amazon tag={TAG}。4300120293 / 4844974314 / 4300120285。",
        "user_intent": "管業の一問一答·速習を比較し、テキスト·問題集との組み合わせを決めたい。",
        "action_items": (
            "速習·一問一答はメインテキストの代わりにしない;"
            "3冊の用途差を比較表で確認する;"
            "短問10問→3日後解き直しを1週間試す;"
            "10月以降は50問120分通しを月1回入れる;"
            "affiliate-problem-booksで本丸の問題集1冊を先に決める"
        ),
        "revision_note": "2026-06-15: Amazon比較記事として全面リライト·published",
        "sections": [
            (
                "一問一答·速習の位置づけ",
                "速習本·一問一答は、本試験対策のメイン教材の代わりにはなりません。"
                "全体像把握→テキスト1冊→問題集→一問一答で穴埋め、という流れの「理解確認·短問演習」に使います。"
                f"試験形式·問題数は{OFFICIAL}の要項で確認してください。"
                "たとえば8月末テキスト第1周完了後にセレクト1000を追加し、"
                "10月から項目別過去8年で50問通しへ移行する計画が定番です。",
            ),
            (
                "3冊の選び方（タイプ別）",
                "通勤·隙間の短問演習なら「管理業務主任者 一問一答セレクト1000」、"
                "要点整理から演習比重を上げるなら「出る順速習テキスト」、"
                "50問120分通し前の分野別 drill なら「項目別過去8年問題集」が向きます。"
                "いずれも2026年度版表記を表紙で確認し、テキスト·問題集と同出版社系列で揃えると復習効率が上がります。"
                "迷った場合は、すでに使っているテキストの出版社に合わせて1冊に絞るのが失敗しにくい選び方です。",
            ),
            (
                "1位：管業セレクト1000の特徴",
                "2026年度版 管理業務主任者 一問一答セレクト1000（TAC出版·2,200円税込参考·516ページ·B5判）は、"
                "管業専用の短問演習量を確保したい人向けです。"
                "基本テキスト·項目別過去8年との併用で、弱点分野の穴埋めにも使えます。"
                "1回5問·15分以内に区切り、誤答語を用語解説で即確認するループが定着しやすい構成です。\n\n"
                "向いている人：通勤15分×週5回で短問を回したい社会人。",
            ),
            (
                "2位：LEC出る順速習の特徴",
                "2026年版 出る順管理業務主任者 速習テキスト（LEC·約4,400円税込参考·B5判）は、"
                "頻出論点をコンパクトに整理し、分野別過去問題集へつなげやすい速習型です。"
                "残り期間が短い場合はstudy-plan-3months記事と併用し、弱点2分野に時間を寄せてください。"
                "テキスト本冊の予習·復習の橋渡しとして使うと、演習比率を上げるタイミングが見えやすくなります。\n\n"
                "向いている人：テキスト読了前後に論点整理の橋渡しが欲しい人。",
            ),
            (
                "3位：TAC項目別過去8年の特徴",
                "2026年度版 管理業務主任者 項目別過去8年問題集（TAC出版·2,860円税込参考·B5判）は、"
                "セレクト1000の誤答分野を年度別·項目別に戻る演習の本丸候補です。"
                "10月以降の50問120分通し（月1〜2回）のメイン演習としても使いやすい1冊です。"
                "おすすめ問題集の記事でも紹介している同ASINですが、本記事では短問後の通し drill として位置づけます。\n\n"
                "向いている人：分野別正答率40％未満の章を厚く drill したい人。",
            ),
            (
                "演習順の具体例（6月開始·25週）",
                "例：6〜8月は基本テキスト中心→9月セレクト1000を週10問→10月から項目別過去8年で週30問→"
                "11月50問通し月2回。正答率より解き直し比率を重視し、"
                "間違えた語は用語解説で即確認する習慣をつけてください。"
                "時間計測はtimed-practice記事、配分はtime-limit-strategy記事で先に整理すると計画がぶれにくくなります。",
            ),
            (
                "購入前チェックリスト",
                "購入前に以下を確認してください。\n"
                "・2026年度版（最新版）か\n"
                "・管理業務主任者試験専用か\n"
                "・速習·一問一答をメイン教材にしない計画か\n"
                "・Amazon在庫·価格（執筆時点と異なる場合あり）\n"
                "・テキスト·問題集と章対応が取れる組み合わせか\n"
                "・購入直前にAmazon販売ページで版表記·在庫状況を再確認してください。"
                "初学者はstudy-plan-beginnerで週次時間を先に決めてから購入すると、使い切れずに終わるリスクが減ります。",
            ),
        ],
        "faqs": [
            (
                "一問一答だけで合格できますか？",
                "短問演習量は確保できますが、事例·条文理解はテキストと問題集が必要です。"
                "一問一答は穴埋め·確認用として、テキスト1冊と問題集1冊とセットで使ってください。"
                "通し50問で35問以上を安定して超えられるまで、弱点分野の章戻りを続けてください。",
            ),
            (
                "速習と一問一答、両方買いますか？",
                "必須ではありません。速習で全体像→テキスト本冊→一問一答、の順が一般的です。"
                "予算を抑えるなら、おすすめテキスト·問題集の記事で2冊を優先し、"
                "一問一答は1冊から始めてください。同時に3冊開くと復習が分散します。",
            ),
            (
                "項目別過去8年は問題集記事と重複しませんか？",
                "同じASINですが、本記事は短問演習後の通し drill 候補として位置づけを説明しています。"
                "問題集記事で1冊を決めたうえで、セレクト1000との併用順を本記事で整理してください。"
                "重複購入を避けるため、手元の問題集が項目別過去8年ならセレクト1000だけ追加する構成も有効です。",
            ),
        ],
        "related_links": (
            "past-question-strategy:過去問の使い方;"
            "timed-practice:時間計測演習;"
            "pass-score:合格基準;"
            "affiliate-textbooks-recommend:おすすめテキスト;"
            "affiliate-problem-books:おすすめ問題集;"
            "study-plan-beginner:初学者向け学習計画;"
            f"{amazon('4300120293')}:管業セレクト1000（Amazon）;"
            f"{amazon('4844974314')}:LEC出る順速習（Amazon）;"
            f"{amazon('4300120285')}:TAC項目別過去8年（Amazon）"
        ),
        "key_points": (
            "2026年度版 管理業務主任者 一問一答セレクト1000;"
            "2026年版 出る順管理業務主任者 速習テキスト;"
            "2026年度版 管理業務主任者 項目別過去8年問題集;"
            "一問一答·速習の位置づけ;"
            "演習順の具体例"
        ),
    },
    "affiliate-beginner-material-set": {
        "title": "管理業務主任者試験の初学者向け教材セット3選【2026年度版·テキスト+問題集】",
        "meta_description": (
            "管理業務主任者試験の初学者向け教材セット3選。"
            "TAC基本+過去8年·Wマスター2冊·LEC出る順2冊を比較。"
            "テキスト1冊+問題集1冊の購入順と週次配分を解説。"
        ),
        "lead": (
            "管理業務主任者試験の初学者教材は、テキスト1冊+問題集1冊+当サイト無料演習の3点が扱いやすい基本形です。"
            "令和8年度は12月6日（日）13:00〜15:00·5出題分野·50問120分·受験手数料8,900円です。"
            "本記事はTAC·Wマスター·LECの3セットを、合計予算·章立てのつながりで比較します。"
            "価格は執筆時点（2026-06-15）のAmazon税込参考です。3冊同時購入は避け、順に揃えてください。"
        ),
        "priority": "355",
        "original_note": f"Amazon tag={TAG}。TAC/W/LEC 6 ASIN。合計 6,050 / 8,030 / 7,150円（税込参考）。",
        "user_intent": "管業初学者が最初に揃える最小2冊セットを比較して決めたい。",
        "action_items": (
            "要項で試験日·5出題分野·8,900円を1行メモする;"
            "3セットの予算と章立てを比較表で確認する;"
            "7月にテキスト1冊を決め8月に問題集1冊を追加する;"
            "週8〜10時間をテキスト4h+演習4hに固定する;"
            "study-plan-beginnerで月次計画をカレンダー固定する"
        ),
        "revision_note": "2026-06-15: 初学者セット比較として全面リライト·published",
        "sections": [
            (
                "初学者の最小構成",
                "初学者は「要項確認→テキスト1冊→問題集1冊→無料演習→50問通し」の順で段階投入します。"
                f"受験資格·試験日·5出題分野は{OFFICIAL}の要項PDFで先に1枚にまとめ、"
                "学習カレンダーと申込手続きカレンダーは分離してください。"
                "3セットを同時購入せず、テキスト到着後2週間で使い心地を確認してから問題集を追加するのが定番です。"
                "当サイトの分野別演習10問で現在地を記録してから購入すると、セット選びの失敗が減ります。",
            ),
            (
                "3セット比較の見方",
                "予算最優先ならTAC2冊セット（約6,050円）、"
                "マン管併用で解説厚めならWマスター2冊（約8,030円）、"
                "論点整理型ならLEC出る順2冊（約7,150円）が目安です。"
                "いずれも2026年度版表記を購入前に確認し、中古は版·書き込み·付属解答の有無を販売ページで確認してください。"
                "比較表で章立てと5出題分野の対応を見たうえで、週8〜10時間の計画に合うセットを1つに絞ってください。",
            ),
            (
                "TAC2冊セット：基本テキスト+項目別過去8年",
                "「2026年度版 管理業務主任者 基本テキスト」（3,190円税込参考）と"
                "「2026年度版 管理業務主任者 項目別過去8年問題集」（2,860円税込参考）の組み合わせです。"
                "5出題分野を860ページで丁寧に学び、演習は項目別過去8年へつなげやすいのが強みです。"
                "TAC系列で章と過去8年項目の対応が取りやすく、初学者の第1セットとして選ばれやすい構成です。\n\n"
                "向いている人：管業初受験で予算を抑えつつTAC系列の縦串を揃えたい人。",
            ),
            (
                "Wマスター2冊セット：テキスト+過去問集",
                "「2026年度版 マンション管理士·管理業務主任者 Wマスターテキスト」（3,630円税込参考）と"
                "「2026年度版 Wマスター過去問集」（4,400円税込参考）の組み合わせです。"
                "マン管合格者の45問演習やW受験設計にも使い分けやすい構成です。"
                "適正化法·委託契約の横断整理に向き、社会人独学のメイン教材候補になります。\n\n"
                "向いている人：解説厚めの2冊で5分野をじっくり1周したい人。",
            ),
            (
                "LEC出る順2冊セット：速習+分野別過去問",
                "「2026年版 出る順管理業務主任者 速習テキスト」（約4,400円税込参考）と"
                "「2026年版 出る順管理業務主任者 分野別過去問題集」（2,750円税込参考）の組み合わせです。"
                "past-questions-by-field記事の週15問と相性がよく、分野別 drill の設計がしやすいです。"
                "出る順系列で頻出論点を整理してから演習へ進みたい人向けの第3の選択肢です。\n\n"
                "向いている人：論点整理から演習へ進みたい人。",
            ),
            (
                "購入順序の具体例（6月開始）",
                "例：6/15要項30分→6/21委託契約10問→7/5（土）テキスト決定→7/19（土）問題集追加→"
                "9月から50問120分通しを月1回。テキスト到着後2週間で第1章+演習10問を試し、"
                "読みにくければ別セットへ切り替えてください。試験手数料8,900円は教材予算とは別行で管理します。"
                "申込締切（Web9/30·郵送8/28消印）は手続きカレンダーに先に登録し、学習量と混同しないでください。",
            ),
            (
                "購入前チェックリスト",
                "購入前に以下を確認してください。\n"
                "・2026年度版（最新版）か\n"
                "・管理業務主任者試験専用か\n"
                "・2冊セットの章·項目対応が取れるか\n"
                "・Amazon在庫·価格（執筆時点と異なる場合あり）\n"
                "・週8時間以上確保できるか（不足ならstudy-plan-1year記事を検討）\n"
                "・購入直前にAmazon販売ページで版表記·在庫状況を再確認してください。"
                "3冊同時購入は避け、テキスト到着後2週間の試用結果で問題集を追加する順序を守ってください。",
            ),
        ],
        "faqs": [
            (
                "初学者は何を最初に買うべきですか？",
                "要項確認のあとテキスト1冊です。"
                "たとえば6/15要項30分→6/21演習10問→7/5に本記事の3セットから1冊、"
                "7/19に問題集1冊、の順が定番です。12月6日試験から逆算し、"
                "3セット同時購入は避けて段階投入してください。",
            ),
            (
                "通信講座は最初から必要ですか？",
                "不要な場合が多いです。週8時間+当サイト無料演習で9月通し50問の35問ラインを確認し、"
                "2週続いて未達なら通信講座比較を検討する順がおすすめです。"
                "11月以前は演習量を最優先し、教材はテキスト+問題集の2冊セットから始めてください。",
            ),
            (
                "教材セットの予算目安はいくらですか？",
                "テキスト+問題集で約6,000〜8,000円（税込参考）が目安です。"
                "TACセット約6,050円、Wマスターセット約8,030円、LECセット約7,150円（2026-06-15時点）。"
                "購入直前にAmazon販売ページで最新価格を確認してください。",
            ),
        ],
        "related_links": (
            "study-plan:学習計画;"
            "study-plan-beginner:初学者向け学習計画;"
            "affiliate-textbooks-recommend:おすすめテキスト;"
            "affiliate-problem-books:おすすめ問題集;"
            "textbook-selection:テキストの選び方;"
            "pass-score:合格基準;"
            f"{amazon('4300120277')}:TAC基本テキスト（Amazon）;"
            f"{amazon('4300120285')}:TAC項目別過去8年（Amazon）;"
            f"{amazon('484715343X')}:Wマスターテキスト（Amazon）;"
            f"{amazon('4847153448')}:Wマスター過去問（Amazon）;"
            f"{amazon('4844974314')}:LEC出る順速習（Amazon）;"
            f"{amazon('4844974321')}:LEC分野別過去問（Amazon）"
        ),
        "key_points": (
            "TAC2冊セット（基本テキスト+項目別過去8年）;"
            "Wマスター2冊セット（テキスト+過去問集）;"
            "LEC出る順2冊セット（速習+分野別過去問）;"
            "購入順序の具体例;"
            "初学者の最小構成"
        ),
    },
}


def write_briefs() -> None:
    BRIEFS.mkdir(parents=True, exist_ok=True)
    for slug, data in BRIEFS_DATA.items():
        path = BRIEFS / f"{slug}.yaml"
        path.write_text(
            yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
        print(f"wrote brief → {path}")


def patch_csv() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames:
        raise SystemExit("CSV header missing")

    for row in rows:
        slug = row.get("slug", "")
        if slug not in CSV_ROWS:
            continue
        cfg = CSV_ROWS[slug]
        row["title"] = cfg["title"]
        row["meta_description"] = cfg["meta_description"]
        row["lead"] = cfg["lead"]
        row["priority"] = cfg["priority"]
        row["original_note"] = cfg["original_note"]
        row["user_intent"] = cfg["user_intent"]
        row["action_items"] = cfg["action_items"]
        row["revision_note"] = cfg["revision_note"]
        row["fact_checked_at"] = "2026-06-15"
        row["content_status"] = "published"
        row["related_links"] = cfg["related_links"]
        row["key_points"] = cfg["key_points"]
        for i, (heading, body) in enumerate(cfg["sections"], start=1):
            row[f"section_{i}_heading"] = heading
            row[f"section_{i}_body"] = body.strip()
        for i in range(len(cfg["sections"]) + 1, 8):
            row[f"section_{i}_heading"] = ""
            row[f"section_{i}_body"] = ""
        for i, (q, a) in enumerate(cfg["faqs"], start=1):
            row[f"faq_{i}_question"] = q
            row[f"faq_{i}_answer"] = a
        for i in range(len(cfg["faqs"]) + 1, 4):
            row[f"faq_{i}_question"] = ""
            row[f"faq_{i}_answer"] = ""
        print(f"patched CSV row: {slug}")

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    write_briefs()
    patch_csv()
    return 0


if __name__ == "__main__":
    sys.exit(main())
