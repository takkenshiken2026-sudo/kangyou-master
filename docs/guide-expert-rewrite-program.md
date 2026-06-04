# 試験ガイド「編集合格」全件リライト

**正本:** `~/Projects/exam-site-shell/docs/guide-expert-rewrite-program.md`

**本サイトのお手本**

- slug: `exam-schedule`
- batch: `tools/kangyou_rewrite_exemplar.py`

**5本 batch の手順:** `docs/guide-hand-rewrite-batch-workflow.md`（`exam-site-shell` から sync）

**運用:** 危険物乙4 130/130 完走後に着手。現状 expert_pass **56/161**（exemplar + batch1–11 適用済み）。

```bash
cd ~/Projects/kangyou-master
python3 tools/run_guide_hand_batch.py --batch tools/kangyou_rewrite_batchN_expert.py
python3 tools/build_article_pages.py
```

**管業の正本・数字（exemplar で使用）**

- 一般社団法人 **マンション管理業協会** `https://www.mankan.or.jp/`
- **50問・120分・4肢択一・マークシート**（5出題分野）
- **受験手数料 8,900円**（非課税・要項で再確認。Web申込は事務手数料別）
- マンション管理士合格者は適正化法 **5問免除**（45問・120分）
- 令和8年度例: 試験日 **2026年12月6日（日）** 13:00〜15:00（要項で上書き確認）
