# GitHub Pages（Actions）— push だけで公開

## 初回セットアップ（1回）

### 1. workflow ファイルを GitHub に置く

**方法 A — ローカルから push（推奨）**

Cursor / ターミナルで PAT に **`workflow`** スコープを付けて push:

```bash
cd /Users/otedaiki/Desktop/kangyou-master
git push origin main
```

未 push のコミット `Enable GitHub Actions deploy on push to main` に `.github/workflows/deploy-pages.yml` が含まれています。

**方法 B — GitHub Web UI**

1. https://github.com/takkenshiken2026-sudo/kangyou-master で **Add file → Create new file**
2. パス: `.github/workflows/deploy-pages.yml`
3. 内容はリポジトリ内の同名ファイルをコピー
4. **Commit directly to the `main` branch**

### 2. Pages の Source を Actions に変更

1. **Settings → Pages**
2. **Build and deployment → Source:** **GitHub Actions**
3. 保存

### 3. 初回ビルド

- **Actions** タブ → **Deploy GitHub Pages** → **Run workflow**  
  または `main` に空コミット push

### 4. （任意）旧 `gh-pages` ブランチを削除

Actions 運用後は不要です。

1. **Settings → Pages** が Actions になっていることを確認
2. **Code → Branches** → `gh-pages` → Delete

`gh-pages had recent pushes` の通知も出なくなります。

## 日常運用

```bash
# データ更新時
python3 tools/import_kangyou_questions.py   # CSV 変更時のみ
python3 tools/build_all.py                    # ローカル確認用（任意）

git add …
git commit -m "…"
git push origin main
```

push 後、**Actions** タブで緑チェック → 数分で https://kangyou-master.jp/ が更新されます。

## トラブル

| 症状 | 対処 |
|------|------|
| workflow push が拒否される | PAT に `workflow` 権限を付与、または Web UI でファイル作成 |
| Actions が走らない | Pages Source が **GitHub Actions** か確認 |
| build 失敗 | Actions ログで `validate_csv` / `build_all` のエラーを確認 |
