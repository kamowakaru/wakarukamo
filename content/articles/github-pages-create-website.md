---
title: "GitHub PagesでWebサイトを作る方法｜無料公開までの手順"
date: "2026-09-14"
category: "web"
tags:
  - github
  - github-pages
  - website
description: "GitHubのリポジトリへHTMLファイルを置き、GitHub PagesでWebサイトを無料公開する基本手順を初心者向けに解説します。"
point: "最初はindex.htmlをリポジトリ直下へ置き、公開元をmainブランチのrootにすると構成を理解しやすくなります。"
---

## 結論

GitHub Pagesを使うと、HTML・CSS・JavaScriptで作った静的なWebサイトを公開できます。サーバーを自分で契約しなくても始められるため、ポートフォリオや小規模な情報サイトを試作したいときに便利です。

ワカルカモも、GitHubのリポジトリへサイト一式を置き、GitHub Pagesで公開しています。最初に必要なのはGitHubアカウント、公開用リポジトリ、入口となる`index.html`です。

## GitHub Pagesで公開できるサイト

GitHub Pagesは、ブラウザへそのまま配信できる静的ファイルに向いています。

- HTMLで作るトップページ
- CSSを使ったデザイン
- JavaScriptによる検索や表示切り替え
- 画像やPDFなどの素材
- Markdownから事前生成した記事ページ

一方、PHPやデータベースをサーバー上で動かす構成には向きません。お問い合わせフォームなど、サーバー処理が必要な機能は外部サービスを使うか、メールリンクなど別の方法を検討します。

## 1．公開用リポジトリを作る

GitHubへログインし、新しいリポジトリを作成します。無料プランでGitHub Pagesを使う場合は、まず公開リポジトリで始めると分かりやすいでしょう。

リポジトリ名はサイトURLの一部になります。たとえばユーザー名が`kamowakaru`、リポジトリ名が`wakarukamo`なら、基本URLは次の形です。

```text
https://kamowakaru.github.io/wakarukamo/
```

## 2．index.htmlを置く

公開元の一番上に`index.html`を置きます。これはサイトへアクセスしたとき最初に表示される入口です。

最低限、次のような内容でもページとして公開できます。

```html
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>はじめてのサイト</title>
</head>
<body>
  <h1>サイトを公開しました</h1>
</body>
</html>
```

## 3．GitHub Pagesを有効にする

リポジトリの`Settings`を開き、左側の`Pages`へ進みます。公開元をブランチにする場合は、`Deploy from a branch`を選び、`main`と`/(root)`を指定して保存します。

GitHub公式ドキュメントでも、ブランチまたはGitHub Actionsを公開元にできると説明されています。[GitHub Pagesの公開元を設定する](https://docs.github.com/ja/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## 4．公開URLを確認する

設定後は`Settings → Pages`に表示されるURLを開きます。反映には少し時間がかかることがあります。すぐに表示されない場合は、数分待って再読み込みしてください。

それでも表示されなければ、`index.html`の場所、ファイル名、選択したブランチを確認します。大文字と小文字も区別されるため、`Index.html`ではなく`index.html`にそろえるのが安全です。

## 最初は小さく公開してから増やす

完成した大量のファイルを一度に入れるより、最初に`index.html`だけで公開確認をすると原因を切り分けやすくなります。公開できたあとにCSS、画像、記事ページを追加していけば、どの変更で問題が起きたか判断しやすくなります。

AIを使ってサイト一式を作った流れは、[ChatGPTでWebサイトを作ってみた体験](chatgpt-build-website-review.html)で紹介しています。

## まとめ

GitHub PagesでWebサイトを公開する基本は、リポジトリを作り、`index.html`を置き、Pagesの公開元を設定することです。まず小さなページで公開を確認し、そのあと必要なファイルを追加すると迷いにくくなります。
