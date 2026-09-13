---
title: "GitHub Pagesが更新されないときは？反映されない原因と確認方法"
date: "2026-09-14"
category: "web"
tags:
  - github
  - github-pages
  - website
description: "GitHubへファイルを追加したのにGitHub Pagesへ反映されないとき、コミット・公開元・Actions・キャッシュを順番に確認する方法を解説します。"
point: "GitHub上のファイル、Actionsの結果、公開ページの順に確認すると、どこで更新が止まったか切り分けられます。"
---

## 結論

GitHub Pagesが更新されないときは、闇雲にファイルを入れ直さず、次の順番で確認します。

1. GitHub上で目的のファイルが更新されているか
2. コミットが完了しているか
3. Pagesの公開元が合っているか
4. GitHub Actionsが成功しているか
5. ブラウザに古い表示が残っていないか

この順番なら、アップロード・自動生成・公開・閲覧のどこで止まったか判断できます。

## GitHub上のファイルを確認する

最初に、リポジトリで変更したファイルを開きます。更新日時や内容が古ければ、アップロードまたはコミットが完了していません。

ZIPの外側フォルダごと入れた場合、元の`index.html`とは違う場所へ新しいファイルが追加されることがあります。ファイル名だけでなく、上部に表示されるフォルダ階層も確認します。

## Pagesの公開元を確認する

`Settings → Pages`を開き、公開に使用しているブランチとフォルダを確認します。

たとえば`main`の`/(root)`を公開元にしているなら、別ブランチや`docs`フォルダへ入れた変更は公開ページへ反映されません。GitHub Pagesでは、ブランチまたはGitHub Actionsを公開元にできます。[公開元の設定方法](https://docs.github.com/ja/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Actionsの結果を確認する

記事MarkdownからHTMLを作るような自動処理を使っている場合は、リポジトリ上部の`Actions`を開きます。

- 緑のチェック：処理成功
- 黄色の丸：実行中
- 赤い印：エラーで停止

赤い印がある場合は、実行結果を開き、最初にエラーになった行を確認します。タグ名の登録漏れ、front matterの書式、ファイルパスの間違いなどが原因になることがあります。

## ブラウザのキャッシュを確認する

GitHub Pages側は更新されていても、ブラウザが以前のCSSや画像を表示している場合があります。

Windowsなら`Ctrl + F5`で再読み込みするか、シークレットウィンドウで公開URLを開きます。別の端末でも同じ表示なら、ブラウザだけの問題ではないと判断できます。

## 反映には時間がかかる場合がある

GitHub公式では、変更後の公開に時間がかかる場合があると案内されています。コミット直後に古い画面が出ても、まずActionsやPagesの状態を確認し、少し待ってから再読み込みします。[GitHub Pagesサイトの作成](https://docs.github.com/ja/pages/getting-started-with-github-pages/creating-a-github-pages-site)

## まとめ

更新されない原因は、アップロード失敗とは限りません。GitHub上のファイル、公開元、Actions、ブラウザの順に確認すれば、同じファイルを何度も差し替えずに原因を見つけやすくなります。
