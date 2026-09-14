ワカルカモ 親子レイアウト修正版 v3

更新ファイルのみ入っています。
- scripts/generate_site.py
- assets/css/style.css
- .github/workflows/build-articles.yml

修正内容:
- 記事一覧・カテゴリページを「左=コンパクトな親記事 / 右=子記事群」に固定
- 親サムネが横幅いっぱいに巨大化しないようデスクトップでは260〜280pxに制限
- 子記事は右側に2〜3列で表示
- 700px以下のみ縦並び
- style.css にバージョン文字列を付け、古いCSSキャッシュが残りにくいよう変更
- Actionsで生成された一覧・カテゴリ等がコミットされる設定を同梱
