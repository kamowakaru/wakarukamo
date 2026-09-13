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

## SNSへの自動投稿
新しい記事Markdownを追加したときだけ、記事公開後に次の処理を行います。本文の修正や自動生成コミットでは再投稿しません。

- X: APIの従量課金を避け、280文字以内のコピペ用原稿を自動生成
- Threads: 読者の体験に寄り添う文章で投稿
- Pinterest: 「方法・手順・設定」などのHow-to記事だけ画像Pinを作成
- LinkedIn: 仕事・業務効率化・自動化に関係する記事だけ投稿
- YouTube Shorts / TikTok: 人気記事の縦型MP4を生成（投稿前に人が確認）

各SNSの認証情報は、GitHubの **Settings → Secrets and variables → Actions → New repository secret** で登録します。ZIPや記事ファイルには書かないでください。

| Secret名 | 内容 |
|---|---|
| `SITE_URL` | 公開サイトURL（例: `https://ユーザー名.github.io/リポジトリ名`） |
| `THREADS_USER_ID` | ThreadsのユーザーID |
| `THREADS_ACCESS_TOKEN` | Threads投稿用アクセストークン |
| `PINTEREST_ACCESS_TOKEN` | Pin作成権限付きアクセストークン |
| `PINTEREST_BOARD_ID` | 投稿先ボードID |
| `LINKEDIN_ACCESS_TOKEN` | Posts API用アクセストークン |
| `LINKEDIN_AUTHOR_URN` | 投稿者URN（例: `urn:li:person:...`） |
| `LINKEDIN_VERSION` | 利用中のLinkedIn APIバージョン（例: `202601`） |

未設定のSNSは警告だけ表示してスキップし、サイト公開は止めません。記事ごとに判定を上書きする場合はfront matterへ `pinterest: true`、`pinterest: false`、`linkedin: true`、`linkedin: false` を追加できます。全SNSへの投稿を止める記事は `social: false` にします。

記事ごとのコピペ用原稿は `social-drafts/<slug>.md` に生成されます。Xは「要点型」「問いかけ型」の2案から選べます。各媒体のURLにはUTMパラメータが付き、アクセス解析を接続した際に流入元を区別できます。

## Shorts / TikTok動画
`data/analytics-pageviews.csv` が更新されると、PV上位3記事について15秒・縦型（1080×1920）のMP4下書きを作ります。初期値は100PV以上です。GitHubの **Settings → Secrets and variables → Actions → Variables** に `MIN_POPULAR_VIEWS` を登録すると基準を変更できます。

動画はActionsの `Build popular article videos` を開き、実行結果のArtifactsにある `wakarukamo-shorts-tiktok` からダウンロードします。自動アップロードにはせず、内容・音源を確認してからYouTube Shorts / TikTokへ投稿する設計です。

## 画像
`assets/images/` の以下3点は、今回ユーザーが差し替えたカモ画像です。
- `logo-duck.svg`
- `hero-duck.svg`
- `tip-duck.svg`
