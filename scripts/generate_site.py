from pathlib import Path
import hashlib, json, csv, re, html, os

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content/articles'
SITE_URL = os.environ.get('SITE_URL', 'https://kamowakaru.github.io/wakarukamo').rstrip('/')

def thumbnail_for(slug, category, specified=''):
    """Return a stable category thumbnail unless the article specifies one."""
    if specified:
        return specified.lstrip('/')
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
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" rel="noopener" target="_blank">\1</a>', text)
    return text

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
    for line in lines:
        if line.startswith('```'):
            flush_para(); close_lists()
            if not in_code:
                in_code, code = True, []
            else:
                out.append('<pre><code>' + html.escape('\n'.join(code)) + '</code></pre>')
                in_code = False
            continue
        if in_code:
            code.append(line); continue
        if not line.strip():
            flush_para(); close_lists(); continue
        m = re.match(r'^(#{2,4})\s+(.+)$', line)
        if m:
            flush_para(); close_lists()
            level, title = len(m.group(1)), m.group(2).strip()
            anchor = re.sub(r'[^0-9A-Za-zぁ-んァ-ヶ一-龠ー]+', '-', title).strip('-') or 'section'
            out.append(f'<h{level} id="{html.escape(anchor)}">{inline(title)}</h{level}>')
            continue
        m = re.match(r'^[-*]\s+(.+)$', line)
        if m:
            flush_para()
            if in_ol:
                out.append('</ol>'); in_ol = False
            if not in_ul:
                out.append('<ul>'); in_ul = True
            out.append('<li>' + inline(m.group(1)) + '</li>')
            continue
        m = re.match(r'^\d+\.\s+(.+)$', line)
        if m:
            flush_para()
            if in_ul:
                out.append('</ul>'); in_ul = False
            if not in_ol:
                out.append('<ol>'); in_ol = True
            out.append('<li>' + inline(m.group(1)) + '</li>')
            continue
        if line.startswith('> '):
            flush_para(); close_lists()
            out.append('<blockquote>' + inline(line[2:]) + '</blockquote>')
            continue
        para.append(line)
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
    return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{html.escape(desc)}">{robots}<link rel="canonical" href="{html.escape(canonical)}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{html.escape(canonical)}"><meta property="og:type" content="{page_type}"><meta property="og:image" content="{html.escape(image)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}"><meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="{html.escape(image)}"><title>{html.escape(title)} | ワカルカモ</title><link rel="stylesheet" href="{prefix}assets/css/style.css"><link rel="stylesheet" href="{prefix}assets/css/point.css">{schema}</head><body data-root="{prefix}"><header class="site-header"><div class="container header-inner"><a class="brand" href="{prefix}index.html"><img src="{prefix}assets/images/logo-duck.webp" alt=""><span><strong>ワカルカモ</strong><small>PC・Web・AIの「わからない」が、わかるかも。</small></span></a><button class="menu-btn" aria-label="メニュー">☰</button><nav class="nav">{nav}</nav><form class="header-search" action="{prefix}search.html"><input name="q" type="search" placeholder="キーワードで検索…"><button>🔍</button></form></div></header>{body}<footer class="footer"><div class="container footer-inner"><div class="footer-brand"><img src="{prefix}assets/images/logo-duck.webp" alt=""><div><strong>ワカルカモ</strong><div style="font-size:12px;color:#6c7c91">PC・Web・AIの「わからない」が、わかるかも。</div></div></div><div class="footer-links"><a href="{prefix}index.html">ホーム</a><a href="{prefix}articles.html">記事一覧</a><a href="{prefix}about.html">このサイトについて</a><a href="{prefix}privacy.html">プライバシーポリシー</a></div></div><p class="copyright">© 2026 ワカルカモ</p></footer><script src="{prefix}assets/js/analytics-config.js"></script><script src="{prefix}assets/js/site.js"></script></body></html>'''

