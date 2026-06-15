#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write affiliate book briefs + CSV rows for kangyou-master (Amazon tag ue083093-22)."""

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


BRIEFS_DATA = {
    "affiliate-textbooks-recommend": {
        "slug": "affiliate-textbooks-recommend",
        "theme_key": "textbooks-recommend",
        "search_intent": "管理業務主任者試験の独学向けおすすめテキストを比較して選びたい",
        "title": "管理業務主任者のおすすめ参考書・テキスト3選【2026年度版・独学】",
        "layout": "product-comparison",
        "asp_primary": "amazon",
        "comparison_kind": "books",
        "comparison_title": "おすすめテキスト3選（比較）",
        "price_disclaimer": (
            "価格・在庫・版情報は執筆時点（2026-06-15）のAmazon税込参考です。"
            "購入前に必ず販売ページでご確認ください。"
        ),
        "products": [
            book(
                1,
                "2026年度版 管理業務主任者 基本テキスト",
                "TAC出版",
                "4300120277",
                price_yen=3190,
                pages=860,
                for_who="5出題分野を1冊で丁寧に学びたい初学者",
                highlights=[
                    "860ページで委託契約·会計·修繕·適正化法·その他を網羅",
                    "TACブランドで管業独学の定番として選ばれやすい",
                    "章立てが要項の5出題分野と対応づけやすい",
                ],
            ),
            book(
                2,
                "2026年版 出る順管理業務主任者 速習テキスト",
                "LEC",
                "4844974314",
                edition="2026年版",
                price_yen=4400,
                for_who="短期で要点整理から演習へ移りたい人",
                highlights=[
                    "出る順シリーズで頻出論点をコンパクトに整理",
                    "速習構成で社会人の週次計画に組み込みやすい",
                    "分野別過去問題集との併用がしやすい",
                ],
            ),
            book(
                3,
                "2026年度版 マンション管理士・管理業務主任者 Wマスターテキスト",
                "Wマスター",
                "484715343X",
                price_yen=3630,
                for_who="マン管と管業をセットで学びたい人",
                highlights=[
                    "マンション管理士試験との共通論点を1冊で整理",
                    "Wマスター過去問集との章対応が取りやすい",
                    "適正化法·管理委託の横断整理に向く",
                ],
            ),
        ],
        "related_links": [
            "textbook-selection:テキスト選び",
            "study-plan:学習計画",
            "past-question-strategy:過去問の使い方",
            "affiliate-problem-books:おすすめ問題集",
            "pass-score:合格基準",
            "textbook-vs-past-questions:テキストと過去問",
        ],
        "operator_note": (
            "Amazon tag=ue083093-22。2026-06-15 Amazon販売ページで価格確認"
            "（TAC 3,190円·LEC 約4,400円·Wマスター 3,630円税込参考）。"
        ),
    },
    "affiliate-problem-books": {
        "slug": "affiliate-problem-books",
        "theme_key": "problem-books",
        "search_intent": "管理業務主任者試験の過去問·問題集を比較して選びたい",
        "title": "管理業務主任者のおすすめ問題集3選【過去問·分野別2026】",
        "layout": "product-comparison",
        "asp_primary": "amazon",
        "comparison_kind": "books",
        "comparison_title": "おすすめ問題集3選（比較）",
        "price_disclaimer": (
            "価格・在庫は執筆時点（2026-06-15）のAmazon税込参考です。"
            "購入前に販売ページで最新版を確認してください。"
        ),
        "products": [
            book(
                1,
                "2026年度版 管理業務主任者 項目別過去8年問題集",
                "TAC出版",
                "4300120285",
                price_yen=2860,
                for_who="項目別·年度別で演習量を確保したい人",
                highlights=[
                    "過去8年分を項目別に整理し弱点分野を切り出しやすい",
                    "基本テキストと章·項目の対応が取りやすい",
                    "50問120分通し前の分野別 drill に向く",
                ],
            ),
            book(
                2,
                "2026年版 出る順管理業務主任者 分野別過去問題集",
                "LEC",
                "4844974321",
                edition="2026年版",
                price_yen=2750,
                for_who="5出題分野ごとに過去問を回したい人",
                highlights=[
                    "分野別構成でpast-questions-by-field記事の週15問と相性がよい",
                    "速習テキストとの併用が定番",
                    "頻出論点の解説付きで復習しやすい",
                ],
            ),
            book(
                3,
                "2026年度版 Wマスター過去問集",
                "Wマスター",
                "4847153448",
                price_yen=4400,
                for_who="Wマスターテキスト読了後に通し演習したい人",
                highlights=[
                    "Wマスターテキストと章対応で戻り学習がしやすい",
                    "50問本番形式の通し演習量を確保しやすい",
                    "マン管合格者の45問演習にも使い分けやすい",
                ],
            ),
        ],
        "related_links": [
            "past-question-strategy:過去問の使い方",
            "past-questions-by-field:分野別過去問",
            "study-plan:学習計画",
            "pass-score:合格基準",
            "affiliate-textbooks-recommend:おすすめテキスト",
            "textbook-vs-past-questions:テキストと過去問",
        ],
        "operator_note": "Amazon tag=ue083093-22。2026-06-15 価格確認。年度版表記を購入前に要確認。",
    },
}


