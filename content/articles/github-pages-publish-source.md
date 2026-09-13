---
title: "GitHub Pagesの公開元はどれを選ぶ？ブランチとActionsの違い"
date: "2026-09-14"
category: "web"
tags:
  - github
  - github-pages
  - automation
description: "GitHub PagesのDeploy from a branchとGitHub Actionsの違いを整理し、静的サイトや自動生成サイトに合う公開方法を解説します。"
point: "完成済みHTMLをそのまま公開するならブランチ、公開前にビルドが必要ならActionsが判断の目安です。"
---

## 結論

GitHub Pagesの公開元は、完成済みのHTMLを置くだけなら`Deploy from a branch`、公開前に変換やビルドが必要なら`GitHub Actions`が向いています。

ワカルカモでは、サイト自体はブランチから公開し、記事MarkdownをHTMLへ変換する処理にGitHub Actionsを使っています。このように、ページ公開とファイル生成を分ける構成も可能です。

## Deploy from a branchとは

指定したブランチの`/(root)`または`/docs`フォルダにあるファイルを公開する方法です。

向いているケースは次のとおりです。

- `index.html`がすでに完成している
- HTML・CSS・JavaScriptをそのまま配信したい
- 複雑なビルド処理がない
- 初めてGitHub Pagesを使う

設定項目が少なく、どのファイルが公開されるか理解しやすいのがメリットです。

## GitHub Actionsを公開元にする方法

Actionsを使うと、公開前にコマンドを実行し、生成したファイルをGitHub Pagesへ送れます。

たとえば次のようなサイトに向いています。

- MarkdownをHTMLへ変換する
- Node.jsなどでサイトをビルドする
- テスト成功後だけ公開する
- 公開用ファイルを別にまとめる

GitHub公式でも、独自のビルド処理が必要な場合はカスタムActionsワークフローを利用できると案内されています。[GitHub Pagesの公開元を設定する](https://docs.github.com/ja/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## ワカルカモの構成

ワカルカモの記事原稿は、`content/articles`にMarkdownで保存します。そのままではサイトの記事ページにならないため、ActionsでPythonスクリプトを動かしてHTMLを生成します。

```text
記事Markdownを追加
↓
GitHub Actionsが起動
↓
HTML・記事一覧データ・SNS原稿を生成
↓
生成結果をmainブランチへ保存
↓
GitHub Pagesで公開
```

この構成なら、記事を書くたびにHTML全体を手作業で編集する必要がありません。

## どちらを選べばよいか

最初から複雑にする必要はありません。まずブランチ公開で`index.html`が見える状態を作り、記事数が増えて手作業が負担になった段階でActionsを追加する方法もあります。

自動生成の具体例は、[Markdownの記事をGitHub Actionsで公開する方法](markdown-github-actions-blog.html)で説明しています。

## まとめ

公開元の選択は、サイトを公開する前に処理が必要かどうかで考えます。完成済みファイルならブランチ、変換やテストが必要ならActionsが基本です。現在の構成を理解したうえで、必要なところだけ自動化しましょう。
