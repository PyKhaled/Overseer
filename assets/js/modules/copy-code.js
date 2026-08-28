export function initCodeCopy() {
  document.querySelectorAll('[data-code-block]').forEach((block) => {
    const code = block.querySelector('code');
    if (!code || !navigator.clipboard) return;

    const button = document.createElement('button');
    button.className = 'b-code-copy';
    button.type = 'button';
    button.textContent = 'Copy';
    button.setAttribute('aria-label', 'Copy code to clipboard');

    button.addEventListener('click', async () => {
      await navigator.clipboard.writeText(code.textContent.trim());
      button.textContent = 'Copied';
      window.setTimeout(() => { button.textContent = 'Copy'; }, 1600);
    });

    block.append(button);
  });
}
