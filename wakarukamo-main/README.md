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
- X・Threadsへコピペする投稿原稿TXT

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
point: "この記事で特に覚えておきたい要点です。"
---

## 結論

ここに本文。

## 手順

本文……
```

`slug` は Markdown のファイル名です。例: `gas-match-list.md` → `/articles/gas-match-list.html`

公開前の下書きは front matter に `draft: true` を追加します。HTML記事ページは生成されず、トップ・記事一覧・カテゴリ・タグ・サイトマップにも表示されません。完成したらこの行を削除するか `draft: false` にします。

記事を大きく更新した場合は `updated: "2026-09-13"` のように更新日を追加できます。検索エンジン向けの構造化データとサイトマップへ反映されます。

## サムネイル画像
各カテゴリには `assets/images/thumbnails/<category>/` 内に10種類のJPEG画像があります。
記事のタイトル・説明・タグに合う画像を優先し、該当しない場合はslugをもとに10種類から自動選択します。同じ記事の画像は再生成しても変わりません。

特定の画像を使いたい場合だけ front matter に追加します。

```md
thumbnail: "google-gas/03.jpg"
```

独自画像も `assets/images/thumbnails/` 以下へ置けば、同じ形式で指定できます。

## ワカルカモポイント
記事内にポイント枠を表示したい場合は、front matterへ `point` を追加します。

```md
point: "この記事で特に覚えておきたいことを一文で書きます。"
```

設定した記事だけ、カモの顔と電球の専用アイコン付きで表示されます。

## 著者情報
すべての記事には「ワカルカモ運営者」の著者名と著者欄が自動表示されます。詳しいプロフィールは `about.html#author-profile` に掲載し、記事の構造化データからも同じプロフィールへ関連付けます。

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

## サイト内検索キーワードの計測
検索結果ページを開いたとき、検索語と検索結果件数をGoogle Analytics 4へ送信できます。

1. Google Analyticsでワカルカモ用のウェブデータストリームを作る
2. `G-` から始まる測定IDを確認する
3. `assets/js/analytics-config.js` を開く
4. 次の空欄へ測定IDを入れてcommitする

```js
window.WAKARUKAMO_GA_MEASUREMENT_ID = 'G-XXXXXXXXXX';
```

設定前はアクセス解析を送信しません。空欄検索、メールアドレスを含む検索語、9桁以上の数字列を含む検索語は記録対象外です。検索語は80文字まで送信します。

GA4ではイベント名 `search`、パラメータ `search_term` と `result_count` で確認できます。個人情報を検索欄へ入力しないよう、プライバシーポリシーにも注意書きを掲載しています。

## GitHubで記事を書く手順
1. `content/articles` を開く
2. **Add file → Create new file**
3. `○○.md` という名前にする
4. 上の形式で記事を書く
5. **Commit changes**
6. Actions の `Build articles` が動き、生成物を自動コミット
7. GitHub Pages が更新される

## X・Threads用の投稿原稿
記事Markdownを追加・更新すると、自動投稿はせず、コピペ用のテキストファイルを生成します。

生成場所は `social-drafts/<slug>.txt` です。1つのファイルに以下が入ります。

- X案1：要点型（280文字以内）
- X案2：問いかけ型（280文字以内）
- Threads案：読者の体験に寄り添う文章
- 投稿前チェックリスト

各投稿文のURLにはX・Threads別のUTMパラメータが付くため、GA4でSNS別の流入を確認できます。使いたい案をコピーして、内容を確認してから手動で投稿してください。

特定の記事だけSNS原稿を作らない場合は、front matterへ `social: false` を追加します。

## Shorts / TikTok動画
`data/analytics-pageviews.csv` が更新されると、PV上位3記事について15秒・縦型（1080×1920）のMP4下書きを作ります。初期値は100PV以上です。GitHubの **Settings → Secrets and variables → Actions → Variables** に `MIN_POPULAR_VIEWS` を登録すると基準を変更できます。

動画はActionsの `Build popular article videos` を開き、実行結果のArtifactsにある `wakarukamo-shorts-tiktok` からダウンロードします。自動アップロードにはせず、内容・音源を確認してからYouTube Shorts / TikTokへ投稿する設計です。

## 画像
`assets/images/` の以下3点は、今回ユーザーが差し替えたカモ画像です。Webページでは表示速度を上げるため軽量なWebP版を使い、元のSVGも保管しています。
- `logo-duck.webp`
- `hero-duck.webp`
- `tip-duck.webp`
