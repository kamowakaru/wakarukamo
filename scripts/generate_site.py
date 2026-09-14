from pathlib import Path
import hashlib, json, csv, re, html, os

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content/articles'
SITE_URL = os.environ.get('SITE_URL', 'https://kamowakaru.github.io/wakarukamo').rstrip('/')

# data/article-management.csv is the publication master.
# Only rows whose 公開済 column is 済 are emitted as public articles.
MANAGEMENT_CSV = ROOT / 'data/article-management.csv'
PUBLISHED_NOS = set()
PUBLISHED_TITLES = set()
if MANAGEMENT_CSV.exists():
    with MANAGEMENT_CSV.open(encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            if (row.get('公開済') or '').strip() == '済':
                no = (row.get('No.') or '').strip()
                title = (row.get('タイトル') or '').strip()
                if no:
                    PUBLISHED_NOS.add(no)
                if title:
                    PUBLISHED_TITLES.add(title)

THUMBNAIL_KEYWORDS = {
    'pc-windows': [
        (2, ('スクリーンショット', '画面保存', 'キャプチャ')),
        (3, ('エラー', '不具合', 'トラブル', '起動しない')),
        (4, ('wi-fi', 'wifi', 'ネットワーク', 'インターネット')),
        (5, ('ファイル', 'フォルダ', '保存', 'ストレージ')),
        (6, ('セキュリティ', 'パスワード', 'ウイルス')),
        (7, ('アップデート', '更新')),
        (8, ('ショートカット', 'キーボード')),
        (9, ('プリンター', 'デバイス')),
        (10, ('遅い', '重い', '高速化', 'パフォーマンス')),
        (1, ('設定', 'windows', 'pc')),
    ],
    'web': [
        (6, ('サイトマップ', 'sitemap')),
        (8, ('html確認', '確認ファイル', 'verification')),
        (5, ('search console', 'インデックス', '検索登録')),
        (9, ('スマホ', 'レスポンシブ', 'モバイル')),
        (10, ('お問い合わせ', 'メール', 'フォーム')),
        (7, ('アクセス解析', 'analytics', '分析')),
        (4, ('seo', '検索')),
        (3, ('github pages', '公開', 'デプロイ', 'actions')),
        (2, ('github', 'markdown', 'アップロード', 'リポジトリ')),
        (1, ('web', 'サイト', 'ブラウザ')),
    ],
    'wordpress': [
        (4, ('白い画面', 'エラー', '不具合')),
        (3, ('プラグイン',)),
        (2, ('テーマ', 'デザイン')),
        (5, ('ログイン', 'セキュリティ')),
        (6, ('seo', '検索')),
        (7, ('バックアップ',)),
        (8, ('高速化', '速度', '重い')),
        (9, ('記事', 'エディター', 'ブロック')),
        (10, ('サーバー', 'ドメイン', 'ホスティング')),
        (1, ('wordpress', 'ブログ')),
    ],
    'google-gas': [
        (2, ('googleフォーム', 'フォーム', '回答')),
        (8, ('サイト内検索', '検索キーワード', '検索語句')),
        (9, ('utm', '流入', 'xとthreads', 'sns')),
        (5, ('自由探索', 'ディメンション', '指標')),
        (6, ('測定id', '測定タグ', 'g-')),
        (7, ('リアルタイム',)),
        (4, ('ga4', 'アナリティクス', 'analytics')),
        (3, ('gas', 'apps script', '自動化')),
        (1, ('スプレッドシート', '表計算')),
        (10, ('google', '連携')),
    ],
    'ai-chatgpt': [
        (4, ('事実確認', 'ファクトチェック', '正確')),
        (5, ('aiっぽい', '自然な文章', '書き直')),
        (7, ('画像生成', '画像を作')),
        (8, ('スプレッドシート', '表計算')),
        (6, ('webサイト', 'ホームページ', 'サイトを作')),
        (3, ('seo記事', '記事を作', '記事を書く', '公開')),
        (2, ('プロンプト', '指示文')),
        (9, ('アイデア', '比較')),
        (10, ('自動化', 'ワークフロー')),
        (1, ('chatgpt', 'ai')),
    ],
    'other': [
        (1, ('プロフィール', '初投稿', 'アカウント')),
        (2, ('sns投稿文', '投稿文', '原稿')),
        (3, ('api', '料金', '有料', '課金')),
        (4, ('お問い合わせ', 'メール', '掲載依頼')),
        (6, ('サムネイル', '画像')),
        (7, ('プライバシー', '個人情報')),
        (8, ('チェックリスト', '手順')),
        (9, ('utm', '流入', '分析')),
        (10, ('著者', '運営者')),
        (5, ('ツール', '便利')),
    ],
}

def thumbnail_for(slug, category, article_no='', specified='', title='', description=''):
    """Choose a thumbnail. New articles use their management No. to share one image per group.

    Example: article_no 17 / 17-2 / 17-2-1 -> groups/17.jpg
    `thumbnail` in front matter always takes priority. Older articles without article_no
    keep the previous keyword-based selection so the current site can still build.
    """
    if specified:
        return specified.lstrip('/')

    article_no = str(article_no).strip()
    if article_no:
        if not re.fullmatch(r'\d+(?:-\d+)*', article_no):
            raise ValueError(f'不正な article_no: {article_no!r}')
        group_no = int(article_no.split('-', 1)[0])
        group_thumb = f'groups/{group_no:02d}.jpg'
        if (ROOT / 'assets/images/thumbnails' / group_thumb).exists():
            return group_thumb
        # If a newly added group does not have its dedicated image yet, keep the
        # whole group visually consistent instead of emitting a broken image.
        fallback_no = ((group_no - 1) % 10) + 1
        return f'{category}/{fallback_no:02d}.jpg'

    # Legacy fallback for existing articles that do not have article_no yet.
    for source in (title, description):
        haystack = source.casefold()
        for number, keywords in THUMBNAIL_KEYWORDS.get(category, []):
            if any(keyword.casefold() in haystack for keyword in keywords):
                return f'{category}/{number:02d}.jpg'
    number = int(hashlib.sha256(slug.encode('utf-8')).hexdigest()[:8], 16) % 10 + 1
    return f'{category}/{number:02d}.jpg'

def truth(value, default=False):
    if value is None:
        return default
    return str(value).lower() in {'1', 'true', 'yes', 'on'}

def parse_frontmatter(text):
    if not text.startswith('---'):
        raise ValueError('front matter がありません')
    parts = text.split('---', 2)
    if len(parts) < 3:
        raise ValueError('front matter が閉じていません')
    fm_lines = parts[1].strip().splitlines()
    body = parts[2].lstrip('\n')
    data, current = {}, None
    for raw in fm_lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        if re.match(r'^\s+-\s+', line) and current:
            data.setdefault(current, []).append(re.sub(r'^\s+-\s+', '', line).strip().strip('"\''))
            continue
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        key, value = key.strip(), value.strip()
        current = key
        data[key] = [] if not value else value.strip('"\'')
    return data, body

def inline(text):
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    def replace_link(match):
        label, href = match.group(1), match.group(2)
        raw_href = html.unescape(href)
        if raw_href.startswith(('https://', 'http://')):
            return f'<a href="{href}" rel="noopener" target="_blank">{label}</a>'
        # 記事同士の相対リンクや、サイト内の絶対パス・ページ内リンクを許可する。
        is_relative = (
            raw_href.startswith(('/', './', '../', '#', '?'))
            or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._~/-]*(?:[?#][^\s]*)?', raw_href)
        )
        if is_relative and ':' not in raw_href:
            return f'<a class="article-reference" href="{href}"><span>{label}</span></a>'
        return match.group(0)

    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', replace_link, text)
    return text

def _split_table_row(line):
    """Split a simple Markdown table row while respecting escaped pipes and inline code."""
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    cells, buf = [], []
    escaped = False
    in_code = False
    for ch in line:
        if escaped:
            buf.append(ch)
            escaped = False
            continue
        if ch == '\\':
            escaped = True
            buf.append(ch)
            continue
        if ch == '`':
            in_code = not in_code
            buf.append(ch)
            continue
        if ch == '|' and not in_code:
            cells.append(''.join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cells.append(''.join(buf).strip())
    return cells

def _is_table_separator(line):
    cells = _split_table_row(line)
    return bool(cells) and all(re.fullmatch(r':?-{3,}:?', c.strip()) for c in cells)

def md_to_html(md):
    lines, out, para = md.splitlines(), [], []
    in_code, code, in_ul, in_ol = False, [], False, False

    def flush_para():
        nonlocal para
        if para:
            out.append('<p>' + inline(' '.join(x.strip() for x in para)) + '</p>')
            para = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append('</ul>'); in_ul = False
        if in_ol:
            out.append('</ol>'); in_ol = False

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith('```'):
            flush_para(); close_lists()
            if not in_code:
                in_code, code = True, []
            else:
                out.append('<pre><code>' + html.escape('\n'.join(code)) + '</code></pre>')
                in_code = False
            i += 1
            continue

        if in_code:
            code.append(line)
            i += 1
            continue

        if not line.strip():
            flush_para(); close_lists()
            i += 1
            continue

        # GitHub-flavored Markdown style tables. A table is recognized only when
        # a header row is immediately followed by a valid --- separator row.
        if '|' in line and i + 1 < len(lines) and _is_table_separator(lines[i + 1]):
            headers = _split_table_row(line)
            separators = _split_table_row(lines[i + 1])
            if len(headers) == len(separators):
                flush_para(); close_lists()
                aligns = []
                for sep in separators:
                    left, right = sep.startswith(':'), sep.endswith(':')
                    aligns.append('center' if left and right else 'left' if left else 'right' if right else '')

                table = ['<div class="table-scroll"><table><thead><tr>']
                for cell, align in zip(headers, aligns):
                    attr = f' class="align-{align}"' if align else ''
                    table.append(f'<th{attr}>' + inline(cell) + '</th>')
                table.append('</tr></thead><tbody>')

                i += 2
                while i < len(lines) and lines[i].strip() and '|' in lines[i] and not lines[i].startswith('```'):
                    cells = _split_table_row(lines[i])
                    # Pad or trim malformed rows to keep valid HTML.
                    cells = (cells + [''] * len(headers))[:len(headers)]
                    table.append('<tr>')
                    for cell, align in zip(cells, aligns):
                        attr = f' class="align-{align}"' if align else ''
                        table.append(f'<td{attr}>' + inline(cell) + '</td>')
                    table.append('</tr>')
                    i += 1
                table.append('</tbody></table></div>')
                out.append(''.join(table))
                continue

        m = re.match(r'^(#{2,4})\s+(.+)$', line)
        if m:
            flush_para(); close_lists()
            level, title = len(m.group(1)), m.group(2).strip()
            anchor = re.sub(r'[^0-9A-Za-zぁ-んァ-ヶ一-龠ー]+', '-', title).strip('-') or 'section'
            out.append(f'<h{level} id="{html.escape(anchor)}">{inline(title)}</h{level}>')
            i += 1
            continue

        m = re.match(r'^[-*]\s+(.+)$', line)
        if m:
            flush_para()
            if in_ol:
                out.append('</ol>'); in_ol = False
            if not in_ul:
                out.append('<ul>'); in_ul = True
            out.append('<li>' + inline(m.group(1)) + '</li>')
            i += 1
            continue

        m = re.match(r'^\d+\.\s+(.+)$', line)
        if m:
            flush_para()
            if in_ul:
                out.append('</ul>'); in_ul = False
            if not in_ol:
                out.append('<ol>'); in_ol = True
            out.append('<li>' + inline(m.group(1)) + '</li>')
            i += 1
            continue

        if line.startswith('> '):
            flush_para(); close_lists()
            out.append('<blockquote>' + inline(line[2:]) + '</blockquote>')
            i += 1
            continue

        para.append(line)
        i += 1

    flush_para(); close_lists()
    if in_code:
        out.append('<pre><code>' + html.escape('\n'.join(code)) + '</code></pre>')
    return '\n'.join(out)

def shell(title, body, prefix='../', desc='', canonical_path='', json_ld='', noindex=False,
          og_image='', page_type='website'):
    nav = (
        f'<a href="{prefix}index.html">ホーム</a>'
        f'<a href="{prefix}index.html#categories">カテゴリ</a>'
        f'<a href="{prefix}articles.html">記事一覧</a>'
        f'<a href="{prefix}about.html">このサイトについて</a>'
    )
    canonical = SITE_URL + ('/' + canonical_path.lstrip('/') if canonical_path else '/')
    schema = f'<script type="application/ld+json">{json_ld}</script>' if json_ld else ''
    image = og_image or f'{SITE_URL}/assets/images/hero-duck.webp'
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ''
    return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{html.escape(desc)}">{robots}<link rel="canonical" href="{html.escape(canonical)}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{html.escape(canonical)}"><meta property="og:type" content="{page_type}"><meta property="og:image" content="{html.escape(image)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}"><meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="{html.escape(image)}"><title>{html.escape(title)} | ワカルカモ</title><link rel="stylesheet" href="{prefix}assets/css/style.css?v=20260914-3"><link rel="stylesheet" href="{prefix}assets/css/point.css"><link rel="stylesheet" href="{prefix}assets/css/article-markdown.css?v=20260915-table">{schema}</head><body data-root="{prefix}"><header class="site-header"><div class="container header-inner"><a class="brand" href="{prefix}index.html"><img src="{prefix}assets/images/logo-duck.webp" alt=""><span><strong>ワカルカモ</strong><small>PC・Web・AIの「わからない」が、わかるかも。</small></span></a><button class="menu-btn" aria-label="メニュー">☰</button><nav class="nav">{nav}</nav><form class="header-search" action="{prefix}search.html"><input name="q" type="search" placeholder="キーワードで検索…"><button>🔍</button></form></div></header>{body}<footer class="footer"><div class="container footer-inner"><div class="footer-brand"><img src="{prefix}assets/images/logo-duck.webp" alt=""><div><strong>ワカルカモ</strong><div style="font-size:12px;color:#6c7c91">PC・Web・AIの「わからない」が、わかるかも。</div></div></div><div class="footer-links"><a href="{prefix}index.html">ホーム</a><a href="{prefix}articles.html">記事一覧</a><a href="{prefix}about.html">このサイトについて</a><a href="{prefix}privacy.html">プライバシーポリシー</a></div></div><p class="copyright">© 2026 ワカルカモ</p></footer><script src="{prefix}assets/js/analytics-config.js"></script><script src="{prefix}assets/js/site.js?v=20260914-2"></script></body></html>'''

def static_card(article, prefix=''):
    cat = catmap[article['category']]
    chips = ''.join(
        f'<a class="tag-link" href="{prefix}tags/{t}.html">{html.escape(tagmap[t]["name"])}</a>'
        for t in article['tags']
    )
    return f'''<article class="card"><a class="thumb" href="{prefix}articles/{article['slug']}.html"><img src="{prefix}assets/images/thumbnails/{html.escape(article['thumbnail'])}" alt="{html.escape(article['title'])}のイメージ画像" loading="lazy"></a><div class="card-body"><span class="chip">{html.escape(cat['name'])}</span><h3><a href="{prefix}articles/{article['slug']}.html">{html.escape(article['title'])}</a></h3><p>{html.escape(article['description'])}</p><div class="meta">{chips}<time datetime="{article['date']}">{article['date'].replace('-', '.')}</time></div></div></article>'''

def article_no_key(article):
    no = str(article.get('article_no', '')).strip()
    if not no:
        return (9999, article.get('date', ''), article['slug'])
    try:
        parts = tuple(int(x) for x in no.split('-'))
        return parts + (-1,) * (4 - len(parts))
    except ValueError:
        return (9998, no, article['slug'])

def grouped_collection(items, prefix=''):
    numbered = [a for a in items if a.get('article_no')]
    legacy = [a for a in items if not a.get('article_no')]
    groups = {}
    for a in sorted(numbered, key=article_no_key):
        root = str(a['article_no']).split('-')[0]
        groups.setdefault(root, []).append(a)
    chunks = []
    for root in sorted(groups, key=lambda x: int(x) if x.isdigit() else 9999):
        members = groups[root]
        parent = next((a for a in members if str(a['article_no']) == root), None)
        children = [a for a in members if a is not parent]
        if parent:
            cat = catmap[parent['category']]
            child_html = ''.join(static_card(a, prefix) for a in children)
            chunks.append(f'<section class="article-group"><article class="parent-card"><a class="parent-thumb" href="{prefix}articles/{parent["slug"]}.html"><img src="{prefix}assets/images/thumbnails/{html.escape(parent["thumbnail"])}" alt="{html.escape(parent["title"])}のイメージ画像" loading="lazy"></a><div class="parent-card-body"><span class="parent-badge">まとめ記事</span><span class="chip">{html.escape(cat["name"])}</span><h2><a href="{prefix}articles/{parent["slug"]}.html">{html.escape(parent["title"])}</a></h2><p>{html.escape(parent["description"])}</p><a class="parent-link" href="{prefix}articles/{parent["slug"]}.html">このテーマをまとめて見る →</a></div></article><div class="group-children">{child_html}</div></section>')
        else:
            chunks.append('<section class="article-group"><div class="group-children">' + ''.join(static_card(a, prefix) for a in children) + '</div></section>')
    if legacy:
        chunks.append('<section class="article-group legacy-group"><h2 class="legacy-heading">その他の記事</h2><div class="group-children">' + ''.join(static_card(a, prefix) for a in legacy) + '</div></section>')
    return ''.join(chunks) or '<div class="empty-note">まだ記事がありません。</div>'

def update_grouped_collection(path, items, prefix=''):
    text = path.read_text(encoding='utf-8')
    content = '<!-- ARTICLES:START -->' + grouped_collection(items, prefix) + '<!-- ARTICLES:END -->'
    if '<!-- ARTICLES:START -->' in text:
        text = re.sub(r'<!-- ARTICLES:START -->.*?<!-- ARTICLES:END -->', content, text, flags=re.S)
    else:
        raise ValueError(f'{path}: 記事一覧の挿入場所が見つかりません')
    text = text.replace('class="list-grid" data-collection="all"', 'class="grouped-article-list" data-collection="all"')
    text = text.replace('class="list-grid" data-collection="category"', 'class="grouped-article-list" data-collection="category"')
    # Force browsers to fetch the latest hierarchy CSS after layout updates.
    text = re.sub(r'(assets/css/style\.css)(?:\?v=[^\"\']+)?', r'\1?v=20260914-hierarchy-v4', text)
    path.write_text(text, encoding='utf-8')

def update_home_parent_links(path, items):
    text = path.read_text(encoding='utf-8')
    # Rebuild these links on every run so newly published parent articles appear automatically.
    text = re.sub(r'<div class="category-card-wrap">(<a class="category-card".*?</a>)<div class="category-parent-links">.*?</div></div>', r'\1', text, flags=re.S)
    parents_by_cat = {}
    for a in sorted(items, key=article_no_key):
        no = str(a.get('article_no', ''))
        if no and '-' not in no:
            parents_by_cat.setdefault(a['category'], []).append(a)
    for cat in categories:
        parents = parents_by_cat.get(cat['slug'], [])[:3]
        if not parents:
            continue
        links = ''.join(f'<a href="articles/{a["slug"]}.html">{html.escape(a["title"].split("｜")[0])}</a>' for a in parents)
        block = f'<div class="category-parent-links"><span>まずはここから</span>{links}</div>'
        pattern = rf'(<a class="category-card" href="categories/{re.escape(cat["slug"])}\.html">.*?</a>)'
        m = re.search(pattern, text, flags=re.S)
        if m and 'category-parent-links' not in text[m.end():m.end()+100]:
            text = text[:m.start()] + f'<div class="category-card-wrap">{m.group(1)}{block}</div>' + text[m.end():]
    path.write_text(text, encoding='utf-8')

def update_collection(path, cards, marker='ARTICLES'):
    text = path.read_text(encoding='utf-8')
    content = f'<!-- {marker}:START -->' + (''.join(cards) or '<div class="empty-note">まだ記事がありません。</div>') + f'<!-- {marker}:END -->'
    if f'<!-- {marker}:START -->' in text:
        text = re.sub(rf'<!-- {re.escape(marker)}:START -->.*?<!-- {re.escape(marker)}:END -->', content, text, flags=re.S)
    else:
        text, count = re.subn(r'(<div class="(?:article-grid|list-grid)"[^>]*data-collection[^>]*>)\s*(</div>)', r'\1' + content + r'\2', text, count=1, flags=re.S)
        if count != 1:
            raise ValueError(f'{path}: 記事一覧の挿入場所が見つかりません')
    path.write_text(text, encoding='utf-8')

def update_static_seo(path, canonical_path, title, desc, noindex=False, json_ld=''):
    text = path.read_text(encoding='utf-8')
    canonical = SITE_URL + ('/' + canonical_path.lstrip('/') if canonical_path else '/')
    image = f'{SITE_URL}/assets/images/hero-duck.webp'
    block = '<!-- SEO:START -->' + ('<meta name="robots" content="noindex,follow">' if noindex else '')
    block += f'<link rel="canonical" href="{html.escape(canonical)}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{html.escape(canonical)}"><meta property="og:type" content="website"><meta property="og:image" content="{image}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}"><meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="{image}">'
    if json_ld:
        block += f'<script type="application/ld+json">{json_ld}</script>'
    block += '<!-- SEO:END -->'
    if '<!-- SEO:START -->' in text:
        text = re.sub(r'<!-- SEO:START -->.*?<!-- SEO:END -->', block, text, flags=re.S)
    else:
        text = text.replace('</head>', block + '</head>', 1)
    path.write_text(text, encoding='utf-8')

categories = json.loads((ROOT/'data/categories.json').read_text(encoding='utf-8'))
tags = json.loads((ROOT/'data/tags.json').read_text(encoding='utf-8'))
catmap = {x['slug']: x for x in categories}
tagmap = {x['slug']: x for x in tags}
all_articles, bodies = [], {}

for fp in sorted(CONTENT.glob('*.md')):
    fm, body = parse_frontmatter(fp.read_text(encoding='utf-8'))
    slug = fp.stem
    required = ['title','date','category','tags','description']
    missing = [k for k in required if k not in fm]
    if missing:
        raise ValueError(f'{fp.name}: 不足項目 {missing}')
    if fm['category'] not in catmap:
        raise ValueError(f'{fp.name}: 未登録カテゴリ {fm["category"]}')
    bad = [t for t in fm['tags'] if t not in tagmap]
    if bad:
        raise ValueError(f'{fp.name}: 未登録タグ {bad}。data/tags.json に追加してください')
    article_no = str(fm.get('article_no', '') or '').strip()
    managed_public = (article_no in PUBLISHED_NOS) if article_no else (fm['title'] in PUBLISHED_TITLES)
    article = {'slug':slug,'title':fm['title'],'date':fm['date'],'updated':fm.get('updated', fm['date']),'category':fm['category'],'tags':fm['tags'],'description':fm['description'],'article_no':article_no,'thumbnail':thumbnail_for(slug, fm['category'], article_no, fm.get('thumbnail', ''), fm['title'], fm['description']),'point':fm.get('point', ''),'draft':truth(fm.get('draft')) or not managed_public}
    all_articles.append(article)
    bodies[slug] = body
all_articles.sort(key=lambda a: (a['date'], a['slug']), reverse=True)
articles = [a for a in all_articles if not a['draft']]

# Previous/next navigation follows article_no (1, 1-1, 1-2 ... 36-x),
# which is also the easiest order for a human QA pass.
nav_articles = sorted(articles, key=article_no_key)
article_neighbors = {}
for i, item in enumerate(nav_articles):
    article_neighbors[item['slug']] = (
        nav_articles[i - 1] if i > 0 else None,
        nav_articles[i + 1] if i + 1 < len(nav_articles) else None,
    )

(ROOT/'data/articles.json').write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding='utf-8')

csv_path = ROOT/'data/analytics-pageviews.csv'
old = {}
if csv_path.exists():
    with csv_path.open(encoding='utf-8') as f:
        for row in csv.DictReader(f):
            old[row['path']] = row.get('views','0')
with csv_path.open('w', encoding='utf-8', newline='') as f:
    w = csv.writer(f); w.writerow(['path','views'])
    for a in articles:
        path = f"/articles/{a['slug']}.html"
        w.writerow([path, old.get(path,'0')])

adir = ROOT/'articles'; adir.mkdir(exist_ok=True)
for old_file in adir.glob('*.html'):
    old_file.unlink()
for a in articles:
    cat = catmap[a['category']]
    chips = ''.join(f'<a class="tag-link" href="../tags/{t}.html">{html.escape(tagmap[t]["name"])}</a>' for t in a['tags'])
    article_body = md_to_html(bodies[a['slug']])
    point = ''
    if a['point']:
        point = f'''<aside class="point yellow wakarukamo-point"><div class="point-heading"><img src="../assets/images/wakarukamo-point.png" alt=""><strong>ワカルカモポイント</strong></div><p>{html.escape(a['point'])}</p></aside>'''
    author_box = '''<section class="author-box" aria-labelledby="author-box-title"><img src="../assets/images/tip-duck.webp" alt="ワカルカモ運営者"><div><span id="author-box-title" class="author-label">この記事を書いた人</span><strong>ワカルカモ運営者</strong><p>企業の情報システム・DX推進・マーケティング業務などを経験。PC・Webサービス・業務自動化など、実際に試して分かったことを初心者向けに解説しています。</p><a href="../about.html#author-profile">運営者情報を見る →</a></div></section>'''
    prev_article, next_article = article_neighbors.get(a['slug'], (None, None))
    prev_link = ''
    next_link = ''
    if prev_article:
        prev_link = (
            f'<a class="article-pager-link article-pager-prev" href="{prev_article["slug"]}.html">'
            f'<span class="article-pager-label">← 前の記事</span>'
            f'<strong>{html.escape(prev_article["title"])}</strong></a>'
        )
    else:
        prev_link = '<span class="article-pager-link article-pager-empty" aria-hidden="true"></span>'
    if next_article:
        next_link = (
            f'<a class="article-pager-link article-pager-next" href="{next_article["slug"]}.html">'
            f'<span class="article-pager-label">次の記事 →</span>'
            f'<strong>{html.escape(next_article["title"])}</strong></a>'
        )
    else:
        next_link = '<span class="article-pager-link article-pager-empty" aria-hidden="true"></span>'
    article_pager = (
        '<nav class="article-pager" aria-label="前後の記事">'
        + prev_link + next_link +
        '</nav>'
    )
    page = f'''<main class="article-main"><div class="container article-layout"><article class="article-body"><div class="breadcrumb"><a href="../index.html">ホーム</a> › <a href="../categories/{cat['slug']}.html">{html.escape(cat['name'])}</a> › {html.escape(a['title'])}</div><div class="meta"><span class="chip">{html.escape(cat['name'])}</span>{chips}<span class="author-byline">著者：<a href="../about.html#author-profile">ワカルカモ運営者</a></span><time datetime="{a['date']}">{a['date'].replace('-','.')}</time></div><h1>{html.escape(a['title'])}</h1><p class="lead">{html.escape(a['description'])}</p><figure class="article-thumbnail"><img src="../assets/images/thumbnails/{html.escape(a['thumbnail'])}" alt="{html.escape(a['title'])}のイメージ画像"></figure>{article_body}{point}{author_box}{article_pager}<h2>関連記事</h2><div class="article-grid" data-related data-category="{a['category']}" data-slug="{a['slug']}"></div></article><aside><div class="sidebox"><img class="side-duck" src="../assets/images/tip-duck.webp" alt=""><h3>この記事のカテゴリ</h3><a class="outline-btn" href="../categories/{cat['slug']}.html">{html.escape(cat['name'])} →</a></div><div class="sidebox"><h3>🔥 人気のタグ</h3><div class="tag-cloud" data-popular-tags></div></div></aside></div></main>'''
    article_url = f'{SITE_URL}/articles/{a["slug"]}.html'
    schema = json.dumps({'@context':'https://schema.org','@graph':[
        {'@type':'Article','headline':a['title'],'description':a['description'],'datePublished':a['date'],'dateModified':a['updated'],'mainEntityOfPage':article_url,'author':{'@type':'Person','name':'ワカルカモ運営者','url':f'{SITE_URL}/about.html#author-profile'},'publisher':{'@type':'Organization','name':'ワカルカモ','url':SITE_URL},'image':f'{SITE_URL}/assets/images/thumbnails/{a["thumbnail"]}'},
        {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'ホーム','item':f'{SITE_URL}/'},{'@type':'ListItem','position':2,'name':cat['name'],'item':f'{SITE_URL}/categories/{cat["slug"]}.html'},{'@type':'ListItem','position':3,'name':a['title'],'item':article_url}]}
    ]}, ensure_ascii=False).replace('</', '<\\/')
    (adir/f"{a['slug']}.html").write_text(shell(a['title'], page, desc=a['description'], canonical_path=f'articles/{a["slug"]}.html', json_ld=schema, og_image=f'{SITE_URL}/assets/images/thumbnails/{a["thumbnail"]}', page_type='article'), encoding='utf-8')

