# 路由與頁面規劃文件 (ROUTES.md)

本文件整理了「個人記帳簿系統」的所有路由路徑、HTTP 請求對應，以及會使用到的 Jinja2 網頁模板清單。

## 1. 路由總覽表格

| 功能名稱 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :------- | :-------- | :------- | :------- | :--- |
| **首頁總覽** | GET | `/` | `templates/index.html` | 讀取目前的餘額與總收支，並附上快速新增收支的表單。 |
| **歷史清單** | GET | `/records` | `templates/records/index.html` | 呈現所有歷史紀錄的詳細清單列表。 |
| **新增收支** | POST | `/records` | — | 接收首頁新建表單。驗證參數，存入 DB，成功後重導向回首頁。 |
| **修改頁面** | GET | `/records/<id>/edit` | `templates/records/edit.html` | 讀取特定一筆紀錄，並顯示更新用的表單。 |
| **更新收支** | POST | `/records/<id>/update`| — | 接收編輯表單的資料並 UPDATE DB，成功後導向歷史清單。 |
| **刪除收支** | POST | `/records/<id>/delete`| — | 刪除單筆紀錄，完成後重導向至歷史清單。（不使用 DELETE 方法以相容 HTML表單）|
| **分類清單** | GET | `/categories` | `templates/categories/index.html` | 列出目前可用的分類與新增表格。 |
| **新增分類** | POST | `/categories` | — | 接收並建立新自訂分類，建立後重導向 `/categories`。 |
| **刪除分類** | POST | `/categories/<id>/delete`| — | 若無掛載任何紀錄則允許刪除，並重導向自身頁面。 |
| **圖表報表** | GET | `/reports` | `templates/reports/index.html` | 顯示包含 JavaScript 圓餅圖組件的報表框架頁面。 |
| **報表 API** | GET | `/api/reports` | — (回傳 JSON) | 分析並計算各分類的加總金額，回應給頁面上的前端圖表。 |

## 2. 每個路由的詳細說明

### 2.1 主頁面 (`/`)
- **輸入**：無。
- **處理邏輯**：呼叫 `Record.get_summary()` 取出收支狀態，以及 `Record.get_all()` 顯示近期幾筆。同時需要呼叫 `Category.get_all()` 產生給下拉選單的選項。
- **輸出**：渲染 `index.html`。
- **錯誤處理**：無。

### 2.2 收支管理模組 (`/records...`)
這裡將所有的 `Record` 相關路由分組。
- **新增 (`POST /records`)**：
  - 輸入：表單的 `amount`, `category_id`, `record_date`, `note`。
  - 處理邏輯：驗證金額與時間合法後，呼叫 `Record.create()`。
  - 輸出：重導向至 `/` (搭配 Flash "新增成功")。
- **更新 (`POST /records/<id>/update`)**：
  - 與新增類似，但呼叫的是 `Record.update()`。成功後導向 `/records`。

### 2.3 分類管理模組 (`/categories...`)
- **刪除 (`POST /categories/<id>/delete`)**：
  - 處理邏輯：檢查該 `id` 是否已存在於 `records` 表中。若有綁定，則設定 Flash error 阻擋並導向 `/categories`。若無綁定，呼叫 `Category.delete()`。

## 3. Jinja2 模板清單

所有的網頁模板放置於 `app/templates/`。我們使用強大的階層繼承：

1. **`base.html`** (共用主版面)：包含所有頁面的標題 (Navigation Bar) 與 Flash Message 渲染機制，以及所需的 CSS 連結。下面的所有頁面皆會繼承此檔案。
2. **`index.html`** (首頁)：首頁總覽。
3. **`records/index.html`**：歷史紀錄的列表清單。
4. **`records/edit.html`**：獨立出來的收支紀錄編輯畫面。
5. **`categories/index.html`**：展示分類與負責新增的 UI 介面。
6. **`reports/index.html`**：繪製 Canvas 圖表的報表頁面。
