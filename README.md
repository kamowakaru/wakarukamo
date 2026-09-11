# ワカルカモ

GitHub Pages向けの静的サイトです。

## 記事追加は基本1ファイルだけ
`content/articles/` に Markdown (`.md`) を1つ追加して commit すると、GitHub Actions が自動で以下を更新します。

- `articles/<slug>.html` の記事ページ
- `data/articles.json` の記事一覧データ
- 記事一覧ページ
- カテゴリページ
- タグページ
- トップページの最新6記事
- 同カテゴリの関連記事
- アクセス集計CSVの新規記事行

### 記事ファイル例
ファイル名: `content/articles/gas-match-list.md`

```md
---
title: "GASで2つの一覧を照合する方法"
date: "2026-09-11"
category: "google-gas"
tags:
  - gas
  - spreadsheet
  - automation
description: "2つの一覧を比較して差分を確認する方法を解説します。"
---

## 結論

ここに本文。

## 手順

本文……
```

`slug` は Markdown のファイル名です。例: `gas-match-list.md` → `/articles/gas-match-list.html`

## カテゴリ
`data/categories.json` が固定マスタです。基本は1記事1カテゴリ。

現在のカテゴリ:
- `pc-windows`
- `web`
- `wordpress`
- `google-gas`
- `ai-chatgpt`
- `other`

## タグ
`data/tags.json` がタグマスタです。記事では slug を指定します。
既存タグだけで記事を書く場合は、記事Markdown1個の追加だけでOKです。
新しいタグを使う場合だけ `data/tags.json` に追加してください。タグページは自動生成されます。

## 人気タグ
`data/analytics-pageviews.csv` のPVをタグ単位に加算し、`scripts/update_popular_tags.py` が `data/popular-tags.json` を更新します。
GA4等からPVをCSVへ入れる処理は次の段階で接続できます。

## GitHubで記事を書く手順
1. `content/articles` を開く
2. **Add file → Create new file**
3. `○○.md` という名前にする
4. 上の形式で記事を書く
5. **Commit changes**
6. Actions の `Build articles` が動き、生成物を自動コミット
7. GitHub Pages が更新される

## 画像
`assets/images/` の以下3点は、今回ユーザーが差し替えたカモ画像です。
- `logo-duck.svg`
- `hero-duck.svg`
- `tip-duck.svg`