tdir = ROOT/'tags'; tdir.mkdir(exist_ok=True)
for old_file in tdir.glob('*.html'):
    old_file.unlink()
for t in tags:
    matches = [a for a in articles if t['slug'] in a['tags']]
    cards = ''.join(static_card(a, '../') for a in matches) or '<div class="empty-note">まだ記事がありません。</div>'
    body = f'''<main><section class="page-hero"><div class="container"><div class="breadcrumb"><a href="../index.html">ホーム</a> › タグ › {html.escape(t['name'])}</div><h1>#{html.escape(t['name'])}</h1></div></section><section class="section"><div class="container"><div class="list-grid" data-collection="tag" data-key="{t['slug']}"><!-- ARTICLES:START -->{cards}<!-- ARTICLES:END --></div></div></section></main>'''
    (tdir/f"{t['slug']}.html").write_text(shell('タグ：'+t['name'], body, desc=f'{t["name"]}に関する記事一覧です。', canonical_path=f'tags/{t["slug"]}.html', noindex=len(matches) < 2), encoding='utf-8')

# JavaScript実行前にも記事リンクが見えるよう、主要一覧へ公開記事を直接書き込みます。
update_collection(ROOT/'index.html', [static_card(a) for a in articles[:6]])
update_collection(ROOT/'index.html', [static_card(a) for a in articles[:3]], marker='NEW_ARTICLES')
update_home_parent_links(ROOT/'index.html', articles)
# data/articles.json is committed by Actions, so the browser can refresh this block
# for future posts even when index.html itself is not part of the generated commit.
home_text = (ROOT/'index.html').read_text(encoding='utf-8')
home_text = home_text.replace(
    '<div class="list-grid new-articles-list">',
    '<div class="list-grid new-articles-list" data-collection="latest" data-limit="3">',
    1,
)
(ROOT/'index.html').write_text(home_text, encoding='utf-8')
update_grouped_collection(ROOT/'articles.html', articles)
for c in categories:
    matches = [a for a in articles if a['category'] == c['slug']]
    update_grouped_collection(ROOT/'categories'/f'{c["slug"]}.html', matches, '../')
    update_static_seo(ROOT/'categories'/f'{c["slug"]}.html', f'categories/{c["slug"]}.html', c['name'], f'{c["name"]}の記事一覧です。', noindex=not matches)

