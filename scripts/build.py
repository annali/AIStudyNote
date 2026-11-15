"""Validate and generate a portable notebook with Python standard library."""
import json, re, shutil
from datetime import date
from html import escape as e
from pathlib import Path
from urllib.parse import urlsplit
from manage import render as render_manage
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
CATEGORIES = ['提示設計', '知識檢索', 'AI 協作']
HEADINGS = ['核心概念', '實作範例', '常見誤解', '動手練習']

def validate(path):
    n = json.loads(path.read_text())
    def check(ok, msg):
        if not ok: raise ValueError(f'{path.name}: {msg}')
    for k in ['slug','title','category','summary','updated']:
        check(isinstance(n.get(k),str) and n[k].strip(), f'{k} 必須是非空字串')
    check(re.fullmatch(r'[^\W_]+(?:-[^\W_]+)*',n['slug']), 'slug 格式錯誤')
    check(path.stem == n['slug'], '檔名必須等於 slug')
    check(n['category'] in CATEGORIES, '無效分類')
    check(re.fullmatch(r'\d{4}-\d{2}-\d{2}', n['updated']), '日期格式錯誤')
    date.fromisoformat(n['updated'])
    check(isinstance(n.get('tags'),list) and 1 <= len(n['tags']) <= 4, '需要 1–4 個標籤')
    check(all(isinstance(t,str) and t.strip() for t in n['tags']), '標籤不得為空')
    check(isinstance(n.get('sections'),list) and len(n['sections']) == 4, '需要四個章節')
    for s,h in zip(n['sections'],HEADINGS):
        check(isinstance(s,dict) and s.get('heading') == h, f'需要章節 {h}')
        ps=s.get('paragraphs')
        check(isinstance(ps,list) and ps and all(isinstance(p,str) and p.strip() for p in ps),'段落不得為空')
    check(isinstance(n.get('sources'),list) and n['sources'], '需要參考來源')
    for s in n['sources']:
        check(isinstance(s,dict) and all(isinstance(s.get(k),str) and s[k].strip() for k in ['title','url']), '來源需要標題與網址')
        u=urlsplit(s['url'])
        check((u.scheme in ('http', 'https') and u.netloc and u.hostname != 'example.com') or s['url'] == '../AGENTS.md', '無效來源網址或模板網址未替換')
    return n

def shell(title,body,p='./',active='筆記總覽',desc='AI 學習筆記庫，將每次理解整理成可累積的知識。'):
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(desc,quote=True)}"><meta name="theme-color" content="#183e36"><title>{e(title)} · AI 學習筆記庫</title><link rel="stylesheet" href="{p}assets/style.css"></head><body><a class="skip" href="#main">跳至主要內容</a><div class="layout"><aside class="sidebar"><a class="brand" href="{p}index.html"><span class="brand-icon">a<span>i</span>.</span><span>AI 學習筆記庫<small>THE LEARNING NOTEBOOK</small></span></a><p class="side-label">我的知識空間</p><nav aria-label="主要導覽"><a class="nav-item {'active' if active=='筆記總覽' else ''}" href="{p}index.html"><span aria-hidden="true">▦</span> 筆記總覽 <span class="nav-arrow">↗</span></a><a class="nav-item {'active' if active=='專案規則' else ''}" href="{p}rules.html"><span aria-hidden="true">≡</span> 專案規則</a><a class="nav-item {'active' if active=='內容管理' else ''}" href="{p}manage.html"><span aria-hidden="true">＋</span> 內容管理</a></nav><div class="side-note"><span class="tiny-dot"></span> 持續累積，慢慢理解<p>把今天學會的一點，<br>變成明天用得上的知識。</p></div><div class="side-foot">BUILT WITH CLEAR RULES<br><a href="{p}AGENTS.md">閱讀 AGENTS.md ↗</a></div></aside><div class="workspace"><header class="topbar"><span>學習空間 <span class="slash">/</span> {active}</span><span class="edition">PERSONAL KNOWLEDGE BASE <span class="avatar">學</span></span></header><main id="main">{body}</main><footer><span>AI 學習筆記庫</span><span>每一份筆記，都是下一次理解的起點。</span><a href="{p}rules.html">內容與協作規則 ↗</a></footer></div></div></body></html>'''

