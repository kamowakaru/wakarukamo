---
title: "Search ConsoleのHTML確認ファイルをGitHub Pagesへ置く方法"
date: "2026-09-15"
article_no: "20-1-1"
category: "other"
tags:
  - "spreadsheet"
  - "github-pages"
  - "github"
description: "Search ConsoleのHTML確認ファイルをGitHub Pagesへ置く方法について、初心者向けに具体的な手順・例・注意点を交えて解説します。"
point: "実際に確認・操作できるところまで具体的に解説します。"
---

HTML確認ファイルは、Googleから受け取ったファイル名・中身を変えず、GitHub Pagesの指定公開URLから直接開ける位置へ置きます。

## まず知っておきたいこと

GitHub Actionsで公開物を生成する場合、リポジトリに置くだけでなく最終公開物へ含まれる必要があります。

## 実際に確認・設定するポイント

Commit→Push→Pages公開後、確認URLをブラウザで開き、Googleの確認文字列が表示された状態でSearch Consoleの「確認」を押します。ファイルは後で消しません。

## 迷ったときの判断

この機能だけを単独で見るのではなく、サイトの公開状態・計測設定・関連レポートも合わせて確認します。設定を変更した場合は、編集画面だけで終わらせず、実際の公開ページやレポートで期待どおりになったことまで確認しましょう。