home_schema = json.dumps({'@context':'https://schema.org','@graph':[
    {'@type':'WebSite','name':'ワカルカモ','url':f'{SITE_URL}/','potentialAction':{'@type':'SearchAction','target':f'{SITE_URL}/search.html?q={{search_term_string}}','query-input':'required name=search_term_string'}},
    {'@type':'Organization','name':'ワカルカモ','url':f'{SITE_URL}/','logo':f'{SITE_URL}/assets/images/logo-duck.webp'}
]}, ensure_ascii=False).replace('</', '<\\/')
update_static_seo(ROOT/'index.html', '', 'ワカルカモ', 'PC・Web・AIの「わからない」が、わかるかも。', json_ld=home_schema)
update_static_seo(ROOT/'articles.html', 'articles.html', '記事一覧', 'ワカルカモの記事一覧です。')
update_static_seo(ROOT/'search.html', 'search.html', '検索', 'ワカルカモの記事を検索できます。', noindex=True)
update_static_seo(ROOT/'about.html', 'about.html', 'このサイトについて', 'ワカルカモの方針と運営者情報です。')
update_static_seo(ROOT/'privacy.html', 'privacy.html', 'プライバシーポリシー', 'ワカルカモのプライバシーポリシーです。')

sitemap_entries = [('/', ''), ('/articles.html', ''), ('/about.html', ''), ('/privacy.html', '')]
sitemap_entries += [(f'/articles/{a["slug"]}.html', a['updated']) for a in articles]
for c in categories:
    matches = [a for a in articles if a['category'] == c['slug']]
    if matches:
        sitemap_entries.append((f'/categories/{c["slug"]}.html', max(a['updated'] for a in matches)))
for t in tags:
    matches = [a for a in articles if t['slug'] in a['tags']]
    if len(matches) >= 2:
        sitemap_entries.append((f'/tags/{t["slug"]}.html', max(a['updated'] for a in matches)))
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += ''.join(f'  <url><loc>{html.escape(SITE_URL + path)}</loc>{f"<lastmod>{lastmod}</lastmod>" if lastmod else ""}</url>\n' for path, lastmod in sitemap_entries)
sitemap += '</urlset>\n'
(ROOT/'sitemap.xml').write_text(sitemap, encoding='utf-8')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n', encoding='utf-8')

# site.js itself can be cached. Add a version query to every generated/static HTML page
# so layout fixes are fetched immediately after deployment.
for html_path in ROOT.rglob('*.html'):
    text = html_path.read_text(encoding='utf-8')
    text = re.sub(r'(assets/js/site\.js)(?:\?v=[^"\']+)?', r'\1?v=20260914-2', text)
    html_path.write_text(text, encoding='utf-8')

print(f'Generated {len(articles)} published + {len(all_articles)-len(articles)} draft articles / {len(tags)} tag pages')
