---
title: "WordPress REST APIとは？できること・使い方を初心者向けに解説"
date: "2026-09-15"
article_no: "28"
category: "wordpress"
tags:
  - "wordpress"
description: "WordPress REST APIとは？できること・使い方を初心者向けに解説について、初心者向けに具体的な手順・例・注意点を交えて解説します。"
point: "実際に確認・操作できるところまで具体的に解説します。"
---

## 結論
WordPress REST APIは、WordPressの記事・固定ページ・カテゴリーなどを**外部プログラムからJSONで取得・操作するための仕組み**です。

公開記事は認証なしで取得できる場合があり、作成・更新など権限が必要な操作では認証が必要です。

## まずブラウザで試す
自分のサイトURLが `https://example.com` なら、次を開きます。
```text
https://example.com/wp-json/wp/v2/posts
```
公開記事のJSONが表示されれば、Postsエンドポイントへアクセスできています。

## 記事取得
一覧は `GET /wp/v2/posts`、特定記事は `GET /wp/v2/posts/<id>` を使います。

## 投稿・更新
記事作成は `POST /wp/v2/posts`。外部スクリプトから行う場合は認証が必要です。WordPressにはApplication Passwordsがあり、メインのログインパスワードを外部スクリプトへ渡さず認証できます。

## ワカルカモで役立つ考え方
WordPressへの委託投稿のように件数が多い作業では、REST APIで投稿済み記事を取得し、手元の管理データと照合すれば、投稿漏れなどを機械的に確認できます。

## まとめ
WordPress REST APIは、**管理画面を人が目視するだけでは大変な取得・照合・自動投稿をプログラム化できる入口**です。
