---
title: "GitHubで間違って上書きしたファイルを元に戻す方法｜Revertの仕組みと手順を解説"
date: "2026-09-16"
article_no: "29-11"
category: "web"
tags:
  - "website"
description: "GitHubで間違って上書きしたファイルを元に戻す方法｜Revertの仕組みと手順を解説について、初心者向けに具体的に解説します。"
point: "実際の操作や仕組みを確認しながら進めるのがポイントです。"
---

## 結論
GitHubで間違ったファイルを上書きしてCommitしてしまっても、履歴が残っていれば戻せます。共有リポジトリやGitHubへPush済みの変更なら、初心者には**過去のCommitを消すResetより、その変更を打ち消す新しいCommitを作るRevert**が扱いやすい方法です。

## Revertは「時間を巻き戻す」のではない
たとえばCommit Aの次に、間違った変更を含むCommit Bがあるとします。BをRevertすると、B自体を履歴から消すのではなく、**Bで行った変更と逆の変更をCommit Cとして追加**します。

履歴は `A → B → C（Bを打ち消す）` のように残ります。そのため「何が起きて、どう戻したか」も後から確認できます。

## GitHub Desktopで戻す手順
1. GitHub Desktopで対象Repositoryを開く
2. **Fetch origin / Pull**でGitHub側の最新状態を取得する
3. **History**タブを開く
4. 戻したい変更を行ったCommitを探す
5. Commitを右クリックする
6. **Revert Changes in Commit**を選ぶ
7. ChangesやHistoryでRevert用Commitが作られたことを確認する
8. **Push origin**でGitHubへ反映する

## 「この履歴の時点へ戻したい」とき
戻したい時点より後に悪いCommitが複数あるなら、影響関係を確認しながら**新しいCommitから古いCommitへ**Revertしていく方法があります。途中に残したい変更が混ざっている場合は、一括で全部Revertせず、対象Commitやファイルを選んで戻すほうが安全です。

## Resetとの違い
Resetはブランチが指す履歴自体を過去へ動かす用途があり、Push済み履歴を書き換えるにはForce Pushが必要になるケースがあります。共同利用や公開済み履歴では影響が大きいため、仕組みを理解せず使わないほうが安全です。

## 実際に起きた例
複数記事をGitHubのブラウザから一括アップロードしたところ、既存ルールと違うファイル名や設定が混ざり、サイト生成が失敗したことがありました。GitHub DesktopのHistoryから該当するアップロードCommitを確認し、Revertしてアップロード前の内容へ戻せました。

この経験で便利だったのは、GitHubが「現在のファイル」だけでなく**変更の履歴を持っていたこと**です。

## 戻した後に確認すること
GitHub上のファイルだけでなく、GitHub Actionsが成功したか、GitHub Pagesなど実際の公開サイトが正常かも確認します。

## まとめ
Push済みの誤変更を安全に打ち消したいなら、まずCommit履歴を特定し、**Revertで逆変更を追加→Push→動作確認**という流れを覚えておくと便利です。
