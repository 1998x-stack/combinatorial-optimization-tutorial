/* Progressive enhancement example: highlight a figure stage, keep ARIA state in sync. */
(() => {
  document.querySelectorAll('[data-stepper]').forEach(group => {
    const buttons = [...group.querySelectorAll('[data-stage]')];
    const items = [...group.querySelectorAll('[data-panel]')];
    function activate(stage) {
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.stage === stage)));
      items.forEach(e => { e.hidden = e.dataset.panel !== stage; });
    }
    buttons.forEach(b => b.addEventListener('click', () => activate(b.dataset.stage)));
    if (buttons.length) activate(buttons[0].dataset.stage);
  });
})();
