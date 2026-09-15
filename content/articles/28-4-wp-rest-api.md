---
title: "WordPress REST APIで記事データをスプレッドシートと照合する方法"
date: "2026-09-15"
article_no: "28-4"
category: "wordpress"
tags:
  - "wordpress"
  - "spreadsheet"
description: "WordPress REST APIで記事データをスプレッドシートと照合する方法について、初心者向けに具体的な手順・例・注意点を交えて解説します。"
point: "実際に確認・操作できるところまで具体的に解説します。"
---

## 結論
WordPress REST APIとスプレッドシートを照合すると、**「管理表にはあるのにWordPressにはない記事」や、その逆**を機械的に見つけられます。

重要なのは、タイトルではなく可能なら記事ID、slug、独自管理番号など**一意に近いキー**で突き合わせることです。

## 処理の流れ
1. スプレッドシートから納品対象の識別子を取得
2. WordPress REST APIから投稿済み記事を全件取得
3. 両方を同じ形式へそろえる
4. 集合の差分を取る
5. 不一致だけ一覧にする

## Pythonで考えると
```python
sheet_ids = {"A001", "A002", "A003"}
wordpress_ids = {"A001", "A003"}

missing = sheet_ids - wordpress_ids
extra = wordpress_ids - sheet_ids

print("WordPressにない:", missing)
print("管理表にない:", extra)
```

実際にはREST APIレスポンスやシートから識別子を作ります。

## タイトル照合だけだと弱い
全角半角、記号、末尾スペース、タイトル修正で一致しなくなるためです。タイトルしかキーがない場合は正規化し、不一致を人が確認します。

## 実際の投稿確認にも向いている
大量のWordPress投稿を目視で1件ずつ確認するより、APIで投稿一覧を取得して管理データと突き合わせれば、漏れ候補だけ確認できます。

## まとめ
照合は**件数比較→一意キー比較→不一致だけ人が確認**の順にすると、大量記事でも確認負荷を下げられます。
