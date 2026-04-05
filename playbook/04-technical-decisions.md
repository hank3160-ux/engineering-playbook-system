# Technical Decisions — 技術架構白皮書

> 版本：1.0.0 | SSOT：GitHub

本文件記錄 Engineering Playbook System（EPS）在設計與演進過程中的核心技術決策，說明每個選擇背後的「為什麼」，而非「做了什麼」。

---

## 1. 可維護性（Maintainability）

### 決策：單一事實來源（SSOT）

所有規範、設定、架構決策集中於 GitHub repository，任何變更皆透過 Pull Request 審查。這消除了「口耳相傳的規範」與「文件與代碼不一致」兩個最常見的維護債。

### 決策：三層架構分離

```
api/       ← HTTP 細節（status code、request parsing）
services/  ← 業務邏輯（可獨立測試，不依賴 HTTP）
schemas/   ← 資料契約（輸入驗證、輸出序列化）
```

每層職責單一，修改一層不影響其他層。Service 層可在不啟動 HTTP server 的情況下直接單元測試，大幅降低測試成本。

### 決策：pydantic-settings 管理環境變數

所有設定從環境變數讀取，型別由 Pydantic 自動驗證。服務啟動時若缺少必要設定會立即失敗（fail-fast），而非在運行中途才崩潰，縮短問題定位時間。

### 決策：統一 logging 模組

所有服務從 `logger.py` 取得 logger，確保格式一致。結構化的 `key=value` 格式讓 log aggregator（CloudWatch、Datadog）可直接解析，無需額外 parser。

---

## 2. 擴充性（Scalability & Extensibility）

### 決策：FastAPI + Pydantic v2

FastAPI 的 async-first 設計天然支援高並發 I/O 場景。Pydantic v2 以 Rust 實作核心，序列化效能較 v1 提升 5-50 倍，為未來流量增長預留空間。

### 決策：SQLAlchemy 2.x 異步 ORM

採用 `async_sessionmaker` 與 `AsyncSession`，資料庫操作不阻塞 event loop。`get_db_session` 以 FastAPI Dependency 注入，Session 生命週期由框架管理，業務邏輯無需關心連線池細節。

### 決策：cookiecutter 專案生成

`cookiecutter.json` 讓新服務可在 30 秒內從模板生成，確保所有服務遵循相同的目錄結構與設定慣例。隨著團隊規模增長，這是維持架構一致性的關鍵槓桿。

### 決策：Router 模組化

每個功能域（health、url_checker、users...）有獨立的 `api/` 模組，透過 `app.include_router()` 組裝。新增功能只需新增 router，不修改現有代碼，符合開放封閉原則（OCP）。

---

## 3. 安全性（Security）

### 決策：Multi-stage Docker Build + 非 root 使用者

Builder stage 安裝依賴，runtime stage 只複製必要檔案，映像體積最小化，攻擊面縮小。以非 root 使用者運行，即使容器被突破，攻擊者也無法取得 root 權限。

### 決策：Pre-commit Secret Scanner

`scripts/check-secrets.sh` 在 commit 前掃描 8 種常見 secret 洩露模式（AWS key、GitHub token、OpenAI key 等）。在開發者本機攔截，成本遠低於在 CI 或生產環境發現。

### 決策：Ruff + Mypy 靜態分析

Ruff 在毫秒內完成 linting，mypy strict 模式強制完整型別標注。型別錯誤在 CI 層攔截，避免 `AttributeError`、`None` 解引用等常見運行時錯誤進入生產環境。

### 決策：全域 Exception Handler 回傳 JSON

所有未捕捉例外統一回傳 `{"error": "...", "detail": "..."}` 格式，而非 FastAPI 預設的 HTML 錯誤頁面。這防止 stack trace 洩漏給 client，同時讓 API consumer 可以程式化處理錯誤。

---

## 4. 演進路徑

| 階段 | 已完成 | 建議下一步 |
|------|--------|-----------|
| 基礎 | FastAPI MVP、logging、SSOT | — |
| 品質 | 三層架構、型別標注、pytest | 加入 coverage 門檻（≥80%） |
| 維運 | Docker、CI/CD、GitHub Pages | 加入 Prometheus metrics endpoint |
| 治理 | Issue/PR 模板、cookiecutter | 加入 Dependabot 自動更新依賴 |
| 資料 | SQLAlchemy async、CRUD | 加入 Alembic migration |

---

*技術決策一旦確立，變更須在本文件說明原因，並透過 PR 審查。*
