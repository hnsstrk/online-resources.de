// Fuse.js-based search — expects /index.json from Hugo outputs
(function () {
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');
  if (!input || !results) return;

  let fuse = null;

  async function loadIndex() {
    try {
      const res = await fetch('/index.json');
      const data = await res.json();
      // PaperMod-compatible: data is an array of { title, permalink, summary, content, date }
      fuse = new Fuse(data, {
        isCaseSensitive: false,
        shouldSort: true,
        location: 0,
        distance: 1000,
        threshold: 0.4,
        minMatchCharLength: 1,
        keys: ['title', 'permalink', 'summary', 'content']
      });
      // If there's a pre-filled query (from URL ?q=…), run it now.
      const params = new URLSearchParams(window.location.search);
      const q = params.get('q');
      if (q) { input.value = q; run(q); }
    } catch (e) {
      results.innerHTML = '<p class="meta">Index konnte nicht geladen werden.</p>';
    }
  }

  function run(query) {
    if (!fuse) return;
    if (!query || query.length < 2) { results.innerHTML = ''; return; }
    const hits = fuse.search(query).slice(0, 30);
    if (!hits.length) {
      results.innerHTML = '<p class="meta">Keine Treffer.</p>';
      return;
    }
    results.innerHTML = hits.map(({ item }) => `
      <article class="search__result">
        <a href="${item.permalink}" class="post-card__title">${item.title}</a>
        ${item.summary ? `<p class="post-card__summary">${item.summary}</p>` : ''}
      </article>
    `).join('');
  }

  input.addEventListener('input', (e) => run(e.target.value));
  loadIndex();
})();
