---
title: "WordPress REST APIで投稿数・公開記事を確認する方法"
date: "2026-09-15"
article_no: "28-3"
category: "wordpress"
tags:
  - "wordpress"
description: "WordPress REST APIで投稿数・公開記事を確認する方法について、初心者向けに具体的な手順・例・注意点を交えて解説します。"
point: "実際に確認・操作できるところまで具体的に解説します。"
---

## 結論
WordPress REST APIで投稿数を確認するなら、**レスポンスヘッダーの総件数を使う方法**と、ページングして記事データを取得する方法があります。

## Pythonで総件数を確認する
```python
import requests

url = "https://example.com/wp-json/wp/v2/posts"
response = requests.get(url, params={"per_page": 1}, timeout=30)
response.raise_for_status()

total = response.headers.get("X-WP-Total")
total_pages = response.headers.get("X-WP-TotalPages")

print("投稿数:", total)
print("総ページ数:", total_pages)
```

## 公開記事を実データで確認する
一覧をページングして、取得したIDやslugを保存すれば「件数だけ合うが別の記事が抜けている」といったケースも確認できます。

## 件数だけでは投稿漏れを断定できない
管理表100件、WordPress100件でも、1件抜けて別の記事が1件多ければ件数は一致します。

そのため納品確認では、件数＋記事を識別できるID・slug・管理番号などを照合するほうが確実です。

## まとめ
投稿数はヘッダーで素早く確認できますが、**投稿漏れチェックでは記事単位の突き合わせまで行う**のがおすすめです。
