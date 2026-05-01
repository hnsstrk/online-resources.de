// Theme toggle — persists in localStorage, respects prefers-color-scheme
(function () {
  const KEY = 'aventurien-theme';
  const root = document.documentElement;

  function apply(theme) {
    if (theme === 'auto' || !theme) {
      root.removeAttribute('data-theme');
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      root.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    } else {
      root.setAttribute('data-theme', theme);
    }
    updateButton(theme);
  }

  function updateButton(theme) {
    const btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    const current = root.getAttribute('data-theme');
    btn.textContent = current === 'dark' ? '☼ Hell' : '☽ Dunkel';
    btn.setAttribute('aria-label', current === 'dark' ? 'Zu hellem Thema wechseln' : 'Zu dunklem Thema wechseln');
  }

  // Initial
  const stored = localStorage.getItem(KEY);
  apply(stored || 'auto');

  // React to system changes if no explicit pref
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (!localStorage.getItem(KEY)) apply('auto');
  });

  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.theme-toggle');
    if (!btn) return;
    const current = root.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem(KEY, next);
    apply(next);
  });

  // Re-check button label once DOM is ready (script may be in <head>)
  document.addEventListener('DOMContentLoaded', () => updateButton(localStorage.getItem(KEY) || 'auto'));
})();
