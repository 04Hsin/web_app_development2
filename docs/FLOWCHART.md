# 流程圖設計文件 (FLOWCHART)

本文件根據「個人記帳簿系統」之 PRD 與相關架構設計，視覺化了使用者的核心操作路徑，以及系統內部的資料與請求流程。

## 1. 使用者流程圖（User Flow）

描述使用者進入記帳系統後，可能進行的各種操作及其先後順序。

```mermaid
flowchart TD
    A([使用者開啟網頁]) --> B[首頁 - 總覽與新增介面]
    
    B --> C{要執行什麼操作？}
    
    C -->|想新增收支| D[填寫收支表單\n包含金額、日期、分類等]
    D -->|點擊送出| E([系統儲存資料並更新餘額])
    E --> B
    
    C -->|查看歷史明細| F[切換至歷史紀錄頁面]
    F --> G{針對特定紀錄操作？}
    G -->|點擊修改| H[修改表單內容]
    H -->|點擊送出| E
    G -->|點擊刪除| I[確認訊息]
    I -->|確認刪除| E
    
    C -->|想了解消費比例| J[切換至圖表報表頁面]
    J --> K[檢視圓餅圖與分類數據]
    
    C -->|管理分類| L[切換至分類設定頁]
    L --> M[新增或刪除自訂分類]
    M --> N([系統更新分類])
    N --> B
```

## 2. 系統序列圖（Sequence Diagram）

以下描述「使用者點擊新增收支」到「系統將資料存入資料庫」並重新顯示結果的完整生命週期。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML/JS)
    participant Flask as Flask (Controller)
    participant Model as Record Model
    participant DB as SQLite
    
    User->>Browser: 填寫收支金額與資訊並按下送出
    Browser->>Flask: POST /records (包含表單資料)
    Flask->>Model: 解析參數，呼叫 create_record()
    Model->>DB: 執行 INSERT INTO records...
    DB-->>Model: 寫入成功
    Model-->>Flask: 回傳執行結果
    Flask->>Model: 查詢最新的總餘額與紀錄清單
    Model->>DB: SELECT SUM(amount)...
    DB-->>Model: 回傳最新資料
    Model-->>Flask: 最新資料變數
    Flask->>Browser: 重新導向 GET / (首頁) 並渲染 Jinja2
    Browser-->>User: 畫面更新，顯示最新餘額與該筆紀錄
```

## 3. 功能清單與路由對照表

根據 PRD 的需求，我們先規劃好基礎的 URL 路徑與對應的操作。

| 功能描述 | URL 路徑 | HTTP 方法 | 說明 |
| :------- | :------- | :-------- | :--- |
| **首頁總覽** | `/` | `GET` | 顯示總餘額、最近幾筆紀錄，並包含「新增收支」的表單。 |
| **新增收支** | `/records` | `POST` | 接收表單資料並寫入資料庫，完成後回到首頁。 |
| **歷史清單** | `/records` | `GET` | 顯示所有收支列表。 |
| **刪除收支** | `/records/<id>/delete` | `POST` | 依據 ID 刪除該筆紀錄（HTML 表單透過 POST 觸發）。 |
| **修改收支** | `/records/<id>` | `POST` | 接收更新後的紀錄內容寫入資料庫。 |
| **報表頁面** | `/reports` | `GET` | 顯示圖表頁面，由前端圖表模組負責渲染。 |
| **取得圖表資料** | `/api/reports` | `GET` | 回傳統計 JSON 供 JS 繪製圓餅圖 / 長條圖使用。 |
| **新增分類** | `/categories` | `POST` | 新增使用者自訂的收支分類。 |
| **刪除分類** | `/categories/<id>/delete` | `POST` | 刪除單一分類。 |