CSV_ROWS = {
    "affiliate-textbooks-recommend": {
        "title": "管理業務主任者のおすすめ参考書・テキスト3選【2026年度版・独学】",
        "meta_description": (
            "管理業務主任者試験の独学向けおすすめテキスト3選。"
            "TAC基本テキスト·LEC出る順速習·Wマスターテキストを比較。"
            "50問·5出題分野の選び方と過去問との併用も解説。"
        ),
        "lead": (
            "管理業務主任者試験は50問·120分·5出題分野（委託契約·会計·維持修繕·"
            "適正化法·その他管理事務）を押さえる必要があり、最初の1冊選びで学習効率が大きく変わります。"
            "本記事では2026年度版の主要テキスト3冊を、初学者·社会人独学の視点で比較します。"
            "令和8年度試験日は2026年12月6日（日）13:00、受験手数料8,900円（要項で再確認）です。"
            "価格·版情報は購入前にAmazonの販売ページで必ずご確認ください。"
        ),
        "priority": "370",
        "original_note": "Amazon Associates tag=ue083093-22。比較: 4300120277 / 4844974314 / 484715343X。",
        "user_intent": (
            "独学で使う管理業務主任者のテキストを、解説の厚み·速習性·マン管併用で比較して1冊に絞りたい。"
        ),
        "action_items": (
            "比較表で3冊の違いを確認する;要項5出題分野と目次を照合して1冊を選ぶ;"
            "管業マスター過去問で弱点分野を把握する"
        ),
        "revision_note": "2026-06-15: テンプレ構成に合わせて本文を全面リライト·Amazon価格再確認",
        "sections": [
            (
                "テキスト選びの3つのポイント",
                "管理業務主任者試験のテキスト選びでは、①管理業務主任者試験センター（公式）の"
                "出題範囲（5出題分野·50問120分）と目次が沿っているか、"
                "②解説量が自分の前提知識に合うか、③章末演習や別冊問題集とセットで使えるかを確認します。\n\n"
                "社会人独学では、通勤で読める分量と週末にまとめて演習できる問題量も判断材料になります。"
                "たとえば6月開始·12/6本番なら、第1〜4週でテキスト1章＋分野別10問、第5週から50問通しへ移行する計画と"
                "ページ数が見合うかを見てください。1冊に絞れない場合は、テキスト1冊＋過去問専門1冊の2冊構成も有効です。",
            ),
            (
                "おすすめテキスト比較の見方",
                "比較では「5分野を厚く学ぶ」「速習で要点から入る」「マン管とセットで学ぶ」の3タイプで見ます。"
                "いずれも2026年度版表記の管業専用教材であることを表紙で確認してから選んでください。"
                "独学初期は理解用1冊に絞り、分野別正答率60％超の段階で問題集を追加する構成が扱いやすいです。"
                "管業マスターの過去問で5分野別得点を記録し、40％未満の分野が出たらテキスト該当章に戻る。"
                "解説の厚みが足りないと感じた冊を基準に選び直すと、買い替えの失敗が減ります。",
            ),
            (
                "1位：TAC基本テキストの特徴",
                "2026年度版 管理業務主任者 基本テキスト（TAC出版·3,190円税込参考·860ページ·B5判）は、"
                "5出題分野を860ページで丁寧に網羅する定番です。"
                "章立てが要項の委託契約·会計·維持修繕·適正化法·その他と対応づけやすく、"
                "初学者が最初の1冊に選びやすい構成です。"
                "テキスト選び記事（textbook-selection）の要項照合表と併用すると、週次計画も組み立てやすくなります。\n\n"
                "向いている人：管業試験が初めてで、5分野を1冊でじっくり学びたい人。",
            ),
            (
                "2位：LEC出る順速習テキストの特徴",
                "2026年版 出る順管理業務主任者 速習テキスト（LEC·約4,400円税込参考·B5判）は、"
                "頻出論点をコンパクトに整理し、短期で全体像から演習へ移りやすい速習型です。"
                "社会人の週8〜10時間計画に組み込みやすく、分野別過去問題集との併用が定番です。"
                "残り期間が短い場合は3か月学習計画記事と併用して、弱点2分野に時間を寄せてください。\n\n"
                "向いている人：ある程度不動産·管理の基礎があり、要点整理から演習比重を上げたい人。",
            ),
            (
                "3位：Wマスターテキストの特徴",
                "2026年度版 マンション管理士·管理業務主任者 Wマスターテキスト（Wマスター·3,630円税込参考·B5判）は、"
                "マンション管理士試験との共通論点を1冊で整理できる教材です。"
                "Wマスター過去問集と章対応が取りやすく、適正化法·管理委託の横断整理に向いています。"
                "マン管合格済みで管業のみ受験する場合、適正化法5問免除（45問120分）の演習計画とも相性がよいです。\n\n"
                "向いている人：マン管と管業をセットで学び、過去問集も同シリーズに揃えたい人。",
            ),
            (
                "テキストと管業マスター過去問の併用",
                "テキストで論点を押さえたら、管業マスターの過去問·一問一答で50問本番形式の演習に移ります。"
                "5分野別正答率を記録し、40％未満の分野をテキスト該当章に戻って復習するサイクルが効率的です。"
                "テキストで理解→演習で確認→間違えた論点を用語解説で補強、の順で回してください。"
                "過去問の回し方は past-question-strategy、分野別 drill は past-questions-by-field で整理できます。",
            ),
            (
                "購入前チェックリスト",
                "購入前に以下を確認してください。\n"
                "・2026年度版（最新版）か\n"
                "・管理業務主任者試験専用か（マン管のみ·宅建のみ教材と混同しない）\n"
                "・Amazon在庫·価格（執筆時点と異なる場合あり）\n"
                "・手元の学習計画（6か月／10か月）に対してページ数·演習量が見合うか\n"
                "・目次が5出題分野（委託·会計·修繕·適正化法·その他）を網羅しているか\n"
                "・中古購入の場合は版·書き込みの有無を販売ページの商品説明で確認する",
            ),
        ],
        "faqs": [
            (
                "テキストは1冊だけで足りますか？",
                "テキスト1冊＋当サイトの過去問演習で独学は可能です。"
                "演習量が足りないと感じたら、おすすめ問題集の記事で紹介している過去問専門1冊を追加する構成がおすすめです。"
                "50問通しで35問以上（正答率70％相当）を安定して超えられるまで、弱点分野の章戻りを続けてください。",
            ),
            (
                "マンション管理士向けテキストだけで管業試験は受けられますか？",
                "マン管教材は共通論点の理解に使えますが、管業の5出題分野·50問演習には管業専用テキストまたは問題集が必要です。"
                "マン管合格者は適正化法5問免除で45問120分ですが、演習記録は5分野別に取る習慣をつけてください。"
                "Wマスターの管業·マン管セット教材は、この使い分けに向いています。",
            ),
            (
                "価格·在庫はどこで確認しますか？",
                "各商品のAmazon販売ページ（本記事の比較表リンク）で、税込価格·在庫·版表記を確認してください。"
                "2026-06-15時点ではTAC 3,190円·LEC 約4,400円·Wマスター 3,630円（税込参考）でしたが、"
                "キャンペーンや品切れで変わります。購入前に目次写真または試し読みで5出題分野が揃っているかも併せて確認すると安心です。",
            ),
        ],
        "related_links": (
            "textbook-selection:テキスト選び;"
            "study-plan:学習計画;"
            "past-question-strategy:過去問の使い方;"
            "affiliate-problem-books:おすすめ問題集;"
            "pass-score:合格基準;"
            "textbook-vs-past-questions:テキストと過去問;"
            f"{amazon('4300120277')}:2026年度版 管理業務主任者 基本テキスト（Amazon）"
        ),
        "key_points": (
            "2026年度版 管理業務主任者 基本テキスト;"
            "2026年版 出る順管理業務主任者 速習テキスト;"
            "2026年度版 マンション管理士·管理業務主任者 Wマスターテキスト;"
            "テキスト選びの基準;"
            "過去問との併用"
        ),
    },
    "affiliate-problem-books": {
        "title": "管理業務主任者のおすすめ問題集3選【過去問·分野別2026】",
        "meta_description": (
            "管理業務主任者試験のおすすめ問題集3選。"
            "TAC項目別過去8年·LEC分野別過去問·Wマスター過去問集を比較。"
            "50問120分の演習量確保と分野別対策も解説。"
        ),
        "lead": (
            "管理業務主任者試験では、過去問·分野別演習の量が得点安定の鍵です。"
            "50問·120分·5出題分野、令和8年度試験日2026年12月6日（日）13:00、"
            "受験手数料8,900円（要項で再確認）が前提です。"
            "本記事では2026年度版の問題集3冊を、収録形式·解説量·独学との相性で比較します。"
            "価格は購入前にAmazonで必ずご確認ください。"
        ),
        "priority": "365",
        "original_note": "Amazon tag=ue083093-22。4300120285 / 4844974321 / 4847153448。",
        "user_intent": (
            "管理業務主任者の過去問·分野別問題集を比較し、演習のメイン1冊を決めたい。"
        ),
        "action_items": (
            "3冊の収録形式を比較する;演習計画に組み込む1冊を選ぶ;"
            "5分野別正答率40％未満の弱点を過去問で確認する"
        ),
        "revision_note": "2026-06-15: Amazon価格を販売ページで再確認して更新",
        "sections": [
            (
                "問題集選びの基準",
                "問題集選びでは、(1)50問120分本番形式に近いか (2)解説で復習できるか "
                "(3)演習量が計画に見合うかを確認します。"
                "5分野別対策には、分野別に解ける問題集か、解説で弱点分野に戻れるかが重要です。"
                "たとえばテキスト第1周完了後（目安8〜10週）に、週1回50問通しをカレンダーに登録し、"
                "問題集1冊をメイン演習に据える計画が定番です。"
                "合格基準（pass-score）の演習目標35問以上も毎回記録してください。",
            ),
            (
                "3冊の選び方（タイプ別）",
                "[[affiliate-hub-placeholder]]\n\n"
                "項目別·年度別で演習量を確保したい人は2026年度版 管理業務主任者 項目別過去8年問題集、"
                "5出題分野ごとに回したい人は2026年版 出る順管理業務主任者 分野別過去問題集、"
                "Wマスターテキスト読了後に通し演習したい人は2026年度版 Wマスター過去問集が向きます。"
                "いずれも管業専用（50問·5出題分野）であることを表紙で確認してから選んでください。"
                "比較表の価格は執筆時点の参考です。",
            ),
            (
                "1位：TAC項目別過去8年問題集",
                "2026年度版 管理業務主任者 項目別過去8年問題集（TAC出版·約2,860円税込参考）は、"
                "過去8年分を項目別に整理し、弱点論点を切り出しやすい1冊です。"
                "TAC基本テキストと項目対応が取りやすく、テキスト読了後の演習メインにも向きます。"
                "5分野1周後に50問120分通しへ接続する前の分野別 drill として定番です。"
                "演習後は管業マスター過去問で同分野を解き直すと定着しやすくなります。",
            ),
            (
                "2位·3位：LEC分野別·Wマスター過去問集",
                "2026年版 出る順管理業務主任者 分野別過去問題集（LEC·約2,750円税込参考）は、"
                "5出題分野ごとに過去問を回しやすい構成です。"
                "past-questions-by-field記事の週15問ローテと相性がよく、速習テキストとの併用も定番です。\n\n"
                "2026年度版 Wマスター過去問集（Wマスター·4,400円税込参考）は、"
                "Wマスターテキスト読了後の通し演習に向く1冊です。"
                "10月以降の50問120分通し模試（月1〜2回）のメイン演習として使いやすく、"
                "マン管合格者の45問演習にも使い分けできます。",
            ),
            (
                "過去問の回し方（管業マスターとの併用）",
                "当サイトの過去問で5分野別正答率を把握したうえで、問題集で「時間を計って50問を解く」練習を行います。"
                "誤答は用語解説で類似論点まで整理し、1週間後に解き直してください。"
                "詳しい手順は past-question-strategy を参照。"
                "無料演習と問題集は役割分担が有効で、理解確認は年度別解説付き、本番形式は問題集側に寄せる構成がおすすめです。",
            ),
            (
                "テキスト未読のまま問題集だけ進めない",
                "条文·数値の前提が未整理のまま年度別通しを増やすと、解説を読んでも定着しにくくなります。"
                "テキスト該当章を読んだ直後から分野別10〜15問が定番です。"
                "正答率40％未満が続く分野は、新しい年度問を増やす前にテキスト該当章へ戻ってください。"
                "テキストと過去問の切替は textbook-vs-past-questions 記事でフェーズ別に整理できます。",
            ),
            (
                "購入前チェックリスト",
                "購入前に以下を確認してください。\n"
                "・2026年度版（最新版）か\n"
                "・管理業務主任者試験専用か\n"
                "・Amazon在庫·価格（執筆時点と異なる場合あり）\n"
                "・分野別·項目別·通しのどれを主役にするか学習計画と一致しているか\n"
                "・テキストと章·項目対応が取れる組み合わせか\n"
                "・中古は版·書き込み·付属解答の有無を販売ページで確認する\n"
                "・購入直前にAmazon販売ページで版表記·付属解答·在庫状況を再確認してください。",
            ),
        ],
        "faqs": [
            (
                "過去問だけで合格できますか？",
                "演習量は確保できますが、初めての論点はテキストで理解してから問題集に入る方が効率的です。"
                "おすすめテキストの記事で紹介している1冊と組み合わせる構成を推奨します。"
                "50問通しで35問以上を安定して超えられるまで、弱点分野の章戻りを続けてください。",
            ),
            (
                "問題集は何冊必要ですか？",
                "メイン1冊＋当サイト過去問で足りる場合が多いです。"
                "分野別 drill と通し模試の両方欲しい場合は2冊構成もあります。"
                "3冊を同時に開くより、フェーズごとに1冊に役割を絞ると計画が立てやすくなります。"
                "テキスト未読の論点が多い場合は、先におすすめテキストの記事で1冊を確定してください。",
            ),
            (
                "価格·在庫·最新版はどこで確認しますか？",
                "各商品のAmazon販売ページ（本記事の比較表リンク）で、税込価格·在庫·版表記を確認してください。"
                "2026-06-15時点ではTAC 約2,860円·LEC 約2,750円·Wマスター 4,400円（税込参考）でした。"
                "表紙の「2026年度版」表記と試験要項の学習範囲が一致するか購入前に確認してください。",
            ),
        ],
        "related_links": (
            "past-question-strategy:過去問の使い方;"
            "past-questions-by-field:分野別過去問;"
            "study-plan:学習計画;"
            "pass-score:合格基準;"
            "affiliate-textbooks-recommend:おすすめテキスト;"
            "textbook-vs-past-questions:テキストと過去問;"
            f"{amazon('4300120285')}:TAC項目別過去8年問題集（Amazon）"
        ),
        "key_points": (
            "2026年度版 管理業務主任者 項目別過去8年問題集;"
            "2026年版 出る順管理業務主任者 分野別過去問題集;"
            "2026年度版 Wマスター過去問集;"
            "問題集選びの基準;"
            "過去問の回し方"
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
            body_clean = body.replace("[[affiliate-hub-placeholder]]", "").strip()
            row[f"section_{i}_body"] = body_clean
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