def static_card(article, prefix=''):
    cat = catmap[article['category']]
    chips = ''.join(
        f'<a class="tag-link" href="{prefix}tags/{t}.html">{html.escape(tagmap[t]["name"])}</a>'
        for t in article['tags']
    )
    return f'''<article class="card"><a class="thumb" href="{prefix}articles/{article['slug']}.html"><img src="{prefix}assets/images/thumbnails/{html.escape(article['thumbnail'])}" alt="{html.escape(article['title'])}のイメージ画像" loading="lazy"></a><div class="card-body"><span class="chip">{html.escape(cat['name'])}</span><h3><a href="{prefix}articles/{article['slug']}.html">{html.escape(article['title'])}</a></h3><p>{html.escape(article['description'])}</p><div class="meta">{chips}<time datetime="{article['date']}">{article['date'].replace('-', '.')}</time></div></div></article>'''

def update_collection(path, cards):
    text = path.read_text(encoding='utf-8')
    content = '<!-- ARTICLES:START -->' + (''.join(cards) or '<div class="empty-note">まだ記事がありません。</div>') + '<!-- ARTICLES:END -->'
    if '<!-- ARTICLES:START -->' in text:
        text = re.sub(r'<!-- ARTICLES:START -->.*?<!-- ARTICLES:END -->', content, text, flags=re.S)
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
    article = {'slug':slug,'title':fm['title'],'date':fm['date'],'updated':fm.get('updated', fm['date']),'category':fm['category'],'tags':fm['tags'],'description':fm['description'],'thumbnail':thumbnail_for(slug, fm['category'], fm.get('thumbnail', '')),'point':fm.get('point', ''),'draft':truth(fm.get('draft'))}
    all_articles.append(article)
    bodies[slug] = body
all_articles.sort(key=lambda a: (a['date'], a['slug']), reverse=True)
articles = [a for a in all_articles if not a['draft']]
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
    author_box = '''<section class="author-box" aria-labelledby="author-box-title"><img src="../assets/images/tip-duck.webp" alt="ワカルカモ運営者"><div><span id="author-box-title" class="author-label">この記事を書いた人</span><strong>ワカルカモ運営者</strong><p>企業の情報システム・DX推進業務を約8年経験。PC・Webサービス・業務自動化など、実際に試して分かったことを初心者向けに解説しています。</p><a href="../about.html#author-profile">運営者情報を見る →</a></div></section>'''
    page = f'''<main class="article-main"><div class="container article-layout"><article class="article-body"><div class="breadcrumb"><a href="../index.html">ホーム</a> › <a href="../categories/{cat['slug']}.html">{html.escape(cat['name'])}</a> › {html.escape(a['title'])}</div><div class="meta"><span class="chip">{html.escape(cat['name'])}</span>{chips}<span class="author-byline">著者：<a href="../about.html#author-profile">ワカルカモ運営者</a></span><time datetime="{a['date']}">{a['date'].replace('-','.')}</time></div><h1>{html.escape(a['title'])}</h1><p class="lead">{html.escape(a['description'])}</p><figure class="article-thumbnail"><img src="../assets/images/thumbnails/{html.escape(a['thumbnail'])}" alt="{html.escape(a['title'])}のイメージ画像"></figure>{article_body}{point}{author_box}<h2>関連記事</h2><div class="article-grid" data-related data-category="{a['category']}" data-slug="{a['slug']}"></div></article><aside><div class="sidebox"><img class="side-duck" src="../assets/images/tip-duck.webp" alt=""><h3>この記事のカテゴリ</h3><a class="outline-btn" href="../categories/{cat['slug']}.html">{html.escape(cat['name'])} →</a></div><div class="sidebox"><h3>🔥 人気のタグ</h3><div class="tag-cloud" data-popular-tags></div></div></aside></div></main>'''
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
update_collection(ROOT/'articles.html', [static_card(a) for a in articles])
for c in categories:
    matches = [a for a in articles if a['category'] == c['slug']]
    update_collection(ROOT/'categories'/f'{c["slug"]}.html', [static_card(a, '../') for a in matches])
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

print(f'Generated {len(articles)} published + {len(all_articles)-len(articles)} draft articles / {len(tags)} tag pages')
