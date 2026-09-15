---
title: "GitHub DesktopでCloneする方法｜GitHubのリポジトリをPCに保存する手順"
date: "2026-09-16"
article_no: "29-7"
category: "web"
tags:
  - "website"
description: "GitHub DesktopでCloneする方法｜GitHubのリポジトリをPCに保存する手順について、初心者向けに具体的に解説します。"
point: "実際の操作や仕組みを確認しながら進めるのがポイントです。"
---

## 結論
Cloneは、GitHub上のリポジトリを**Gitの履歴ごとPCへコピー**する操作です。単なるZIPダウンロードと違い、その後Commit・Push・Pullを続けられます。

## GitHub DesktopでCloneする手順
1. GitHub Desktopを開く
2. **File → Clone repository** を開く
3. GitHub.comタブなどから対象Repositoryを選ぶ
4. **Local path**で保存先を指定する
5. **Clone**を押す

## Clone後はどこを編集する？
Local pathで指定したフォルダが作業場所です。記事や画像を追加するときは、このフォルダ内の正しい場所へ入れます。

## ZIPとの違い
ZIPはその時点のファイル一式を取得する用途には便利ですが、GitHubとの接続情報を持つ作業コピーにはなりません。継続更新するならCloneが便利です。

## まとめ
Clone後は、**PCで編集→DesktopでChanges確認→Commit→Push**が基本の流れになります。
