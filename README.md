# 管業マスター（kangyou-master）

管理業務主任者試験向けの学習サイトです。

- **公開 URL（GitHub Pages）:** https://takkenshiken2026-sudo.github.io/kangyou-master/
- **データ:** `data/past_questions.csv`（900問）・`practice_questions.csv`（500問）・`ichimon_questions.csv`（400問）

## データ取り込み

デスクトップの `管理業務主任者/` フォルダ内 CSV から再生成:

```bash
python3 tools/import_kangyou_questions.py
python3 tools/build_all.py
```

## デプロイ

`main` へ push すると `.github/workflows/deploy-pages.yml` が `public_site/` を GitHub Pages へ公開します。  
リポジトリ Settings → Pages → Source を **GitHub Actions** に設定してください。
