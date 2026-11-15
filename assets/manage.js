'use strict';
(() => {
  const form = document.querySelector('#note-form');
  const status = document.querySelector('#form-status');
  const output = document.querySelector('#json-output');
  const link = document.querySelector('#github-new');
  const today = new Date();
  form.elements.updated.value = `${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`;
  const headings = ['核心概念','實作範例','常見誤解','動手練習'];
  form.addEventListener('submit', event => {
    event.preventDefault();
    const v = name => form.elements[name].value.trim();
    const tags = v('tags').split(/[,，]/).map(t=>t.trim()).filter(Boolean);
    if (tags.length < 1 || tags.length > 4) { status.textContent = '請填寫 1–4 個標籤。'; return; }
    const required = ['title','summary','sourceTitle','sourceUrl',...headings.map((_,i)=>`section${i}`)];
    if (required.some(name=>!v(name))) { status.textContent = '欄位不能只有空白，請填寫所有必填內容。'; return; }
    let sourceUrl = v('sourceUrl');
    if (sourceUrl !== '../AGENTS.md') {
      if (sourceUrl.startsWith('//')) sourceUrl = 'https:' + sourceUrl;
      else if (!/^[a-z][a-z0-9+.-]*:/i.test(sourceUrl)) sourceUrl = 'https://' + sourceUrl;
      let source;
      try { source = new URL(sourceUrl); } catch { status.textContent = '這個來源網址無法辨識，請貼上完整網站地址。'; return; }
      if (!['http:','https:'].includes(source.protocol) || !source.hostname.includes('.') || source.hostname === 'example.com' || /\s/.test(source.hostname) || source.username || source.password) {
        status.textContent = '請填入實際來源的網站地址，例如 www.wikipedia.org；也可以保留原本的 http:// 或 https://。'; return;
      }
      sourceUrl = source.href;
    }
    const base = (v('slug') || v('title')).normalize('NFKC').toLocaleLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-+|-+$/g, '') || `note-${Date.now()}`;
    const used = new Set([...document.querySelectorAll('.manage-row a[href^="notes/"]')].map(a=>decodeURIComponent(a.getAttribute('href').slice(6,-5))));
    let slug = base;
    for (let suffix=2; used.has(slug); suffix++) slug = `${base}-${suffix}`;
    const note = {slug,title:v('title'),category:v('category'),summary:v('summary'),updated:v('updated'),tags,
      sections:headings.map((heading,i)=>({heading,paragraphs:v(`section${i}`).split(/\n\s*\n/).map(p=>p.trim()).filter(Boolean)})),
      sources:[{title:v('sourceTitle'),url:sourceUrl}]};
    output.value = JSON.stringify(note,null,2)+'\n';
    link.href = `https://github.com/annali/AIStudyNote/new/main/content?filename=${encodeURIComponent(note.slug+'.json')}`;
    document.querySelector('#target-file').textContent = `目標檔案：content/${note.slug}.json`;
    document.querySelector('#export-panel').hidden = false;
    status.textContent = `JSON 已產生，網址名稱為「${slug}」，來源網址已整理。尚未儲存，請複製並至 GitHub 提交。`;
  });
  form.addEventListener('input', () => {
    if (!document.querySelector('#export-panel').hidden) {
      document.querySelector('#export-panel').hidden = true;
      status.textContent = '內容已變更，請重新產生 JSON。';
    }
  });
  document.querySelector('#copy-open').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(output.value);
      status.textContent = 'JSON 已複製。請到 GitHub 新檔案貼上並提交；目前尚未儲存。';
      // Use the visible link after async clipboard completion to avoid blocked popups.
      link.textContent = 'JSON 已複製，點此到 GitHub 貼上並提交 ↗';
      link.focus();
    } catch {
      output.focus(); output.select();
      status.textContent = '瀏覽器未允許自動複製，請手動複製選取的 JSON，再點 GitHub 新增連結。';
    }
  });
})();
