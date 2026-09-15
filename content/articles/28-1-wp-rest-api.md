---
title: "WordPress REST APIで記事一覧を取得する方法"
date: "2026-09-15"
article_no: "28-1"
category: "wordpress"
tags:
  - "wordpress"
description: "WordPress REST APIで記事一覧を取得する方法について、初心者向けに具体的な手順・例・注意点を交えて解説します。"
point: "実際に確認・操作できるところまで具体的に解説します。"
---

## 結論
WordPress REST APIで公開記事一覧を取得する基本URLは次です。
```text
https://あなたのサイト/wp-json/wp/v2/posts
```
GETリクエストなので、公開記事の取得だけならブラウザでURLを開いて確認できるサイトもあります。

## Pythonで取得する
```python
import requests

url = "https://example.com/wp-json/wp/v2/posts"
params = {"per_page": 10, "page": 1}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

posts = response.json()

for post in posts:
    print(post["id"], post["link"], post["title"]["rendered"])
```

`example.com` は自分のWordPressサイトへ置き換えます。

## 件数を増やす
`per_page` で1ページあたりの件数、`page` でページ番号を指定できます。大量の記事を全部取得するときはページングが必要です。

## 必要な項目だけ使う
レスポンスにはID、リンク、slug、status、titleなど多くの情報があります。照合ならIDやslugなど、目的に必要な値だけ取り出します。

## まとめ
まずブラウザでエンドポイントを確認し、その後PythonやGASからGETする流れにすると切り分けやすくなります。
