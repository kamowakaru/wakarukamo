# ワカルカモ 完成ベース

## 収録内容
- トップページ
- 記事一覧
- 6カテゴリの一覧ページ
- タグ一覧ページ（サンプル記事で使う12タグ）
- 6カテゴリそれぞれに記事雛形1本
- 検索ページ
- About / Contact / Privacy / 404
- PC・タブレット・スマホ対応
- ベクター形式（SVG）のカモ画像3種
- カテゴリ・タグ・記事メタデータのJSON管理
- 人気タグ集計スクリプト

## 管理方法
### カテゴリ
`data/categories.json` がカテゴリのマスタです。原則として1記事1カテゴリ。

### タグ
`data/tags.json` がタグのマスタです。1記事に複数付与できます。表記揺れを防ぐため、新しいタグは先にここへ追加します。

### 記事
`data/articles.json` にタイトル・slug・日付・カテゴリ・タグ・descriptionを登録します。
記事本文は `articles/*.html` です。

## 人気タグ
`data/analytics-pageviews.csv` に記事URLとPV数が入ると、`scripts/update_popular_tags.py` が各記事のPVをタグへ加算し、上位8タグを `data/popular-tags.json` に出力します。
PVが全て0の間は、記事数を仮スコアにします。

GitHub Actionsの `.github/workflows/rebuild-popular-tags.yml` も同梱しています。
CSVが更新されるとランキングを再計算します。

※実際のアクセス数を完全自動で入れるには、後からGA4またはSearch Consoleの取得処理を接続してください。

## ローカル確認
JSONをfetchしているため、`index.html` を直接ダブルクリックするより、簡易HTTPサーバーで確認するのが確実です。

例：
`python -m http.server 8000`

その後 `http://localhost:8000/` を開きます。GitHub Pages上ではそのまま動作します。
