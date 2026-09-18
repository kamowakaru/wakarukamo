ワカルカモ 親子レイアウト修正版 v4

変更点
- 記事一覧とカテゴリページは同じ grouped_collection() を使用
- 親記事を「巨大カード」ではなく、横長のコンパクトなグループ見出しカードに変更
- 親サムネはPCで180×112pxに固定
- 子記事は親の下に3列（中幅2列・スマホ1列）
- 記事一覧/カテゴリページのCSS URLにバージョンを自動付与し、古いCSSキャッシュを回避

差し替えファイル
- scripts/generate_site.py
- assets/css/style.css

GitHubへ上書きPush後、Actionsの生成で articles.html と categories/*.html に反映されます。
