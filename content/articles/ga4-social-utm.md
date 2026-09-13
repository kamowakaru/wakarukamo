---
title: "GA4でXとThreadsの流入を分けて確認する方法｜UTM設定例"
date: "2026-09-14"
category: "google-gas"
tags:
  - ga4
  - analytics
  - sns
  - utm
description: "XとThreadsへ同じ記事を投稿するとき、UTMパラメータでSNS別のアクセスをGA4へ記録し、流入を比較する方法を解説します。"
point: "utm_sourceだけ媒体別に変え、mediumとcampaignの命名を統一すると比較しやすくなります。"
---

## 結論

XとThreadsからの流入をGA4で分けるには、投稿する記事URLへ媒体別のUTMパラメータを付けます。

ワカルカモでは次のルールにしました。

```text
X
?utm_source=x&utm_medium=social&utm_campaign=article_share

Threads
?utm_source=threads&utm_medium=social&utm_campaign=article_share
```

GA4の追加イベント設定は不要です。UTM付きリンクからアクセスがあると、参照元やキャンペーンとして記録されます。

## UTMパラメータとは

UTMパラメータは、URLの末尾に付ける流入判別用の情報です。主に次の三つを使います。

- `utm_source`：どこから来たか
- `utm_medium`：どの種類の経路か
- `utm_campaign`：どの施策か

Googleの[Campaign URL Builder](https://ga-dev-tools.google/campaign-url-builder/)でも、パラメータ付きURLを作成できます。

## X用URLを作る

記事URLの後ろへ`?`を付け、次のようにつなげます。

```text
https://example.com/article.html?utm_source=x&utm_medium=social&utm_campaign=article_share
```

すでにURLへ`?`から始まる別のパラメータがある場合は、追加部分を`&`でつなぎます。

## Threads用URLを作る

`utm_source`だけを`threads`へ変更します。

```text
https://example.com/article.html?utm_source=threads&utm_medium=social&utm_campaign=article_share
```

大文字と小文字、`thread`と`threads`など表記が分かれると、GA4でも別の値になります。最初にルールを決め、毎回同じ文字を使います。

## GA4で確認する

標準レポートでは、`レポート → 集客 → トラフィック獲得`を開き、表の項目を`セッションの参照元／メディア`へ変更します。

アクセスがあれば、次のような値で確認できます。

```text
x / social
threads / social
```

自由探索で比較する場合は、行へ`セッションの参照元／メディア`、値へ`セッション`、フィルタへキャンペーン`article_share`を設定します。

## 投稿文とURLを一緒に作る

記事を公開するたびに手でUTMを付けると、表記揺れや貼り間違いが起きます。ワカルカモでは、記事MarkdownからX・Threads用の投稿文と媒体別URLを一つのTXTへ自動生成し、最後の投稿だけ手動にしました。

自動投稿APIを使わなくても、文章とURLの準備を自動化すれば作業を減らせます。[SNS投稿原稿だけを自動生成する方法](sns-manual-draft-automation.html)もあわせて確認してください。

## まとめ

XとThreadsは`utm_source`を分け、`utm_medium`と`utm_campaign`を統一します。リンクを投稿する前に実際に開けるか確認し、アクセス後にGA4のトラフィック獲得で比較しましょう。