def card(n,i):
    tags=''.join('<span># '+e(t)+'</span>' for t in n['tags'])
    return f'''<a class="note-card" href="notes/{n['slug']}.html" data-category="{e(n['category'])}"><div class="card-meta"><span class="category">{e(n['category'])}</span><span class="note-no">NOTE / {i:02d}</span></div><h3>{e(n['title'])}</h3><p>{e(n['summary'])}</p><div class="tags">{tags}</div><div class="card-bottom"><span>更新 {n['updated'].replace('-','.')}</span><span class="circle-arrow" aria-hidden="true">↗</span></div></a>'''

def build():
    notes=sorted([validate(p) for p in (ROOT/'content').glob('*.json')],key=lambda n:(n['updated'],n['slug']),reverse=True)
    if not notes: raise ValueError('至少需要一篇筆記')
    if len({n['slug'] for n in notes}) != len(notes): raise ValueError('slug 重複')
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT/'notes').mkdir(parents=True)
    shutil.copytree(ROOT/'assets',OUT/'assets')
    shutil.copy(ROOT/'AGENTS.md',OUT/'AGENTS.md')
    count=len(notes)
    filters=''.join(f'<button class="filter" data-filter="{c}" aria-pressed="false">{c}</button>' for c in CATEGORIES)
    cards=''.join(card(n,i) for i,n in enumerate(notes,1))
    body=f'''<section class="hero"><div><p class="eyebrow"><span class="tiny-dot"></span> LEARN · CONNECT · GROW</p><h1>把 AI 學習，<br>整理成自己的<span class="accent">知識。</span></h1><p class="hero-copy">從一個概念開始，留下理解、範例與練習。<br>讓每一次學習，都能接著上一次繼續。</p><a class="primary-button" href="#library">探索我的筆記 <span aria-hidden="true">↓</span></a></div><div class="notebook-art" aria-hidden="true"><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><div class="art-sheet"><div class="sheet-top">FIELD NOTES <span>01 — ∞</span></div><div class="art-title">A little more<br>understanding,<br><em>every day.</em></div><div class="art-line"></div><div class="art-lines"></div><div class="art-stamp">學<br>習</div></div><span class="floating-label">ideas → knowledge</span><span class="art-plus">+</span></div></section><div class="stats"><span><strong>{count:02d}</strong> 篇學習筆記</span><span><strong>{len(set(n['category'] for n in notes)):02d}</strong> 個主題分類</span><span class="stats-end"><span class="tiny-dot"></span> 有來源，也有自己的理解</span></div><section id="library" class="library"><div class="section-heading"><div><p class="eyebrow">THE NOTE COLLECTION</p><h2>知識，從這裡累積</h2></div><div class="search-wrap"><label class="sr-only" for="search">搜尋筆記</label><span aria-hidden="true">⌕</span><input id="search" type="search" placeholder="搜尋標題、內容或標籤…" autocomplete="off"></div></div><div class="filter-row"><div class="filters" role="group" aria-label="筆記分類"><button class="filter selected" data-filter="全部" aria-pressed="true">全部筆記 <span>{count}</span></button>{filters}</div><span id="result-count" class="result-count" role="status" aria-live="polite">共 {count} 篇筆記</span></div><div id="note-grid" class="note-grid">{cards}</div><div id="empty" class="empty" hidden><h3>還沒找到這份筆記</h3><p>試試其他關鍵字，或切換到全部筆記。</p><button id="reset" class="primary-button">清除搜尋與篩選</button></div></section><section class="rules-banner"><span class="banner-icon" aria-hidden="true">↳</span><div><p class="eyebrow">A NOTEBOOK THAT GROWS WITH YOU</p><h2>好規則，讓下一篇筆記更容易。</h2><p>共用一份內容模板，讓 AI 依照相同方式繼續整理、建立與驗證。</p></div><a href="rules.html">看看專案規則 ↗</a></section><script src="assets/app.js" defer></script>'''
    (OUT/'index.html').write_text(shell('筆記總覽',body))
    for n in notes:
        sections=''.join(f'<section id="s{i}"><h2><span>{i:02d}</span>{e(s["heading"])}</h2>'+''.join(f'<p>{e(p)}</p>' for p in s['paragraphs'])+'</section>' for i,s in enumerate(n['sections'],1))
        sources=''.join(f'<li><a href="{e(s["url"],quote=True)}">{e(s["title"])} ↗</a></li>' for s in n['sources'])
        toc=''.join(f'<a href="#s{i}">{i:02d} {s["heading"]}</a>' for i,s in enumerate(n['sections'],1))
        body=f'''<div class="article-header"><a class="back" href="../index.html">← 返回筆記總覽</a><p class="eyebrow">{e(n['category'])} / LEARNING NOTE</p><h1>{e(n['title'])}</h1><p class="article-summary">{e(n['summary'])}</p><div class="article-meta">更新於 {n['updated']} · AI 輔助整理，附參考來源</div></div><div class="article-layout"><article class="article-body">{sections}<section class="sources"><h2>參考來源</h2><ul>{sources}</ul><p class="source-note">外部來源核對日期：{n['updated']}。範例與練習為本站教學設計；本文非官方翻譯。</p></section><a class="back" href="../index.html">← 繼續探索其他筆記</a></article><nav class="toc" aria-label="文章目錄"><p class="eyebrow">這篇筆記</p>{toc}</nav></div>'''
        (OUT/'notes'/(n['slug']+'.html')).write_text(shell(n['title'],body,'../',desc=n['summary']))
    rules='''<div class="article-header"><p class="eyebrow">THE WAY WE BUILD</p><h1>讓 AI 知道，<br>下一篇該怎麼繼續。</h1><p class="article-summary">網站是一份成果；專案規則讓成果能夠持續累積。</p></div><article class="article-body rules-body"><section><h2><span>01</span>先有規則，再有內容</h2><p>AGENTS.md 分為 12 個部分，說明讀者與學習目標、分類判斷、四個章節的品質標準、合格與不合格範例、來源核對、例外處理及逐項驗收。AI 不只知道檔案放哪裡，也知道如何判斷內容是否完成。</p><a class="primary-button" href="https://github.com/annali/AIStudyNote/blob/main/AGENTS.md">閱讀完整 AGENTS.md ↗</a></section><section><h2><span>02</span>一篇檔案，就是一篇新筆記</h2><p>複製 templates/note.json 到 content/，填入標題、摘要、分類、標籤、日期、四個章節與參考來源。固定章節為：核心概念、實作範例、常見誤解、動手練習。</p><pre><code>content/few-shot-prompting.json
+ python3 scripts/build.py
→ notes/few-shot-prompting.html
→ 自動更新首頁與搜尋索引</code></pre></section><section><h2><span>03</span>把模糊要求，變成可檢查的步驟</h2><p>建置器會檢查檔名、slug、日期、分類、標籤、章節與來源格式。內容以純文字輸出，樣式共用；一般新增文章不需要修改 HTML 或 CSS。</p><p>自動驗證格式後，仍要人工核對資料來源與閱讀體驗，確認搜尋、分類及手機畫面能正常使用。</p></section><section><h2><span>04</span>下次，可以這樣請 AI 幫忙</h2><blockquote>請先閱讀 AGENTS.md，依照模板新增「少樣本提示」筆記，分類為提示設計。核對官方來源，包含四個固定章節，執行建置後說明檢查結果。</blockquote><p>同一套方式可以持續新增主題，也能維持一致的風格、來源品質與內容結構。</p><p>已實際依規則新增第五篇「少樣本提示」筆記。你也可以使用<a href="manage.html">內容管理頁</a>新增、修改與刪除筆記；登入 GitHub 提交後，自動更新正式 GitHub Pages 網站。</p><a class="primary-button" href="extension-demo.html">查看實際擴充紀錄 ↗</a></section></article>'''
    (OUT/'manage.html').write_text(shell('內容管理',render_manage(notes, HEADINGS, CATEGORIES),active='內容管理'))
    (OUT/'rules.html').write_text(shell('專案規則',rules,active='專案規則'))
    (OUT/'search-index.json').write_text(json.dumps([{'slug':n['slug'],'text':' '.join([n['title'],n['summary'],*n['tags'],*[p for s in n['sections'] for p in s['paragraphs']]])} for n in notes],ensure_ascii=False))
    demo = (ROOT/'docs/extension-demo.md').read_text()
    demo_link = '<a class="primary-button" href="notes/few-shot-prompting.html">閱讀新增的筆記 ↗</a>' if any(n['slug'] == 'few-shot-prompting' for n in notes) else '<p>這份紀錄中的示範文章目前已移除，請參考 GitHub 歷史版本。</p>'
    (OUT/'extension-demo.html').write_text(shell('實際擴充紀錄','<div class="article-header"><p class="eyebrow">FROM RULES TO A REAL PAGE</p><h1>第五篇筆記，如何長出來？</h1></div><article class="article-body rules-body"><pre class="demo-record">'+e(demo)+'</pre>'+demo_link+'</article>',active='專案規則'))
    (OUT/'.nojekyll').touch()
    print(f'建置成功：{count} 篇筆記、首頁、規則頁、搜尋索引 → {OUT}')
if __name__ == '__main__': build()
