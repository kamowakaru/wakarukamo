---
title: "Netlifyとは？GitHub Pagesとの違い・無料でWebサイトを公開する方法"
date: "2026-09-16"
article_no: "7-6"
category: "web"
tags:
  - "website"
description: "Netlifyは、Webサイトやフロントエンドをビルド・公開できるホスティングサービスです。GitHubなどのリポジトリと接続すると、pushに合わせて自動でビルド・デプロイできます。GitHub Pagesも静的サイトを公開できますが、Netlifyはデプロイ設定やプレビューなどWeb開発向けの機能をまとめて使いたい場合に向いています。"
point: "タイトルの疑問に先に答え、必要な手順・違い・注意点だけを具体的に解説します。"
---

Netlifyは、**HTML/CSS/JavaScriptや各種フロントエンドプロジェクトをインターネットへ公開するためのサービス**です。GitHubなどのリポジトリを接続しておけば、コードをpushしたときにビルドと公開を自動実行できます。

## GitHub Pagesとの違い

どちらも静的なWebサイトを公開できますが、考え方が少し違います。

|  | Netlify | GitHub Pages |
| --- | --- | --- |
| 主な用途 | Webプロジェクトのビルド・デプロイ | GitHubリポジトリから静的サイト公開 |
| Git連携 | GitHub等を接続して自動デプロイ | GitHub上のブランチまたはActions |
| ビルド | フレームワークを検出して設定可能 | JekyllまたはActionsで独自ビルド |
| 独自ドメイン | 対応 | 対応 |

単純なHTML/CSSをGitHubで管理して公開するだけならGitHub Pagesでも十分です。フレームワークのビルドやデプロイ環境をNetlify側でまとめて扱いたいならNetlifyが候補になります。

## GitHubのリポジトリからNetlifyへ公開する手順

1. Netlifyのアカウントを作成してログインします。
2. ダッシュボードで **Add new project → Import an existing project** を選びます。
3. GitHubなど利用するGitプロバイダーを選び、アクセスを許可します。
4. 公開したいリポジトリを選びます。
5. Build commandやPublish directoryなどを確認します。フレームワークによってはNetlifyが既定値を検出します。
6. **Publish** してデプロイします。
7. 発行されたNetlifyのURLを開き、サイトが表示されることを確認します。

接続後は、対象ブランチへpushすると新しいデプロイが作られる構成にできます。

## Gitを使わずに公開する方法もある

Netlifyはファイルから始める公開方法も用意しています。完成済みのHTML/CSSサイトをまずWeb上で確認したい場合にはこちらの方が手軽なこともあります。

## どちらを選べばいい？

「GitHubに置いた静的サイトをシンプルに公開したい」なら[GitHub Pages](../articles/8-github-pages.html)から検討すると分かりやすいです。「Git連携に加えてビルドやデプロイの機能を使いたい」ならNetlifyが候補です。

料金・無料枠・利用上限は変更されることがあるため、実際に使う時点でNetlifyの公式料金ページも確認してください。
