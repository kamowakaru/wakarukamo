---
title: "Markdownの記事をGitHub ActionsでHTMLへ自動変換する方法"
date: "2026-09-14"
category: "web"
tags:
  - markdown
  - github
  - github-pages
  - automation
description: "記事Markdownを追加するとGitHub ActionsがHTMLと記事一覧を生成する、静的ブログの自動化方法を基本構成から解説します。"
point: "人が編集する原稿と自動生成物を分けると、記事追加はMarkdown1ファイルだけにできます。"
---

## 結論

静的サイトでも、記事をMarkdownで管理し、GitHub ActionsでHTMLへ変換すれば、ブログのように記事を追加できます。

ワカルカモでは`content/articles`へMarkdownを1つ追加すると、記事HTML、一覧データ、タグページ、SNS投稿原稿などを自動生成します。毎回複数のHTMLを手で直さなくてよいため、記事数が増えても更新箇所を減らせます。

## 手作業でHTMLを増やす問題

記事をHTMLで直接作る場合、本文以外にも次の更新が必要になります。

- 記事一覧へカードを追加する
- トップページへ新着記事を表示する
- カテゴリページへ追加する
- タグページを更新する
- サイトマップへURLを追加する
- 関連記事を設定する

一つでも忘れると、記事ページは存在するのにサイト内から移動できない状態になります。

## 原稿と生成物を分ける

編集する原稿を`content/articles`、公開用HTMLを`articles`へ分けます。

```text
content/articles/sample.md  ← 人が編集
articles/sample.html        ← 自動生成
```

Markdown上部には、タイトルや日付などをfront matterとして記載します。

```text
---
title: "記事タイトル"
date: "2026-09-14"
category: "web"
tags:
  - github
description: "記事の説明文"
---
```

この情報を生成プログラムが読み取り、ページタイトルや記事一覧へ反映します。

## GitHub Actionsで処理を動かす

`.github/workflows`にワークフローファイルを置き、`content/articles`のMarkdownが変更されたときだけ生成プログラムを動かします。

主な処理は次のとおりです。

1. リポジトリの内容を取得する
2. Pythonなどの実行環境を準備する
3. 記事生成スクリプトを実行する
4. 変更されたHTMLやデータをコミットする

GitHub Pagesは静的ファイルを公開でき、独自の生成処理にはActionsを利用できます。[GitHub Pagesサイトを作成する](https://docs.github.com/ja/pages/getting-started-with-github-pages/creating-a-github-pages-site)

## 自動コミットによるループを防ぐ

生成されたHTMLのコミットで、同じ処理が何度も起動しないようにします。起動条件を`content/articles/**.md`や生成スクリプトだけに限定し、出力先の`articles`は条件から外します。

こうすると、人が原稿を変更したときは動きますが、Actionsが生成物を保存しただけでは再実行されません。

## 下書きも管理する

公開前の記事には`draft: true`を付け、生成対象から除外する方法があります。本文が完成したら`draft: false`へ変更するか、その行を削除します。

大量の記事を作る場合でも、空の雛形を公開しないための仕組みとして有効です。

## まとめ

MarkdownとGitHub Actionsを組み合わせると、静的サイトでも記事追加を自動化できます。原稿、生成プログラム、公開用HTMLの役割を分け、最初は一記事で動作確認してから対象を増やすのが安全です。
