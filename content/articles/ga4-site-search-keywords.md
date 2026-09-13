---
title: "GA4でサイト内検索キーワードを収集する方法"
date: "2026-09-14"
category: "google-gas"
tags:
  - ga4
  - analytics
  - website
description: "サイトの検索窓で入力された語句をGA4のview_search_resultsとsearch_termで収集する仕組みを解説します。"
point: "検索結果URLにqなどの検索パラメータが付けば、GA4の拡張計測機能でサイト内検索を取得できます。"
---

## 結論

GA4では、検索結果ページのURLに検索語がクエリパラメータとして付くサイトなら、拡張計測機能でサイト内検索を収集できます。

たとえばワカルカモでは、検索結果URLが次の形になります。

```text
search.html?q=ChatGPT
```

このページが表示されると、GA4は`view_search_results`イベントを記録し、`search_term`へ`ChatGPT`を入れます。

## サイト内検索を集める目的

検索窓へ入力された語句には、訪問者がサイト内で見つけられなかった情報や、次に知りたい内容が表れます。

- 検索結果が0件だった語句を記事候補にする
- 表記違いをタグへ追加する
- よく検索される記事を見つけやすくする
- 記事タイトルと読者の言葉のずれを確認する

単なるアクセス数だけでなく、次に作るコンテンツを決める材料になります。

## 1．検索結果URLを確認する

サイトの検索窓で言葉を入力し、検索後のURLを見ます。

```text
?q=検索語
?s=検索語
?search=検索語
```

GA4は一般的な検索パラメータを使ってサイト内検索を検知します。独自の名前を使う場合は、ウェブデータストリームの拡張計測機能からサイト内検索の詳細設定を確認します。

## HTML側で必要な作業

GA4の管理画面を設定するだけでは、検索窓のないサイトで検索語句は集まりません。HTML側では、検索語をURLの`q`パラメータへ入れて検索結果ページを開く仕組みを作ります。

ワカルカモでは、次の3か所を用意しています。

1. 各ページに検索フォームを置く
2. `search.html`に検索結果の表示場所を置く
3. JavaScriptでURLから検索語を読み、記事を絞り込む

### 1．検索フォームをHTMLへ追加する

トップページなど、リポジトリ直下にあるHTMLには次のフォームを置きます。

```html
<form class="header-search" action="search.html" method="get">
  <input
    name="q"
    type="search"
    placeholder="キーワードで検索…"
    aria-label="サイト内検索"
  >
  <button type="submit">検索</button>
</form>
```

重要なのは、入力欄の`name="q"`です。フォームを送信すると、ブラウザが入力内容を次のようなURLに変換します。

```text
search.html?q=ChatGPT
```

`q`はGA4が標準で認識するサイト内検索用のパラメータです。検索フォームが記事ページなど1階層下のHTMLにある場合は、検索結果ページへ戻れるように`action="../search.html"`とします。

### 2．検索結果ページを作る

リポジトリ直下に`search.html`を作り、検索語と結果一覧を表示する場所を用意します。

```html
<main>
  <h1>検索結果</h1>
  <p>「<strong data-search-query></strong>」の検索結果</p>
  <div class="search-results" data-search-results></div>
</main>

<script src="assets/js/analytics-config.js"></script>
<script src="assets/js/site.js"></script>
```

`data-search-query`には検索された言葉を表示し、`data-search-results`には該当記事をJavaScriptで並べます。GA4の読み込み処理を含む`site.js`は、HTMLの最後で読み込みます。

### 3．JavaScriptで検索語を取得する

`assets/js/site.js`では、URLの`q`から検索語を取り出します。

```javascript
const params = new URLSearchParams(window.location.search);
const query = params.get('q')?.trim() || '';

document.querySelector('[data-search-query]').textContent =
  query || 'すべて';
```

その後、記事一覧データを読み込み、タイトルや説明文に検索語が含まれる記事だけを残します。

```javascript
const response = await fetch('data/articles.json');
const articles = await response.json();

const filtered = !query
  ? articles
  : articles.filter(article =>
      `${article.title} ${article.description}`
        .toLowerCase()
        .includes(query.toLowerCase())
    );
```

