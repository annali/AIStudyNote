實際擴充紀錄｜2026-11-14

目的
驗證 AI 能依 AGENTS.md 新增內容，沿用共用版型，並透過 GitHub 提交發布。

使用指令
「請依照 AGENTS.md 與 templates/note.json，新增一篇介紹少樣本提示的初學者筆記，slug 為 few-shot-prompting，分類為提示設計。先核對官方來源，填入四個固定章節，最後執行建置，報告修改檔案及驗證結果。」

這次實際做了什麼
1. 閱讀 AGENTS.md、模板與既有提示設計筆記。
2. 閱讀 Meta 官方 Prompt engineering 的 Zero- and few-shot prompting 章節。
3. 依模板新增 content/few-shot-prompting.json，填入固定欄位與四個章節。
4. 執行 python3 scripts/build.py，產生第五篇獨立頁與更新後的搜尋索引。
5. 提交至 GitHub main，由 Pages 工作流程驗證並發布。

新增文章的檔案
content/few-shot-prompting.json

自動產物（不手動修改）
notes/few-shot-prompting.html
index.html 的文章卡片與文章數量
search-index.json 的全文搜尋資料

規則如何發揮作用
章節順序、來源要求與命名由 AGENTS.md 指定；模板提供資料格式；共用建置器產生網頁。因此新增第五篇時，不必複製 HTML 或為該篇新增 CSS。

同次改善
新增內容管理頁，提供新增表單與 GitHub 修改、刪除入口；登入有寫入權限的 GitHub 帳號提交後，正式 Pages 網址才會更新。表單產生 JSON 並不等於已儲存。Sites 是手動發布的展示鏡像。

可核對證據
- 新文章：notes/few-shot-prompting.html
- 原始資料：GitHub 的 content/few-shot-prompting.json
- 發布執行：GitHub Repository → Actions → Build and deploy notebook
- 實際驗證結果將依工作流程及瀏覽器檢查填入，未成功前不宣稱完成。
