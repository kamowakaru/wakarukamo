(() => {
  const body = document.body;
  const root = body.dataset.root || '';

  // 一覧カードの画像と本文を別レイヤーに固定し、狭い画面でも重なりを防ぐ。
  const cardLayoutStyle = document.createElement('style');
  cardLayoutStyle.textContent = `
    .card { display:flex; min-width:0; flex-direction:column; }
    .card > .thumb {
      display:block; width:100%; height:auto; aspect-ratio:16/9;
      flex:0 0 auto; overflow:hidden; line-height:0;
    }
    .card > .thumb img {
      display:block; width:100%; height:100%; object-fit:cover;
    }
    .card > .card-body {
      position:relative; z-index:1; flex:1 1 auto;
      padding:16px; border-top:1px solid #e2eaf2; background:#fff;
    }
  `;
  document.head.appendChild(cardLayoutStyle);

  const menu = document.querySelector('.menu-btn');
  const nav = document.querySelector('.nav');
  if (menu && nav) menu.addEventListener('click', () => nav.classList.toggle('open'));

  function initAnalytics() {
    const id = window.WAKARUKAMO_GA_MEASUREMENT_ID || '';
    if (!/^G-[A-Z0-9]+$/.test(id)) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', id, { anonymize_ip: true });
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(id)}`;
    document.head.appendChild(script);
  }

  function safeSearchTerm(value) {
    const term = String(value || '').trim().replace(/\s+/g, ' ').slice(0, 80);
    if (!term || /@/.test(term) || /\d{9,}/.test(term)) return '';
    return term;
  }

  function trackSearch(term, resultCount) {
    const safe = safeSearchTerm(term);
    if (!safe || typeof window.gtag !== 'function') return;
    window.gtag('event', 'search', { search_term: safe, result_count: resultCount });
  }

  const json = async path => {
    const response = await fetch(root + path);
    if (!response.ok) throw new Error(path);
    return response.json();
  };
  const categoryName = async slug => {
    const categories = await json('data/categories.json');
    return categories.find(item => item.slug === slug)?.name || slug;
  };
  function escapeHtml(value) {
    return String(value).replace(/[&<>\"]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[char]);
  }

  async function makeCard(article) {
    const category = await categoryName(article.category);
    const tags = await json('data/tags.json');
    const chips = article.tags.map(tag => {
      const name = tags.find(item => item.slug === tag)?.name || tag;
      return `<a class="tag-link" href="${root}tags/${tag}.html">${escapeHtml(name)}</a>`;
    }).join('');
    const thumbnail = article.thumbnail || `${article.category}/01.jpg`;
    return `<article class="card"><a class="thumb" href="${root}articles/${article.slug}.html"><img src="${root}assets/images/thumbnails/${escapeHtml(thumbnail)}" alt="${escapeHtml(article.title)}のイメージ画像" loading="lazy"></a><div class="card-body"><span class="chip">${escapeHtml(category)}</span><h3><a href="${root}articles/${article.slug}.html">${escapeHtml(article.title)}</a></h3><p>${escapeHtml(article.description)}</p><div class="meta">${chips}<time>${article.date.replaceAll('-', '.')}</time></div></div></article>`;
  }

  async function renderCollection() {
    const element = document.querySelector('[data-collection]');
    if (!element) return;
    const mode = element.dataset.collection;
    const key = element.dataset.key;

    // 記事一覧とカテゴリページはPythonで親子構造を静的生成している。
    // ここで再描画すると親子レイアウトが通常カードへ戻ってしまうため触らない。
    if (mode === 'all' || mode === 'category') return;

    const articles = await json('data/articles.json');
    let filtered = articles;
    if (mode === 'category') filtered = articles.filter(article => article.category === key);
    if (mode === 'tag') filtered = articles.filter(article => article.tags.includes(key));
    if (mode === 'latest') filtered = articles.slice().sort((a, b) => b.date.localeCompare(a.date));
    const limit = parseInt(element.dataset.limit || '0', 10);
    if (limit) filtered = filtered.slice(0, limit);
    element.innerHTML = (await Promise.all(filtered.map(makeCard))).join('') || '<div class="empty-note">まだ記事がありません。</div>';
  }

  async function renderPopular() {
    const box = document.querySelector('[data-popular-tags]');
    if (!box) return;
    let popular = [];
    try { popular = await json('data/popular-tags.json'); } catch (_) {}
    if (!popular.length) {
      const [articles, tags] = await Promise.all([json('data/articles.json'), json('data/tags.json')]);
      popular = tags.map(tag => ({ slug: tag.slug, name: tag.name, score: articles.filter(article => article.tags.includes(tag.slug)).length })).sort((a, b) => b.score - a.score).slice(0, 8);
    }
    box.innerHTML = popular.slice(0, 8).map(tag => `<a href="${root}tags/${tag.slug}.html">${escapeHtml(tag.name)}</a>`).join('');
  }

  async function search() {
    const wrap = document.querySelector('[data-search-results]');
    if (!wrap) return;
    const query = new URLSearchParams(location.search).get('q')?.trim() || '';
    document.querySelector('[data-search-query]').textContent = query || 'すべて';
    const [articles, tags, categories] = await Promise.all([json('data/articles.json'), json('data/tags.json'), json('data/categories.json')]);
    const filtered = !query ? articles : articles.filter(article => {
      const category = categories.find(item => item.slug === article.category)?.name || '';
      const tagNames = article.tags.map(tag => tags.find(item => item.slug === tag)?.name || '').join(' ');
      return `${article.title} ${article.description} ${category} ${tagNames}`.toLowerCase().includes(query.toLowerCase());
    });
    wrap.innerHTML = filtered.map(article => `<a class="search-row" href="${root}articles/${article.slug}.html"><strong>${escapeHtml(article.title)}</strong><small>${escapeHtml(article.description)}</small></a>`).join('') || '<div class="empty-note">該当する記事がありません。</div>';
    trackSearch(query, filtered.length);
  }

  async function related() {
    const element = document.querySelector('[data-related]');
    if (!element) return;
    const articles = await json('data/articles.json');
    const filtered = articles.filter(article => article.category === element.dataset.category && article.slug !== element.dataset.slug).slice(0, 3);
    element.innerHTML = (await Promise.all(filtered.map(makeCard))).join('') || '<div class="empty-note">関連する記事はまだありません。</div>';
  }

  initAnalytics();
  renderCollection();
  renderPopular();
  search();
  related();
})();
