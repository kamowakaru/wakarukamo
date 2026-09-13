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

def shell(title, body, prefix='../', desc='', canonical_path='', json_ld=''):
    nav = (
        f'<a href="{prefix}index.html">ホーム</a>'
        f'<a href="{prefix}index.html#categories">カテゴリ</a>'
        f'<a href="{prefix}articles.html">記事一覧</a>'
        f'<a href="{prefix}about.html">このサイトについて</a>'
    )
    canonical = SITE_URL + ('/' + canonical_path.lstrip('/') if canonical_path else '/')
    schema = f'<script type="application/ld+json">{json_ld}</script>' if json_ld else ''
    return f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{html.escape(canonical)}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{html.escape(canonical)}"><meta property="og:type" content="article"><title>{html.escape(title)} | ワカルカモ</title><link rel="stylesheet" href="{prefix}assets/css/style.css"><link rel="stylesheet" href="{prefix}assets/css/point.css">{schema}</head><body data-root="{prefix}"><header class="site-header"><div class="container header-inner"><a class="brand" href="{prefix}index.html"><img src="{prefix}assets/images/logo-duck.svg" alt=""><span><strong>ワカルカモ</strong><small>PC・Web・AIの「わからない」が、わかるかも。</small></span></a><button class="menu-btn" aria-label="メニュー">☰</button><nav class="nav">{nav}</nav><form class="header-search" action="{prefix}search.html"><input name="q" type="search" placeholder="キーワードで検索…"><button>🔍</button></form></div></header>{body}<footer class="footer"><div class="container footer-inner"><div class="footer-brand"><img src="{prefix}assets/images/logo-duck.svg" alt=""><div><strong>ワカルカモ</strong><div style="font-size:12px;color:#6c7c91">PC・Web・AIの「わからない」が、わかるかも。</div></div></div><div class="footer-links"><a href="{prefix}index.html">ホーム</a><a href="{prefix}articles.html">記事一覧</a><a href="{prefix}about.html">このサイトについて</a><a href="{prefix}privacy.html">プライバシーポリシー</a></div></div><p class="copyright">© 2026 ワカルカモ</p></footer><script src="{prefix}assets/js/analytics-config.js"></script><script src="{prefix}assets/js/site.js"></script></body></html>'''

categories = json.loads((ROOT/'data/categories.json').read_text(encoding='utf-8'))
tags = json.loads((ROOT/'data/tags.json').read_text(encoding='utf-8'))
catmap = {x['slug']: x for x in categories}
tagmap = {x['slug']: x for x in tags}
articles, bodies = [], {}

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
    article = {'slug':slug,'title':fm['title'],'date':fm['date'],'category':fm['category'],'tags':fm['tags'],'description':fm['description'],'thumbnail':thumbnail_for(slug, fm['category'], fm.get('thumbnail', '')),'point':fm.get('point', '')}
    articles.append(article)
    bodies[slug] = body
articles.sort(key=lambda a: (a['date'], a['slug']), reverse=True)
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
    page = f'''<main class="article-main"><div class="container article-layout"><article class="article-body"><div class="breadcrumb"><a href="../index.html">ホーム</a> › <a href="../categories/{cat['slug']}.html">{html.escape(cat['name'])}</a> › {html.escape(a['title'])}</div><div class="meta"><span class="chip">{html.escape(cat['name'])}</span>{chips}<time>{a['date'].replace('-','.')}</time></div><h1>{html.escape(a['title'])}</h1><p class="lead">{html.escape(a['description'])}</p><figure class="article-thumbnail"><img src="../assets/images/thumbnails/{html.escape(a['thumbnail'])}" alt="{html.escape(a['title'])}のイメージ画像"></figure>{article_body}{point}<h2>関連記事</h2><div class="article-grid" data-related data-category="{a['category']}" data-slug="{a['slug']}"></div></article><aside><div class="sidebox"><img class="side-duck" src="../assets/images/tip-duck.svg" alt=""><h3>この記事のカテゴリ</h3><a class="outline-btn" href="../categories/{cat['slug']}.html">{html.escape(cat['name'])} →</a></div><div class="sidebox"><h3>🔥 人気のタグ</h3><div class="tag-cloud" data-popular-tags></div></div></aside></div></main>'''
    article_url = f'{SITE_URL}/articles/{a["slug"]}.html'
    schema = json.dumps({
        '@context':'https://schema.org', '@type':'Article', 'headline':a['title'],
        'description':a['description'], 'datePublished':a['date'], 'dateModified':a['date'],
        'mainEntityOfPage':article_url, 'author':{'@type':'Organization','name':'ワカルカモ'},
        'publisher':{'@type':'Organization','name':'ワカルカモ'},
        'image':f'{SITE_URL}/assets/images/thumbnails/{a["thumbnail"]}'
    }, ensure_ascii=False).replace('</', '<\\/')
    (adir/f"{a['slug']}.html").write_text(shell(a['title'], page, desc=a['description'], canonical_path=f'articles/{a["slug"]}.html', json_ld=schema), encoding='utf-8')

tdir = ROOT/'tags'; tdir.mkdir(exist_ok=True)
for old_file in tdir.glob('*.html'):
    old_file.unlink()
for t in tags:
    body = f'''<main><section class="page-hero"><div class="container"><div class="breadcrumb"><a href="../index.html">ホーム</a> › タグ › {html.escape(t['name'])}</div><h1>#{html.escape(t['name'])}</h1></div></section><section class="section"><div class="container"><div class="list-grid" data-collection="tag" data-key="{t['slug']}"></div></div></section></main>'''
    (tdir/f"{t['slug']}.html").write_text(shell('タグ：'+t['name'], body, canonical_path=f'tags/{t["slug"]}.html'), encoding='utf-8')

sitemap_paths = ['/', '/articles.html', '/about.html', '/privacy.html']
sitemap_paths += [f'/articles/{a["slug"]}.html' for a in articles]
sitemap_paths += [f'/categories/{c["slug"]}.html' for c in categories]
sitemap_paths += [f'/tags/{t["slug"]}.html' for t in tags]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sitemap += ''.join(f'  <url><loc>{html.escape(SITE_URL + path)}</loc></url>\n' for path in sitemap_paths)
sitemap += '</urlset>\n'
(ROOT/'sitemap.xml').write_text(sitemap, encoding='utf-8')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n', encoding='utf-8')

print(f'Generated {len(articles)} articles / {len(tags)} tag pages')
