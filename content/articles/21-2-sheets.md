---
title: "GASでGoogleスプレッドシートを操作する方法｜基本的な書き方を解説"
date: "2026-09-15"
article_no: "21-2"
category: "google-gas"
tags:
  - "spreadsheet"
  - "gas"
description: "GASでGoogleスプレッドシートを操作する方法について、初心者向けに具体的な手順・例・注意点を交えて解説します。"
point: "実際に確認・操作できるところまで具体的に解説します。"
---

GASからスプレッドシートを操作するときは、**スプレッドシート→シート→セル範囲（Range）**の順に対象を取得して、値を読み書きします。

## セルの値を読む

スプレッドシートに紐づいたGASなら、次のように現在のファイルとシートを取得できます。

```javascript
function readCell() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('シート1');
  const value = sheet.getRange('A1').getValue();

  console.log(value);
}
```

`getRange('A1')`でA1セルを指定し、`getValue()`で値を取得します。

## セルへ値を書く

```javascript
function writeCell() {
  const sheet = SpreadsheetApp
    .getActiveSpreadsheet()
    .getSheetByName('シート1');

  sheet.getRange('B1').setValue('確認済み');
}
```

実行するとB1へ「確認済み」と入ります。

## 複数セルをまとめて読む

A2:C10のような表をまとめて取得するなら`getValues()`を使います。

```javascript
const values = sheet.getRange('A2:C10').getValues();
```

結果は二次元配列です。大量のセルを1個ずつ`getValue()`するより、範囲をまとめて取得してJavaScript側で処理する方が効率的です。

## 書き込みもまとめられる

二次元配列を`setValues()`へ渡せば複数セルへまとめて書き込めます。配列の行数・列数は指定Rangeと一致させます。

## ワカルカモ運営でも使える考え方

記事管理表なら「1行＝1記事」にしておくと、GASで全行を配列として読み込み、記事番号や公開状態を条件にチェックしやすくなります。

[Googleスプレッドシートの使い方｜初心者向けに基本操作を解説](17-sheets.html)
