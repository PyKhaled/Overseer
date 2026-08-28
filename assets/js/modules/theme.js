const THEME_KEY = 'overseer-theme';

export function initTheme() {
  const toggle = document.querySelector('[data-theme-toggle]');
  if (!toggle) return;

  const updateLabel = () => {
    const isLight = document.documentElement.dataset.theme === 'light';
    toggle.setAttribute('aria-label', `Switch to ${isLight ? 'dark' : 'light'} theme`);
    toggle.querySelector('[data-theme-icon]').textContent = isLight ? '☾' : '☀';
  };

  updateLabel();

  toggle.addEventListener('click', () => {
    const nextTheme = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = nextTheme;
    localStorage.setItem(THEME_KEY, nextTheme);
    updateLabel();
  });
}