検索結果の表示方法はサイトごとに異なります。GA4で検索語を集めるうえで重要なのは、検索結果を表示するときのURLが`search.html?q=検索語`になっていることです。

### 4．GA4タグを読み込む

すべてのページでGA4タグが読み込まれ、検索結果ページでも`page_view`が送信される状態にします。ワカルカモでは、測定IDを`assets/js/analytics-config.js`へ保存し、`site.js`からGoogleタグを読み込んでいます。

```javascript
window.WAKARUKAMO_GA_MEASUREMENT_ID = 'G-XXXXXXXXXX';
```

測定IDは自分のGA4プロパティに表示される`G-`から始まる値へ置き換えます。公開記事へ自分の測定IDを例として載せる必要はありません。

## 2．拡張計測機能を確認する

GA4の`管理 → データストリーム`から対象ウェブストリームを開き、拡張計測機能のサイト内検索が有効か確認します。

Google公式によると、`view_search_results`は検索結果ページのURLに`q`などのクエリパラメータがあるときに記録され、`search_term`が送信されます。拡張計測機能を使うだけなら、`view_search_results`を送るJavaScriptを自分で書く必要はありません。[拡張計測機能イベント](https://support.google.com/analytics/answer/9216061?hl=ja)

## 3．リアルタイムでテストする

公開サイトの検索窓から、個人情報を含まないテスト語を検索します。その後、GA4のリアルタイムで`view_search_results`が出るか確認します。

ワカルカモでは、メールアドレスらしい文字列や長い数字列を独自イベントの対象外にしています。ただし、検索欄自体へ個人情報を入力しない案内も必要です。

## 推奨イベントのsearchも送る場合

GA4には、自動取得される`view_search_results`とは別に、手動で送信できる推奨イベント`search`があります。検索結果件数なども一緒に記録したい場合に使えます。

ワカルカモでは、検索結果を画面へ表示したあとに次の処理を実行しています。

```javascript
gtag('event', 'search', {
  search_term: query,
  result_count: filtered.length
});
```

`search_term`は検索語、`result_count`は該当した記事数です。Google公式の`search`推奨イベントでは`search_term`が必須パラメータとして案内されています。[GA4の推奨イベント](https://developers.google.com/analytics/devguides/collection/ga4/reference/events?hl=ja#search)

なお、`result_count`はワカルカモ独自のパラメータです。GA4の通常レポートで使う場合は、別途カスタム指標の登録が必要です。検索ニーズの把握だけなら、まずは自動取得される`view_search_results`と`search_term`だけでも十分です。

ただし、拡張計測機能の`view_search_results`と両方を送ると、一回の検索に二つのイベントが記録されます。集計ではイベント名を指定し、二重に数えないようにします。

### 個人情報らしい文字列を送らないようにする例

検索窓へメールアドレスや長い番号が入力される可能性もあります。ワカルカモでは、送信前に文字数を制限し、`@`を含む文字列や9桁以上の連続した数字を除外しています。

```javascript
function safeSearchTerm(value) {
  const term = String(value || '')
    .trim()
    .replace(/\s+/g, ' ')
    .slice(0, 80);

  if (!term || /@/.test(term) || /\d{9,}/.test(term)) return '';
  return term;
}
```

これはすべての個人情報を完全に判定する仕組みではありませんが、明らかなメールアドレスや長い番号を送信しにくくできます。

## 収集後の見方

検索語を一覧で見るには、GA4の自由探索を使います。行へ検索語句、値へイベント数、フィルタへ`view_search_results`を設定します。

詳しい画面設定は、[GA4の自由探索でサイト内検索語句を見る方法](ga4-free-form-exploration.html)で説明しています。

## まとめ

HTML側では、`name="q"`の検索フォーム、`search.html`、検索結果を作るJavaScript、GA4タグの4つを用意します。そのうえで、GA4側の拡張計測機能とリアルタイムイベントを確認します。

検索語は訪問者のニーズそのものです。まずは`view_search_results`と`search_term`を収集し、0件検索や頻出語を次の記事作りへ活用しましょう。
