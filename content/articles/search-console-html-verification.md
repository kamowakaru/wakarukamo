---
title: "Search ConsoleのHTML確認ファイルをGitHub Pagesへ置く方法"
date: "2026-09-14"
category: "web"
tags:
  - search-console
  - github
  - github-pages
description: "Google Search Consoleから取得した所有権確認用HTMLファイルを、GitHub Pagesの正しい場所へ追加する方法を解説します。"
point: "確認ファイルは名前も中身も変えず、公開URLの直下で直接開ける場所へ置きます。"
---

## 結論

Search ConsoleのHTML確認ファイルは、ダウンロードした名前と内容を変えず、GitHub Pagesの公開元直下へ置きます。GitHubへ追加しただけでなく、ブラウザから確認用URLを開ける状態になってから、Search Consoleの確認ボタンを押します。

## HTML確認ファイルとは

Search Consoleは、登録しようとしているサイトを本当に管理できるか確認します。HTMLファイル方式では、Googleが指定した名前のファイルをサイトへ置けることが所有権の証明になります。

ファイル名は次のような形です。

```text
googlexxxxxxxxxxxxxxxx.html
```

この文字列は利用者ごとに異なるため、別の人のファイルを流用できません。

## GitHubへ追加する場所

ワカルカモのように`main`ブランチの`/(root)`を公開している場合、確認ファイルもリポジトリ直下へ置きます。

```text
index.html
sitemap.xml
googlexxxxxxxxxxxxxxxx.html
```

`assets`や`articles`の中へ入れると、Search Consoleが指定するURLと一致しません。

## アップロード手順

1. Search ConsoleからHTMLファイルをダウンロードする
2. GitHubで対象リポジトリを開く
3. `Add file → Upload files`を選ぶ
4. HTMLファイルを追加する
5. `Commit changes`で確定する
6. GitHub Pagesの反映を待つ

反映後は、Search Consoleに表示された確認用URLをブラウザで開きます。ファイル内の短い確認文字列が表示されれば準備完了です。

## 確認できないとき

次を順番に確認します。

- ファイル名を変更していないか
- `.html.html`のように拡張子が重複していないか
- リポジトリ直下へ置いたか
- GitHub Pagesへ反映されたか
- 登録したプロパティURLが正しいか

GitHub上で見えるだけでは不十分です。`github.com`のファイル画面ではなく、`github.io`の公開URLで開ける必要があります。

## 確認後も削除しない

Google公式では、HTML確認ファイルを削除すると所有権を失うと説明されています。[所有権の確認方法](https://support.google.com/webmasters/answer/9008080?hl=ja)

サイトのデザインには表示されないため、確認が終わってもリポジトリに残しておきます。

## まとめ

確認ファイルは、名前と内容を変えず、公開元の一番上へ置くのが基本です。公開URLで直接開けることを確認してからSearch Consoleへ戻れば、場所の間違いを見つけやすくなります。
