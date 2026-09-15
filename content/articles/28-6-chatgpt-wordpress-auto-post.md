---
title: "ChatGPTで作った記事をWordPressへ自動投稿する方法｜OpenAI APIとREST APIを使う流れ"
date: "2026-09-16"
article_no: "28-6"
category: "ai-chatgpt"
tags:
  - chatgpt
description: "ChatGPTで作った記事をWordPressへ自動投稿する方法｜OpenAI APIとREST APIを使う流れについて、初心者向けに具体例と手順を交えて解説します。"
point: "仕組みを理解し、実際のデータやコードで確認しながら進めるのがポイントです。"
---

## 結論
ChatGPTで作った記事をWordPressへ自動投稿する仕組みは、**記事生成→内容チェック→WordPress REST API用データへ整形→認証→下書き投稿→確認→必要なら公開**という流れにすると安全です。

最初からAI生成直後に自動公開するより、`draft` で投稿して確認工程を残すのがおすすめです。

## 全体構成
1. OpenAI APIなどで記事本文を生成
2. タイトル・本文・slugなどを整形
3. WordPressのApplication Passwordを用意
4. `POST /wp/v2/posts` へ送信
5. `status: draft` で下書き作成
6. WordPress管理画面で内容確認
7. 問題なければ公開

## WordPressへ下書きを送るPython例
```python
import os
import requests
from requests.auth import HTTPBasicAuth

url = "https://example.com/wp-json/wp/v2/posts"
username = os.environ["WP_USERNAME"]
app_password = os.environ["WP_APP_PASSWORD"]

data = {
    "title": "テスト記事",
    "content": "<p>ここに確認済みの記事本文</p>",
    "status": "draft",
}

response = requests.post(
    url,
    json=data,
    auth=HTTPBasicAuth(username, app_password),
    timeout=30,
)
response.raise_for_status()

post = response.json()
print("作成した記事ID:", post["id"])
print("状態:", post["status"])
```

## Application Passwordを使う
WordPressのユーザープロフィールからApplication Passwordを発行できる環境では、外部スクリプト用の認証情報として利用できます。メインログインパスワードをコードへ書く必要はありません。

## AI生成と投稿を直結しすぎない
自動生成した記事には誤情報、リンクミス、HTML崩れ、重複などが含まれる可能性があります。

そのため、生成→QA→投稿を別工程にし、投稿後も記事IDを記録して二重投稿を防ぎます。

## 秘密情報を守る
OpenAI APIキーやWordPress Application Passwordはソースコードへ直書きせず、環境変数やSecretsへ保存します。公開GitHubへ含めないようにします。

## まとめ
AI記事の自動投稿は技術的には組み合わせられますが、重要なのは**自動公開することより、検査・下書き・重複防止まで含めて自動化すること**です。
