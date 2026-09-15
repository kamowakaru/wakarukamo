---
title: "WordPress REST APIで特定の記事を取得する方法"
date: "2026-09-15"
article_no: "28-2"
category: "wordpress"
tags:
  - "wordpress"
description: "WordPress REST APIで特定の記事を取得する方法について、初心者向けに具体的な手順・例・注意点を交えて解説します。"
point: "実際に確認・操作できるところまで具体的に解説します。"
---

## 結論
WordPress REST APIで特定の記事をID指定で取得するURLは次です。
```text
https://example.com/wp-json/wp/v2/posts/123
```
`123` をWordPressの記事IDへ置き換えます。

## Python例
```python
import requests

post_id = 123
url = f"https://example.com/wp-json/wp/v2/posts/{post_id}"

response = requests.get(url, timeout=30)
response.raise_for_status()
post = response.json()

print(post["id"])
print(post["slug"])
print(post["link"])
print(post["title"]["rendered"])
```

## slugなどで探したい場合
記事IDが分からずslugが分かるなら、一覧エンドポイントへクエリを付けて絞り込めます。
```text
https://example.com/wp-json/wp/v2/posts?slug=sample-post
```

返ってくるのは配列なので、0件の場合を考慮します。

## 下書きは同じ感覚で取れない
公開されていない記事など、権限が必要なデータは認証なしでは取得できません。

## まとめ
IDが分かるなら `/posts/<id>`、slugなどで探すなら一覧エンドポイントの絞り込みを使い分けます。
