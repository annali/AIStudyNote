# AI 學習筆記庫

一個以 `AGENTS.md` 驅動內容擴充的繁體中文靜態網站。透過「核心概念 → 實作範例 → 常見誤解 → 動手練習」的固定格式，把 AI 學習整理成可以持續累積的筆記。

Repository：https://github.com/annali/AIStudyNote

正式網站（GitHub 提交後自動發布）：https://annali.github.io/AIStudyNote/

展示鏡像（手動更新）：https://ai-notebook-anna-2026.singinghedgehog2.chatgpt.site

## 專案亮點

- 首頁有主題篩選、全文搜尋及無結果提示。
- 五篇獨立筆記，涵蓋提示設計、RAG、工作流程與 Agent、專案協作規則。
- `AGENTS.md` 規定內容、風格、檔案責任與開發驗證步驟。
- 內容管理頁提供新增表單、GitHub 修改與刪除入口；需登入並提交後才保存。
- 每篇 JSON 自動生成 HTML，新增文章不用複製頁面或修改首頁。
- 無第三方建置套件、無 API 金鑰、無後端需求。
- 外部技術概念附原始論文或官方來源；本文為 AI 輔助整理的教學內容，非官方翻譯。

## 本機啟動

需要 Python 3.9 以上版本。

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory dist
```

瀏覽 `http://localhost:8000`。請透過 HTTP 預覽，瀏覽器直接開啟檔案時不一定能載入全文搜尋索引。索引載入失敗時會退回標題、摘要與標籤搜尋。

## 結構

```text
AGENTS.md                  AI 協作規則（請先閱讀）
content/*.json             一篇檔案一篇筆記
assets/style.css           共用樣式與手機排版
assets/app.js              搜尋及分類互動
templates/note.json        新增筆記模板
scripts/build.py           內容驗證與靜態頁生成器
.github/workflows/pages.yml  GitHub Pages 自動發布
dist/                      自動產物，不提交
SUBMISSION.md              作業繳交文字
```

## 如何新增內容

1. 先閱讀 [AGENTS.md](AGENTS.md)。
2. 複製 [文章模板](templates/note.json) 到 `content/<slug>.json`。
3. 填好標題、摘要、日期、分類、標籤、四個章節及實際閱讀的來源。
4. 執行 `python3 scripts/build.py`，錯誤會指出需要修正的檔案。
5. 本機檢查首頁、搜尋、分類、獨立頁面、參考來源與手機排版。
6. 推送 main 分支，讓 Pages 工作流程建置及部署。

給 AI 的指令範例：

> 請先閱讀 AGENTS.md，依模板新增少樣本提示筆記，slug 為 few-shot-prompting。分類為提示設計，核對官方來源後填入四個章節，執行建置，說明驗證結果。

## GitHub Pages 設定

在 Repository 的 Settings → Pages → Build and deployment，將 Source 設為 **GitHub Actions**，再從 Actions 執行 `Build and deploy notebook`。此網站所有內部連結使用相對路徑，支援 `https://帳號.github.io/儲存庫名稱/` 子路徑。

也可將 `dist/` 部署到其他靜態網站服務；`.openai/hosting.json` 是此專案 Sites 發布設定，不影響 GitHub Pages。

## 檢查範圍

建置器驗證文章結構、檔名、slug、分類、日期、標籤、段落及來源網址格式，並以 HTML escaping 輸出文字。格式檢查無法證明內容正確；仍需核對外部資料及實際閱讀體驗。

## AI 使用說明

本專案由使用者選定主題，透過 AI 協助撰寫規則、程式與初版教學筆記。網站範例與練習為教學設計，未聲稱已執行真實模型測試。繳交前請閱讀、理解並依課程規定揭露 AI 使用方式。

## 實際管理內容

在網站「內容管理」頁填表產生 JSON，按「複製 JSON」，再點 GitHub 新增連結，貼到新檔案中並 Commit changes。修改與刪除入口會前往對應 GitHub 頁面，由有寫入權限的帳號確認提交。表單尚未提交的內容不會保存到網站。

GitHub main 提交 → Actions 驗證 → 建置 dist → GitHub Pages 發布。正式持續更新網址是 `https://annali.github.io/AIStudyNote/`；Sites 是手動更新的鏡像，不會隨 GitHub 自動同步。

## 擴充實證與驗證

[第五篇筆記的實際擴充紀錄](docs/extension-demo.md) 記錄使用指令、來源與檔案變更。

執行 `python3 scripts/check.py`，會在暫存專案驗證新增、修改、刪除如何同步影響獨立頁、首頁與索引，也確認格式不符會阻止建置。GitHub Actions 會先執行此檢查，再建置部署。這些檢查不會修改真正的筆記。
