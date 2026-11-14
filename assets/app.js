'use strict';
(() => {
  const input = document.querySelector('#search');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.note-card')];
  const count = document.querySelector('#result-count');
  let category = '全部';
  const texts = new Map(cards.map(card => [card, card.textContent.toLocaleLowerCase()]));
  function update() {
    const terms = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    cards.forEach(card => {
      const match = (category === '全部' || card.dataset.category === category) && terms.every(t => texts.get(card).includes(t));
      card.hidden = !match;
      if (match) visible++;
    });
    count.textContent = `共 ${visible} 篇筆記`;
    document.querySelector('#empty').hidden = visible !== 0;
    buttons.forEach(b => {
      b.classList.toggle('selected', b.dataset.filter === category);
      b.setAttribute('aria-pressed', String(b.dataset.filter === category));
    });
  }
  input.addEventListener('input', update);
  buttons.forEach(b => b.addEventListener('click', () => { category = b.dataset.filter; update(); }));
  document.querySelector('#reset').addEventListener('click', () => { category = '全部'; input.value = ''; update(); input.focus(); });
  fetch('search-index.json').then(r => { if (!r.ok) throw new Error('search index'); return r.json(); }).then(index => {
    const bySlug = new Map(index.map(n => [n.slug, n.text.toLocaleLowerCase()]));
    cards.forEach(card => {
      const slug = card.getAttribute('href').split('/').pop().replace(/\.html$/, '');
      texts.set(card, bySlug.get(slug) || texts.get(card));
    });
    update();
  }).catch(() => {
    input.placeholder = '搜尋標題、摘要或標籤…';
    update();
  });
})();
