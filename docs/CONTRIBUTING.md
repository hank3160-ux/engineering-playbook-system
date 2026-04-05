# Contributing Guide

歡迎貢獻 Engineering Playbook System。本指南說明如何使用 `template/` 啟動新專案，以及如何提交變更。

---

## 使用 template/ 啟動新專案

`template/` 是一個可直接複製的標準 Python 服務骨架，內建三層架構、logging、環境變數管理與測試範例。

```bash
# 1. 複製模板到新目錄
cp -r template/ ../your-new-service
cd ../your-new-service

# 2. 建立環境變數檔
cp .env.example .env
# 編輯 .env，至少設定 APP_NAME

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 啟動服務
uvicorn app.main:app --reload

# 5. 執行測試
pytest tests/ -v
```

### 模板結構說明

| 路徑 | 職責 | 修改時機 |
|------|------|---------|
| `app/api/` | 路由定義（HTTP 細節） | 新增 endpoint 時 |
| `app/services/` | 業務邏輯 | 新增功能時 |
| `app/schemas/` | Pydantic 資料結構 | 新增 request/response model 時 |
| `app/config/settings.py` | 環境變數 | 新增設定項目時 |

---

## 提交變更流程

### 1. Fork & Branch

```bash
git checkout -b feat/your-feature-name
```

分支命名遵循 `<type>/<short-description>`，type 同 Conventional Commits。

### 2. 開發

- 遵循 [`playbook/01-standard-workflow`](../playbook/01-standard-workflow/) 的命名與 commit 規範
- 架構決策參考 [`playbook/02-architecture-and-quality`](../playbook/02-architecture-and-quality/)

### 3. 本地驗證

```bash
# Lint
pip install ruff
ruff check .

# 測試
pytest

# 安全掃描
bash scripts/check-secrets.sh
```

### 4. 提交 Pull Request

- 使用 PR 模板填寫所有 checkbox
- 確保 CI 全數通過後再請求 review

---

## 規範文件更新原則

若你的變更涉及工程規範（命名、架構、資安），請同步更新對應的 `playbook/` 文件，確保 SSOT 一致性。

---

*有任何問題，請開 Issue 討論，再開始實作。*
