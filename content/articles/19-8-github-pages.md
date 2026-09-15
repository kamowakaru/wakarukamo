---
title: "GitHub PagesにGA4を設定する方法｜測定開始までの手順"
date: "2026-09-15"
article_no: "19-8"
category: "other"
tags:
  - "spreadsheet"
  - "github-pages"
  - "github"
description: "GitHub PagesにGA4を設定する方法について、初心者向けに具体的な手順・例・注意点を交えて解説します。"
point: "実際に確認・操作できるところまで具体的に解説します。"
---

GitHub PagesへGA4を入れるには、Googleタグを最終的な公開HTMLの`<head>`へ追加し、Pages公開後にリアルタイムで確認します。

## まず知っておきたいこと

ワカルカモはMarkdown→GitHub Actions→HTML生成→GitHub Pages公開なので、各HTMLへ手作業で貼るより、生成後の全ページへ反映される共通処理へタグを入れるのが適しています。

## 実際に確認・設定するポイント

Commit→Push→Actions→Pages公開後、本番HTMLにタグがあることを確認し、GA4のリアルタイムで受信確認して完了です。

## 迷ったときの判断

この機能だけを単独で見るのではなく、サイトの公開状態・計測設定・関連レポートも合わせて確認します。設定を変更した場合は、編集画面だけで終わらせず、実際の公開ページやレポートで期待どおりになったことまで確認しましょう。
