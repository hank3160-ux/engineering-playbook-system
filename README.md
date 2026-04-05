# Engineering Playbook System

> 工程標準系統 — 以 GitHub 為核心的單一事實來源（SSOT）平台，統一管理開發規範、流程自動化與可驗證的 MVP 示範。

---

## Vision

打造一套**可執行、可驗證、可演進**的工程標準體系：

- 所有規範以 Markdown 文件存活於 `playbook/`，版本由 Git 管控
- 所有示範以可運行的程式碼存活於 `demo/`，確保文件與實作一致
- 任何變更皆透過 Pull Request 審查，保持 SSOT 原則

---

## Architecture

```
engineering-playbook-system/
│
├── .github/workflows/
│   └── ci.yml                       # GitHub Actions CI（push to main 自動測試）
│
├── playbook/                        # 工程規範文件（SSOT）
│   ├── 01-standard-workflow.md      # 命名、Git Commit、環境安全
│   └── 02-architecture-and-quality.md  # 架構規範、錯誤處理、日誌標準
│
├── demo/                            # 可執行的 MVP 示範
│   ├── main.py                      # FastAPI 入口（middleware & exception handler）
│   ├── logger.py                    # 統一 logging 設定
│   ├── requirements.txt             # 依賴清單
│   └── tests/
│       └── test_health.py           # pytest 測試
│
├── template/                        # 標準 Python 專案模板
│   ├── app/
│   │   ├── main.py                  # FastAPI 入口（組裝層）
│   │   ├── logger.py                # logging 模組
│   │   ├── api/
│   │   │   └── health.py            # 路由層（HTTP 細節）
│   │   ├── services/
│   │   │   └── health_service.py    # 業務邏輯層
│   │   ├── schemas/
│   │   │   └── health.py            # Pydantic 資料結構
│   │   └── config/
│   │       └── settings.py          # pydantic-settings 環境變數管理
│   ├── tests/
│   │   └── test_health.py           # pytest 範例
│   ├── .env.example                 # 環境變數範本
│   └── requirements.txt             # 依賴清單
│
├── mkdocs.yml                       # MkDocs 文件站設定
└── README.md                        # 專案首頁（本文件）
```

### 資料流

```
開發者
  │
  ├─► playbook/  ──► 規範定義（命名、Commit、安全）
  │
  └─► demo/      ──► 實作驗證（FastAPI /health API）
                        │
                        └─► GitHub Actions（CI 自動驗證）
```

---

## 目錄導覽

| 路徑 | 說明 |
|------|------|
| [`playbook/01-standard-workflow.md`](playbook/01-standard-workflow.md) | 專案命名準則、Git Commit 規範、環境安全指引 |
| [`playbook/02-architecture-and-quality.md`](playbook/02-architecture-and-quality.md) | 架構規範、錯誤處理機制、日誌追蹤標準 |
| [`demo/main.py`](demo/main.py) | FastAPI MVP — `/health` API、ProcessTimeMiddleware、Exception Handler |
| [`demo/logger.py`](demo/logger.py) | 結構化 logging 模組 |
| [`template/`](template/) | 標準 Python 專案模板（可直接複製使用） |

---

## Quick Start

```bash
# 1. 安裝依賴
pip install -r demo/requirements.txt

# 2. 啟動 API 服務
uvicorn demo.main:app --reload

# 3. 驗證健康狀態（回應 Header 含 X-Process-Time-Ms）
curl -i http://localhost:8000/health
```

---

## Using the Template

新建服務時，直接複製 `template/` 資料夾：

```bash
# 1. 複製模板
cp -r template/ ../your-new-service

# 2. 建立環境變數檔
cp your-new-service/.env.example your-new-service/.env
# 編輯 .env，填入實際值

# 3. 安裝依賴
pip install -r your-new-service/requirements.txt

# 4. 啟動服務
uvicorn app.main:app --reload
```

模板已內建：pydantic-settings 環境變數管理、統一 logging、global exception handler、pytest 範例測試。

---

## Contributing

所有變更請遵循 [`playbook/01-standard-workflow.md`](playbook/01-standard-workflow.md) 中定義的規範，並透過 Pull Request 提交。

---

## Local Docs Preview

本專案使用 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) 建立文件站。

```bash
# 安裝 MkDocs 與 Material 主題
pip install mkdocs-material

# 啟動本地預覽（預設 http://127.0.0.1:8000）
mkdocs serve
```

文件站包含：首頁（README）、Playbook 所有規範文件，並支援深色模式與程式碼複製。

---

*Maintained with SSOT principle — GitHub is the source of truth.*
