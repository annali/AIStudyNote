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
    const required = ['slug','title','summary','sourceTitle','sourceUrl',...headings.map((_,i)=>`section${i}`)];
    if (required.some(name=>!v(name))) { status.textContent = '欄位不能只有空白，請填寫所有必填內容。'; return; }
    let source;
    try { source = new URL(v('sourceUrl')); } catch { status.textContent = '請填入有效的 HTTPS 來源網址。'; return; }
    if (source.protocol !== 'https:' || source.hostname === 'example.com') { status.textContent = '請使用實際閱讀過的 HTTPS 來源，不可使用模板網址。'; return; }
    const existing = [...document.querySelectorAll('.manage-row a[href^="notes/"]')].some(a=>a.getAttribute('href') === `notes/${v('slug')}.html`);
    if (existing) { status.textContent = '此 slug 已存在，請使用上方修改入口或選擇新的 slug。'; return; }
    const note = {slug:v('slug'),title:v('title'),category:v('category'),summary:v('summary'),updated:v('updated'),tags,
      sections:headings.map((heading,i)=>({heading,paragraphs:v(`section${i}`).split(/\n\s*\n/).map(p=>p.trim()).filter(Boolean)})),
      sources:[{title:v('sourceTitle'),url:v('sourceUrl')}]};
    output.value = JSON.stringify(note,null,2)+'\n';
    link.href = `https://github.com/annali/AIStudyNote/new/main/content?filename=${encodeURIComponent(note.slug+'.json')}`;
    document.querySelector('#target-file').textContent = `目標檔案：content/${note.slug}.json`;
    document.querySelector('#export-panel').hidden = false;
    status.textContent = 'JSON 已產生，尚未儲存。請複製並至 GitHub 提交。';
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
