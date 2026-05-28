# 管業マスター（kangyou-master）

管理業務主任者試験向けの学習サイトです。

- **公開 URL:** https://kangyou-master.jp/
- **データ:** `data/past_questions.csv`（900問）・`practice_questions.csv`（500問）・`ichimon_questions.csv`（400問）

## データ取り込み

デスクトップの `管理業務主任者/` フォルダ内 CSV から再生成:

```bash
python3 tools/import_kangyou_questions.py
python3 tools/build_all.py
```

## パフォーマンス

Lighthouse のキャッシュ・レンダリングブロック対策は `docs/performance-cache.md` を参照。ビルド時に `tools/write_asset_version.py` がアセット版を更新します。

## デプロイ

**推奨:** `main` へ push すると GitHub Actions が `build_all.py` を実行し Pages へ公開します。

1. リポジトリ **Settings → Pages → Build and deployment → Source** を **GitHub Actions** に設定（初回のみ）
2. `main` に push

手動デプロイ（Actions が使えない場合のみ）:

```bash
bash tools/deploy_gh_pages.sh
```
