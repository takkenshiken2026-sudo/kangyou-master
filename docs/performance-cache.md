# パフォーマンス（キャッシュ・LCP）

## コード側の対策（本リポジトリ）

- **問題データ JS**（`exam-site-data-*.js`）は `site-exam-data-loader.js` で初回描画後に読み込み（レンダリングブロック回避）
- **`site-theme.css`** は `<head>` で先読み
- **`site-asset-version.js`** … ビルド時にハッシュを書き出し、クエリ `?v=` でキャッシュ更新
- **`sw.js`** … 静的 JS/CSS をブラウザに長期キャッシュ（GitHub Pages の `max-age=600` を補完）
- **GA4** … `requestIdleCallback` で gtag 読み込みを遅延（強制リフロー軽減）

ビルド: `python3 tools/build_all.py`（末尾で `write_asset_version.py` を実行）

## Cloudflare（kangyou-master.jp）

本番は Cloudflare 経由のため、ダッシュボードで次を設定すると PageSpeed の「効率的なキャッシュ」がさらに改善します。

1. **Rules → Cache Rules**（または Page Rules）
2. 対象: URI Path が `/exam-site-data-` で始まる、または拡張子 `.js` / `.css`
3. **Edge TTL**: 1 か月以上
4. **Browser TTL**: 1 日以上（または Respect origin）
5. デプロイ後に **Caching → Configuration → Purge Everything** で古い 10 分キャッシュを一度消す

クエリ `?v=` 付き URL はファイル更新時に自動で別キャッシュキーになります。
