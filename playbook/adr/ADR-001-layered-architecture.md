# ADR-001: 層次架構設計

| 欄位 | 內容 |
|------|------|
| 狀態 | Accepted |
| 日期 | 2026-04-05 |
| 決策者 | Engineering Team |

---

## 背景

隨著服務功能增加，若所有邏輯集中在路由函式中，會導致：
- 業務邏輯與 HTTP 細節耦合，難以單元測試
- 不同端點重複相同邏輯，違反 DRY 原則
- 新成員難以快速定位「這段邏輯在哪裡」

## 決策

採用三層分離架構：

```
api/       ← HTTP 層：處理 request/response、status code、路由定義
services/  ← 業務層：純 Python 邏輯，不依賴 HTTP 框架
schemas/   ← 資料層：Pydantic model，定義輸入驗證與輸出序列化
```

`main.py` 只負責組裝（掛載 middleware、router），不含任何業務邏輯。

## 考慮過的替代方案

| 方案 | 拒絕原因 |
|------|---------|
| 全部邏輯放在路由函式 | 無法獨立測試業務邏輯，耦合度高 |
| 四層（加 repository 層） | 對目前規模過度設計，可在需要時演進 |
| 使用 MVC 框架（Django） | FastAPI 更輕量，async-first，適合 API 服務 |

## 後果

- 正面：Service 層可在不啟動 HTTP server 的情況下直接測試
- 正面：新增功能只需新增 router + service，不修改現有代碼（OCP）
- 負面：小型功能需建立三個檔案，初期有輕微樣板成本
- 演進路徑：當資料存取邏輯複雜化時，可在 services/ 下加入 repository 層
