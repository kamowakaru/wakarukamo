---
title: "GitHub PagesをGoogle Search Consoleへ登録する方法"
date: "2026-09-14"
category: "web"
tags:
  - search-console
  - github-pages
  - seo
description: "GitHub Pagesで公開したサイトをGoogle Search Consoleへ追加し、検索状況を確認できるようにする流れを解説します。"
point: "github.io配下のサイトでは、URLプレフィックスで正確な公開URLを登録するとHTMLファイル確認を使えます。"
---

## 結論

GitHub PagesのサイトもGoogle Search Consoleへ登録できます。サイトの公開URLをプロパティとして追加し、所有権を確認したあと、サイトマップを送信します。

ワカルカモではGitHub PagesのURLを登録し、Googleからページが見えているか、どんな検索語で表示されたかを確認できるようにしました。

## Search Consoleでできること

Search Consoleでは、主に次の情報を確認できます。

- Google検索で表示された回数
- 検索結果からクリックされた回数
- 検索に使われた語句
- ページが登録されているか
- サイトマップの読み込み状況
- クロールやインデックス登録の問題

GA4がサイト内での行動を見るのに対し、Search ConsoleはGoogle検索に表示されるまでと、検索結果からの流入を見るためのサービスです。

## 1．プロパティを追加する

Search Consoleを開き、プロパティ追加画面でGitHub Pagesの公開URLを入力します。

```text
https://kamowakaru.github.io/wakarukamo/
```

GitHub Pagesのプロジェクトサイトでは、ユーザー名だけでなくリポジトリ名まで含めます。`http`と`https`、末尾の階層も確認してください。

## 2．所有権を確認する

URLプレフィックスでは、HTML確認ファイルを使えます。Search Consoleから指定されたHTMLをダウンロードし、GitHubリポジトリの公開元直下へ追加します。

公開後に指定URLでファイルを開けることを確認し、Search Consoleへ戻って確認ボタンを押します。確認ファイルは削除すると所有権を失う可能性があるため、登録後も残します。[Search Consoleの所有権を確認する](https://support.google.com/webmasters/answer/9008080?hl=ja)

## 3．サイトマップを送信する

所有権を確認できたら、左側の`サイトマップ`を開き、サイトマップのURLを送信します。

```text
https://kamowakaru.github.io/wakarukamo/sitemap.xml
```

ステータスが成功になれば、GoogleへURL一覧の場所を伝えられています。ただし、送信しただけで全ページの登録が保証されるわけではありません。

## 4．登録状況を待つ

新しいサイトでは、検索データやページ登録状況がすぐにそろわないことがあります。エラーがなければ何度も設定をやり直さず、数日後に確認します。

特定ページだけ確認したい場合はURL検査を使います。すべての記事で毎回リクエストが必要かは、[新しい記事ごとにインデックス登録をリクエストする必要はあるか](search-console-request-indexing.html)で説明しています。

## まとめ

GitHub PagesをSearch Consoleへ登録する流れは、URL追加、所有権確認、サイトマップ送信の三段階です。正しい公開URLを使い、確認ファイルを残しておくことがポイントです。
