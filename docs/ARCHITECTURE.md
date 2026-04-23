# 系統架構設計文件 (ARCHITECTURE)

基於「個人記帳簿系統」PRD 的需求，以下為本專案的系統架構設計與資料夾結構規劃。

## 1. 技術架構說明

- **選用技術與原因**
  - **後端：Python + Flask**  
    Flask 為輕量級且靈活的 Web 框架，十分適合快速建置 MVP 與中小型個人應用程式。
  - **模板引擎：Jinja2**  
    Flask 內建的模板系統，負責在後端結合 HTML 產生動態頁面，無須額外的繁重前端框架。
  - **資料庫：SQLite**  
    免安裝、輕巧且使用檔案儲存，完全滿足本系統快速啟動與開發的需求。

- **Flask MVC 模式說明**  
  在此架構中，不採取複雜的前後端分離，而是透過經典的 MVC 模式運作：
  - **Model (模型)**：負責與 SQLite 溝通，處理「收支紀錄」與「收支分類」的資料存取與邏輯計算。
  - **View (視圖)**：由 `templates` 內的 Jinja2 HTML 檔案組成，負責呈現畫面與接受使用者的表單輸入。
  - **Controller (控制器)**：由 Flask 的路由 (`routes`) 擔任，接收來自瀏覽器的 Request，調用 Model 取出或寫入資料後，把結果丟給 View (Jinja2) 渲染後回傳給使用者。

## 2. 專案資料夾結構

建議採用模組化的結構，將不同職責的程式碼實體切割：

```text
/
├── app/
│   ├── models/          ← 資料庫模型（定義資料庫操作與 Schema）
│   │   ├── index.py     ← 資料庫連線或初始化腳本
│   │   └── record.py    ← 收支紀錄及分類的 Model
│   ├── routes/          ← Flask 路由（Controller，定義路徑與行為）
│   │   └── main.py      ← 主要路由（首頁、紀錄收支、歷史列表等）
│   ├── templates/       ← Jinja2 HTML 模板（View）
│   │   ├── base.html    ← 共用版型（包含 Navigation Bar 等）
│   │   ├── index.html   ← 首頁（總覽、新增收支的表單）
│   │   └── history.html ← 歷史紀錄與修改頁面
│   └── static/          ← 靜態資源檔案
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
├── instance/
│   └── database.db      ← SQLite 資料庫檔案（程式執行後動態生成）
├── docs/                ← 文件目錄（PRD, Architecture 等）
├── app.py               ← 專案進入點，負責初始化 Flask 與註冊 routes
└── requirements.txt     ← Python 依賴套件表 (Flask 等)
```

## 3. 元件關係圖

以下展示各元件在一個典型 HTTP 請求中的互動關係：

```mermaid
flowchart TD
    Browser(使用者瀏覽器) --"1. 發送 GET/POST Request"--> Route(Flask Route\n[Controller])
    Route --"2. 請求 CRUD 或計算"--> Model(Models\n[商業邏輯與資料層])
    Model --"3. 執行 SQL 語法"--> SQLite[(SQLite 資料庫)]
    SQLite --"4. 回傳資料查詢結果"--> Model
    Model --"5. 將處理後資料回傳"--> Route
    Route --"6. 將資料變數傳入 Template"--> Template(Jinja2 Template\n[View])
    Template --"7. 結合變數渲染出完整 HTML"--> Route
    Route --"8. 回傳 HTTP Response"--> Browser
```

## 4. 關鍵設計決策

1. **採用後端渲染 (SSR) 取代前後端分離**  
   **原因：** 本應用功能相對單純、著重於 CRUD 與個人化使用。使用 Flask 直接回傳渲染好的 HTML，可避開建立 RESTful API 以及除錯 CORS 的耗時工作，加速 MVP 的產出。

2. **將資料庫與應用邏輯封裝在 Models 目錄**  
   **原因：** 確保所有的 SQL 語句與複雜運算不和 Route 邏輯混淆，使得 Route 的程式碼可以維持簡短，只專注於接收參數跟選擇渲染頁面，提高程式碼的易讀性與未來可擴充性。

3. **靜態資源的管理與圖表渲染**  
   **原因：** 畫面的圖表（如圓餅圖）需要一定的前端互動性，因此會在頁面上寫 JavaScript 透過外部庫（如 Chart.js）繪製。後端 Route 只負責算好總數並當作 JSON 結構寫入 Jinja 變數（或直接回應輕量的 JSON 給 JS 呼叫），讓繪圖操作交給瀏覽器處理以維持效能。
