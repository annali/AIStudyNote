# 作業繳交內容

繳交標題：`學校 學號 系級 姓名 AI 學習筆記庫`（請自行填入個人資料）

## 1. 專案簡介

「AI 學習筆記庫」是面向 AI 初學者的繁體中文知識網站，整理提示設計、RAG、工作流程與 Agent 等概念。每篇筆記包含核心概念、實作範例、常見誤解、動手練習及參考來源。網站提供分類、全文搜尋、獨立文章頁與內容管理入口，方便累積與回顧。

這次的重點是建立可重複使用的規則。專案以 AGENTS.md 定義內容與開發方式，透過 JSON 模板及共用建置器，讓未來新增文章時也能保持一致。

## 2. GitHub Repository 連結

https://github.com/annali/AIStudyNote

## 3. 網頁連結

正式自動更新網站：https://annali.github.io/AIStudyNote/

展示鏡像：https://ai-notebook-anna-2026.singinghedgehog2.chatgpt.site

## 4. AGENTS.md

檔案位於專案根目錄：[AGENTS.md](AGENTS.md)。文件包含專案目的、技術與目錄責任、整體風格、文章欄位、來源規則、新增流程、驗證方式與完成判準。

## 5. 規則如何幫助 AI 繼續新增內容？

如果要新增「少樣本提示」筆記，AI 可以先閱讀 AGENTS.md，複製 templates/note.json 到 content/few-shot-prompting.json，依規定填入標題、摘要、分類、標籤、日期、四個固定章節與參考來源，再執行 python3 scripts/build.py。

建置器會檢查格式並自動產生獨立網頁、更新首頁與搜尋索引。因此新增內容時不用重新設計版型，也不用手動維護文章清單。共用樣式讓新舊內容風格一致，而規則中的來源要求與檢查步驟，讓 AI 知道內容完成後還應驗證什麼。

## AI 使用說明

使用 AI 協助完成專案規則、網站程式與初版筆記，技術內容附官方文件或原始論文來源。提交前由本人閱讀與確認內容，並依課程規定揭露 AI 使用方式。

## 延伸能力的實際證據

已依照 AGENTS.md 與模板新增第五篇「用範例教 AI：少樣本提示」，檔案為 content/few-shot-prompting.json。完整操作紀錄見 [docs/extension-demo.md](docs/extension-demo.md)。

內容管理頁可產生新筆記 JSON，並提供 GitHub 修改、刪除入口；登入並提交後，GitHub Actions 會檢查格式、重建網站並發布到 GitHub Pages。管理權限由 GitHub 控制，沒有把私密金鑰放進網頁。

驗證執行紀錄見 Repository 的 Actions 頁面；新增、修改、刪除的建置結果由 scripts/check.py 在隔離的暫存專案測試。

## 自動發布成功紀錄

[首次新版成功發布的 GitHub Actions 執行](https://github.com/annali/AIStudyNote/actions/runs/43587355669)，對應提交 19e6aeedbf2932d4c73dc2d9fedf8d96822ae3ec，結果為 success。正式網站已由原本四篇擴充為五篇。
