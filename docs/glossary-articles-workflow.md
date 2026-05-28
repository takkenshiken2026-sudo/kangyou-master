# 用語解説記事の作成フロー（管理業務主任者）

## 方針

- 読者価値：定義・要件・数値・判例・実務の区別を試験向けに整理
- SEO：1用語1意図、信頼性表・FAQ・関連用語・内部リンク
- 正本：`data/glossary_terms.csv`（`comparison_table` 列は任意）

## 作業手順

```bash
# 1. 手作り本文を data/kangyou_glossary_handcrafted/*.json に追記
#    （civil / condo / ops / misc の4ファイル、計309語）
# 2. 品質検証
python3 tools/validate_kangyou_glossary_knowledge.py

# 3. CSV へ反映
python3 tools/enrich_kangyou_glossary_articles.py

# 4. ビルド・検証
python3 tools/build_all.py

# 5. デプロイ
bash tools/deploy_gh_pages.sh
```

## データ分割

| ファイル | 分野 |
|----------|------|
| `data/kangyou_glossary_handcrafted/civil.json` | 民法・借地借家法、判例・横断総合 |
| `data/kangyou_glossary_handcrafted/condo.json` | 区分所有法、標準管理規約 |
| `data/kangyou_glossary_handcrafted/ops.json` | 建築・設備、会計・税務、管理適正化法 |
| `data/kangyou_glossary_handcrafted/misc.json` | 委託契約書、品確法、宅建業法 |

旧形式（`tools/kangyou_glossary_knowledge_*.py`）は handcrafted JSON が無い場合のフォールバック。

## 必須フィールド（各用語）

`short_def`, `definition`, `term_detail_body`, `exam_points`, `common_mistakes`, `memory_tip`, `explanation`, `article_lead`, FAQ 2組

## 品質チェック

- `enrich_kangyou_glossary_articles.py` が全語更新済みであること
- `build_all.py` で内部リンク・SEO 検証 OK
- 一覧の定義抜粋がテンプレ文になっていないこと（`terms/index.html`）
