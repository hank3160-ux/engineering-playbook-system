# 🏗️ Engineering Playbook System（工程標準系統）

> **v2.0.0 Golden Release** — 以 GitHub 為核心的**單一事實來源（SSOT）**平台，統一管理開發規範、流程自動化與可驗證的 MVP 示範。

📖 **線上文件站**：[https://hank3160-ux.github.io/engineering-playbook-system](https://hank3160-ux.github.io/engineering-playbook-system)

[![CI](https://github.com/hank3160-ux/engineering-playbook-system/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/hank3160-ux/engineering-playbook-system/actions/workflows/ci.yml)
[![Deploy Docs](https://github.com/hank3160-ux/engineering-playbook-system/actions/workflows/deploy-docs.yml/badge.svg?branch=main)](https://github.com/hank3160-ux/engineering-playbook-system/actions/workflows/deploy-docs.yml)
[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![codecov](https://img.shields.io/badge/coverage-tracked-brightgreen?logo=codecov)](https://github.com/hank3160-ux/engineering-playbook-system)
[![Version](https://img.shields.io/badge/version-v2.0.0-6366f1)](https://github.com/hank3160-ux/engineering-playbook-system/blob/main/CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-22c55e)](https://github.com/hank3160-ux/engineering-playbook-system/blob/main/LICENSE)

---

## 📋 目錄

- [專案簡介](#-專案簡介)
- [核心理念](#-核心理念)
- [技術棧總覽](#-技術棧總覽)
- [系統架構圖](#-系統架構圖)
- [請求處理流程圖](#-請求處理流程圖)
- [CI/CD 自動化流程圖](#-cicd-自動化流程圖)
- [專案目錄結構](#-專案目錄結構)
- [目錄導覽](#-目錄導覽)
- [快速開始](#-快速開始)
- [Docker 部署](#-docker-部署)
- [API 文件](#-api-文件)
- [測試說明](#-測試說明)
- [安全機制](#-安全機制)
- [工程實踐說明](#-工程實踐說明)
- [如何使用 Template 建立新服務](#-如何使用-template-建立新服務)
- [本地文件站預覽](#-本地文件站預覽)
- [版本紀錄](#-版本紀錄)
- [給面試官的閱讀指南](#-給面試官的閱讀指南)
- [貢獻指南](#-貢獻指南)
- [開發歷程](#-開發歷程)

---

## 📌 專案簡介

**Engineering Playbook System（EPS）** 是一套**可執行、可驗證、可演進**的工程標準體系。它不是一個要直接部署的服務，而是一個**工程文化的起手式**——提供規範文件、可運行的示範程式碼、標準專案模板，以及完整的自動化防護鏈。

**這個專案解決什麼問題？**

| 問題 | EPS 的解法 |
|------|-----------|
| 工程規範只存在口頭約定，新人無從遵循 | 所有規範以 Markdown 存活於 `docs/playbook/`，版本由 Git 管控 |
| 文件寫了但沒人看，因為跟實作脫節 | 所有示範以可運行的程式碼存活於 `demo/`，CI 自動驗證 |
| 每個新專案從零開始，架構風格不一致 | `template/` 提供標準三層架構模板，可直接複製使用 |
| 敏感資料不小心被 commit | `pre-commit` hook 自動掃描 8 種常見 secret 洩露模式 |

---

## 💡 核心理念

```
┌─────────────────────────────────────────────────────────┐
│                    SSOT 原則                             │
│   Single Source of Truth — 單一事實來源                    │
│                                                         │
│   📄 規範 → Git 管控的 Markdown（docs/playbook/）         │
│   💻 實作 → 可運行的程式碼（demo/）                        │
│   🔄 變更 → 必須透過 Pull Request 審查                    │
│   ✅ 驗證 → GitHub Actions CI 自動測試                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ 技術棧總覽

### 後端框架與語言

| 技術 | 版本 | 用途說明 |
|------|------|---------|
| **Python** | 3.11+ | 主要開發語言，支援現代型別提示語法（`X \| None`） |
| **FastAPI** | 0.110 | 高效能非同步 Web 框架，自動生成 OpenAPI 文件 |
| **Uvicorn** | 0.29 | ASGI 伺服器，支援 HTTP/1.1，用於運行 FastAPI |
| **Pydantic** | 2.6 | 資料驗證與序列化，定義 Request/Response Schema |
| **pydantic-settings** | 2.2 | 環境變數管理，支援 `.env` 檔案自動載入 |

### 資料庫（Template 示範用）

| 技術 | 版本 | 用途說明 |
|------|------|---------|
| **SQLAlchemy** | 2.0 | ORM 框架，支援非同步操作（async/await） |
| **aiosqlite** | 0.20 | SQLite 非同步驅動，用於測試環境的 in-memory DB |
| **asyncpg** | 0.29 | PostgreSQL 非同步驅動，用於生產環境 |

### 測試工具

| 技術 | 版本 | 用途說明 |
|------|------|---------|
| **pytest** | 8.1 | Python 測試框架，支援 fixture、參數化測試 |
| **pytest-asyncio** | 0.23 | pytest 的非同步測試擴充，支援 `async def test_*` |
| **httpx** | 0.27 | 非同步 HTTP 客戶端，用於 API 整合測試 |

### 程式碼品質工具

| 技術 | 用途說明 |
|------|---------|
| **Ruff** | 超快速 Python Linter & Formatter（取代 flake8 + isort + black） |
| **Mypy** | 靜態型別檢查，啟用 `--strict` 模式 |
| **pre-commit** | Git hook 管理框架，commit 前自動執行檢查 |
| **Commitizen** | 互動式 Conventional Commits 工具，自動生成 CHANGELOG |

### 容器化與部署

| 技術 | 用途說明 |
|------|---------|
| **Docker** | Multi-stage build，最小化映像體積，非 root 使用者運行 |
| **Docker Compose** | 一鍵啟動 API 服務（port 8000）+ 文件站（port 8080） |
| **GitHub Actions** | CI/CD 自動化：測試、文件部署、CHANGELOG 生成 |
| **GitHub Pages** | 靜態文件站託管（MkDocs Material 主題） |

### 文件系統

| 技術 | 用途說明 |
|------|---------|
| **MkDocs** | 靜態文件站生成器，以 Markdown 為來源 |
| **Material for MkDocs** | MkDocs 主題，支援深色模式、導航分頁、Mermaid 圖表 |
| **Mermaid** | 在 Markdown 中繪製流程圖、時序圖、架構圖 |

---

## 🏛️ 系統架構圖

### 整體架構

```mermaid
graph TB
    subgraph "👨‍💻 開發者工作流"
        DEV[開發者] -->|git commit| PRE[pre-commit hooks]
        PRE -->|1. 格式檢查| RUFF[Ruff Linter/Formatter]
        PRE -->|2. 型別檢查| MYPY[Mypy 靜態分析]
        PRE -->|3. 安全掃描| SEC[check-secrets.sh]
        PRE -->|4. 檔案檢查| HOOKS[trailing-whitespace<br/>end-of-file-fixer<br/>check-yaml/toml/json]
    end

    subgraph "🔄 GitHub Actions CI/CD"
        PUSH[Push to main] -->|觸發| CI[CI Pipeline]
        CI -->|1| INSTALL[安裝依賴]
        INSTALL -->|2| TEST[pytest 自動測試]
        PUSH -->|觸發| DOCS_DEPLOY[文件站部署]
        DOCS_DEPLOY --> PAGES[GitHub Pages]
        PUSH -->|觸發| RELEASE[Release Pipeline]
        RELEASE --> CHANGELOG[自動更新 CHANGELOG]
    end

    subgraph "📦 Docker 容器"
        COMPOSE[docker-compose.yml] -->|啟動| API_CONTAINER[API 容器<br/>port 8000]
        COMPOSE -->|啟動| DOCS_CONTAINER[文件站容器<br/>port 8080]
    end

    subgraph "🌐 FastAPI 應用程式"
        APP[FastAPI App] --> MW1[Request ID Middleware]
        MW1 --> MW2[Process Time Middleware]
        MW2 --> ROUTER{路由分發}
        ROUTER -->|/health| HEALTH[健康檢查端點]
        ROUTER -->|/items/*| ITEMS[Items CRUD 端點]
        APP --> EXC[全域 Exception Handler]
        APP --> LOG[結構化 Logging<br/>自動注入 Request ID]
    end
```

### 三層架構設計（Layered Architecture）

```mermaid
graph LR
    subgraph "API 層 — api/"
        A1[路由定義]
        A2[HTTP 狀態碼處理]
        A3[Request/Response 轉換]
    end

    subgraph "業務邏輯層 — services/"
        B1[核心業務規則]
        B2[資料處理邏輯]
        B3[不依賴 HTTP 框架]
    end

    subgraph "資料結構層 — schemas/"
        C1[Pydantic Model]
        C2[輸入驗證]
        C3[輸出序列化]
    end

    A1 -->|呼叫| B1
    B1 -->|使用| C1
    A3 -->|驗證| C2

    style A1 fill:#4FC3F7,stroke:#0288D1
    style A2 fill:#4FC3F7,stroke:#0288D1
    style A3 fill:#4FC3F7,stroke:#0288D1
    style B1 fill:#81C784,stroke:#388E3C
    style B2 fill:#81C784,stroke:#388E3C
    style B3 fill:#81C784,stroke:#388E3C
    style C1 fill:#FFB74D,stroke:#F57C00
    style C2 fill:#FFB74D,stroke:#F57C00
    style C3 fill:#FFB74D,stroke:#F57C00
```

> **設計原則**：每一層只依賴下一層，不反向依賴。API 層處理 HTTP 細節，Service 層處理純業務邏輯（可獨立單元測試），Schema 層定義資料結構與驗證規則。詳見 [ADR-001](docs/playbook/adr/ADR-001-layered-architecture.md)。

---

## 🔄 請求處理流程圖

以下展示一個 HTTP 請求從進入到回應的完整生命週期：

```mermaid
sequenceDiagram
    participant C as 客戶端
    participant MW1 as Request ID<br/>Middleware
    participant MW2 as Process Time<br/>Middleware
    participant R as 路由層<br/>api/
    participant S as 業務層<br/>services/
    participant L as Logger

    C->>MW1: HTTP Request
    MW1->>MW1: 生成/讀取 X-Request-ID
    MW1->>MW2: 傳遞請求
    MW2->>MW2: 記錄開始時間
    MW2->>R: 傳遞請求
    R->>S: 呼叫業務邏輯
    S-->>R: 回傳結果
    R-->>MW2: HTTP Response
    MW2->>MW2: 計算處理耗時
    MW2->>L: 記錄 method / path / status / duration_ms
    MW2-->>MW1: 注入 X-Process-Time-Ms Header
    MW1-->>C: 注入 X-Request-ID Header + 回應
```

**關鍵設計說明：**

- **Request ID**：每個請求自動分配唯一 UUID，透過 `contextvars` 在整個非同步呼叫鏈中傳遞，不需手動傳參
- **Process Time**：自動計算每個請求的處理耗時（毫秒），注入 Response Header，為 SLI/SLO 監控提供數據
- **結構化 Logging**：每條 log 自動包含 `request_id`，格式為 `key=value`，方便日誌聚合工具解析

---

## 🚀 CI/CD 自動化流程圖

```mermaid
graph LR
    subgraph "觸發條件"
        PUSH[Push to main]
        PR[Pull Request]
    end

    subgraph "CI Pipeline（ci.yml）"
        CHECKOUT1[Checkout 程式碼] --> SETUP1[設定 Python 3.11]
        SETUP1 --> DEPS[安裝依賴]
        DEPS --> PYTEST[執行 pytest 測試]
    end

    subgraph "文件部署（deploy-docs.yml）"
        CHECKOUT2[Checkout 程式碼] --> SETUP2[設定 Python 3.11]
        SETUP2 --> MKDOCS[安裝 MkDocs Material]
        MKDOCS --> DEPLOY[部署至 GitHub Pages]
    end

    subgraph "版本發布（release.yml）"
        CHECKOUT3[Checkout 程式碼] --> CZ[Commitizen]
        CZ --> CL[生成/更新 CHANGELOG]
        CL --> COMMIT[自動 Commit 回 main]
    end

    PUSH --> CHECKOUT1
    PUSH --> CHECKOUT2
    PUSH --> CHECKOUT3
    PR --> CHECKOUT1

    style PYTEST fill:#81C784,stroke:#388E3C
    style DEPLOY fill:#4FC3F7,stroke:#0288D1
    style CL fill:#FFB74D,stroke:#F57C00
```

**三條 Pipeline 說明：**

| Pipeline | 觸發條件 | 功能 |
|----------|---------|------|
| **CI**（`ci.yml`） | Push to main / PR | 自動執行 `pytest` 測試，確保程式碼品質 |
| **Deploy Docs**（`deploy-docs.yml`） | Push to main | 自動將 MkDocs 文件站部署至 GitHub Pages |
| **Release**（`release.yml`） | Push to main | 使用 Commitizen 自動生成/更新 CHANGELOG |

---

## 📁 專案目錄結構

```
engineering-playbook-system/
│
├── .github/workflows/                    # GitHub Actions 自動化工作流
│   ├── ci.yml                           #   ├── CI：push/PR 時自動執行 pytest
│   ├── deploy-docs.yml                  #   ├── 文件站：自動部署至 GitHub Pages
│   └── release.yml                      #   └── 版本：Commitizen 自動更新 CHANGELOG
│
├── demo/                                # 可執行的 MVP 示範應用程式
│   ├── main.py                          #   ├── FastAPI 入口（Middleware + Exception Handler + 路由掛載）
│   ├── context.py                       #   ├── Request Context（contextvars 傳遞 request_id）
│   ├── logger.py                        #   ├── 結構化 Logging（自動注入 request_id）
│   ├── Dockerfile                       #   ├── Multi-stage Docker 建置檔
│   ├── requirements.txt                 #   ├── Python 依賴清單
│   ├── api/                             #   ├── API 層（路由定義）
│   │   ├── __init__.py                  #   │   └── 套件初始化
│   │   └── items.py                     #   │   └── Items CRUD 路由（GET/POST/DELETE）
│   ├── schemas/                         #   ├── 資料結構層（Pydantic Model）
│   │   ├── __init__.py                  #   │   └── 套件初始化
│   │   └── item.py                      #   │   └── ItemCreate / ItemResponse 定義
│   ├── services/                        #   ├── 業務邏輯層（純 Python，不依賴 HTTP）
│   │   ├── __init__.py                  #   │   └── 套件初始化
│   │   └── item_service.py             #   │   └── CRUD 邏輯（in-memory dict 模擬）
│   └── tests/                           #   └── 測試套件
│       ├── __init__.py                  #       ├── 套件初始化
│       ├── test_health.py               #       ├── /health 端點測試（4 個測試案例）
│       ├── test_items.py                #       ├── /items CRUD 測試（7 個測試案例）
│       └── test_database.py             #       └── 非同步資料庫測試（SQLite in-memory）
│
├── template/                            # 標準 Python 專案模板（可直接複製使用）
│   ├── app/                             #   ├── 應用程式主目錄
│   │   ├── main.py                      #   │   ├── FastAPI 入口（組裝層）
│   │   ├── logger.py                    #   │   ├── Logging 模組
│   │   ├── api/health.py                #   │   ├── 路由層範例
│   │   ├── services/health_service.py   #   │   ├── 業務邏輯層範例
│   │   ├── schemas/health.py            #   │   ├── 資料結構層範例
│   │   ├── config/settings.py           #   │   ├── pydantic-settings 環境變數管理
│   │   └── database/                    #   │   └── 資料庫層
│   │       ├── connection.py            #   │       ├── 非同步連線管理
│   │       ├── models.py                #   │       ├── SQLAlchemy ORM Model
│   │       └── crud.py                  #   │       └── CRUD 操作函式
│   ├── tests/test_health.py             #   ├── pytest 測試範例
│   ├── .env.example                     #   └── 環境變數範本
│   └── requirements.txt                 #
│
├── docs/                                # MkDocs 文件站來源
│   ├── playbook/                        #   ├── 工程規範文件（Playbook）
│   │   ├── 01-standard-workflow.md      #   │   ├── 命名準則、Git Commit 規範、環境安全
│   │   ├── 02-architecture-and-quality.md#  │   ├── 架構規範、錯誤處理、日誌標準
│   │   ├── 03-observability-and-security.md#│   ├── 可觀測性、SLI/SLO、資安防禦
│   │   ├── 04-technical-decisions.md    #   │   ├── 技術決策總覽
│   │   ├── 05-reliability-checklist.md  #   │   ├── 可靠性檢查清單
│   │   └── adr/                         #   │   └── 架構決策紀錄（ADR）
│   │       ├── ADR-001-layered-architecture.md  # 三層架構設計決策
│   │       ├── ADR-002-async-database.md        # 非同步資料庫選型決策
│   │       └── ADR-003-cicd-design.md           # CI/CD 設計決策
│   └── how-to-extend.md                 #   └── 架構擴充指南
│
├── scripts/                             # 自動化腳本
│   ├── dev-setup.sh                     #   ├── 開發環境一鍵初始化
│   └── check-secrets.sh                 #   └── Pre-commit 敏感資料掃描
│
├── docker-compose.yml                   # Docker Compose：一鍵啟動 API + 文件站
├── mkdocs.yml                           # MkDocs Material 文件站設定
├── pyproject.toml                       # 專案設定（Ruff + pytest + Mypy + Commitizen）
├── .pre-commit-config.yaml              # Pre-commit hooks 設定
├── cookiecutter.json                    # Cookiecutter 模板參數
├── CHANGELOG.md                         # 自動生成的版本變更紀錄
├── LICENSE                              # MIT 授權條款
└── README.md                            # 本文件
```

---

## 📖 目錄導覽

| 路徑 | 說明 |
|------|------|
| [`docs/playbook/01-standard-workflow`](https://hank3160-ux.github.io/engineering-playbook-system/playbook/01-standard-workflow/) | 專案命名準則、Git Commit 規範（Conventional Commits）、環境安全指引 |
| [`docs/playbook/02-architecture-and-quality`](https://hank3160-ux.github.io/engineering-playbook-system/playbook/02-architecture-and-quality/) | 三層架構規範、錯誤處理機制、結構化日誌追蹤標準 |
| [`docs/playbook/03-observability-and-security`](https://hank3160-ux.github.io/engineering-playbook-system/playbook/03-observability-and-security/) | 可觀測性指標（SLI/SLO）、金鑰管理 SOP、資安防禦清單 |
| [`docs/playbook/04-technical-decisions`](https://hank3160-ux.github.io/engineering-playbook-system/playbook/04-technical-decisions/) | 技術決策總覽與 ADR 索引 |
| [`docs/playbook/05-reliability-checklist`](https://hank3160-ux.github.io/engineering-playbook-system/playbook/05-reliability-checklist/) | 生產環境可靠性檢查清單 |
| [`docs/playbook/adr/`](docs/playbook/adr/) | 架構決策紀錄（ADR）— 層次架構、非同步 DB、CI/CD 設計 |
| [`demo/`](demo/) | FastAPI MVP 示範 — Middleware、Exception Handler、CRUD、pytest |
| [`template/`](template/) | 標準 Python 專案模板（三層架構 + 資料庫層，可直接複製） |
| [`scripts/`](scripts/) | 自動化腳本 — 開發環境初始化、敏感資料掃描 |
| [`pyproject.toml`](pyproject.toml) | 統一設定：Ruff linter、pytest、Mypy、Commitizen |

---

## ⚡ 快速開始

### 方式一：一鍵初始化（推薦）

```bash
# 複製專案
git clone https://github.com/hank3160-ux/engineering-playbook-system.git
cd engineering-playbook-system

# 一鍵初始化開發環境
# 此腳本會自動完成以下步驟：
#   1. 檢查 Python 版本（需 3.11+）
#   2. 建立虛擬環境 .venv
#   3. 安裝所有依賴（含開發工具：ruff, mypy, pre-commit）
#   4. 安裝 pre-commit hooks
#   5. 複製 .env.example → .env
#   6. 執行測試預熱，確認環境正常
bash scripts/dev-setup.sh

# 啟動開發伺服器
source .venv/bin/activate
uvicorn demo.main:app --reload

# 驗證服務是否正常
curl -i http://localhost:8000/health
# 預期回應：
# HTTP/1.1 200 OK
# x-request-id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
# x-process-time-ms: 1.23
# {"status":"ok","version":"2.0.0","uptime_seconds":5.67,"timestamp":"2026-04-30T..."}
```

### 方式二：手動安裝

```bash
# 複製專案
git clone https://github.com/hank3160-ux/engineering-playbook-system.git
cd engineering-playbook-system

# 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# 安裝依賴
pip install -r demo/requirements.txt

# 啟動服務
uvicorn demo.main:app --reload

# 健康檢查
curl http://localhost:8000/health
```

---

## 🐳 Docker 部署

```bash
# 一鍵啟動 API 服務（port 8000）與文件站（port 8080）
docker compose up --build

# API 健康檢查
curl http://localhost:8000/health

# 開啟文件站
# 瀏覽器打開 http://localhost:8080

# 背景執行
docker compose up -d --build

# 停止服務
docker compose down
```

**Docker 設計特點：**

| 特點 | 說明 |
|------|------|
| Multi-stage Build | 分離建置階段與運行階段，最小化映像體積 |
| 非 root 使用者 | 以 `appuser` 身份運行，降低容器逃逸攻擊面 |
| HEALTHCHECK | 內建健康檢查，每 30 秒自動偵測服務狀態 |
| 無 access log | Uvicorn 關閉預設 access log，由自訂 Middleware 統一記錄 |

---

## 📡 API 文件

啟動服務後，可透過以下方式查看自動生成的 API 文件：

- **Swagger UI**：http://localhost:8000/docs
- **ReDoc**：http://localhost:8000/redoc

### 端點總覽

| 方法 | 路徑 | 說明 | 回應碼 |
|------|------|------|--------|
| `GET` | `/health` | 系統健康檢查（含版本、運行時間、時間戳） | `200` |
| `GET` | `/items/` | 列出所有 Items | `200` |
| `POST` | `/items/` | 建立新 Item（需提供 `name`，`description` 選填） | `201` |
| `GET` | `/items/{item_id}` | 依 ID 取得單一 Item | `200` / `404` |
| `DELETE` | `/items/{item_id}` | 依 ID 刪除 Item | `204` / `404` |

### 請求/回應範例

```bash
# 建立 Item
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "筆記型電腦", "description": "MacBook Pro 16 吋"}'

# 回應：
# {"id": 1, "name": "筆記型電腦", "description": "MacBook Pro 16 吋"}

# 列出所有 Items
curl http://localhost:8000/items/

# 取得單一 Item
curl http://localhost:8000/items/1

# 刪除 Item
curl -X DELETE http://localhost:8000/items/1
```

### 共用 Response Headers

每個回應都會包含以下自訂 Header：

| Header | 說明 | 範例 |
|--------|------|------|
| `X-Request-ID` | 本次請求的唯一追蹤 ID（UUID v4） | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` |
| `X-Process-Time-Ms` | 伺服器處理耗時（毫秒） | `1.23` |

---

## 🧪 測試說明

### 執行測試

```bash
# 執行所有測試（含詳細輸出）
pytest demo/tests/ -v

# 執行特定測試檔案
pytest demo/tests/test_health.py -v      # 健康檢查測試
pytest demo/tests/test_items.py -v       # CRUD 測試
pytest demo/tests/test_database.py -v    # 非同步資料庫測試
```

### 測試覆蓋範圍

| 測試檔案 | 測試數量 | 覆蓋範圍 |
|----------|---------|---------|
| `test_health.py` | 4 個 | `/health` 回應狀態、必要欄位、Process Time Header、404 JSON 回應 |
| `test_items.py` | 7 個 | Items CRUD 完整流程：建立、列表、查詢、刪除、404 錯誤處理 |
| `test_database.py` | 5 個 | 非同步 DB 操作：建立使用者、查詢、停用、不存在的資源處理 |

### 測試設計特點

- **測試隔離**：每個測試前自動重置 in-memory store（透過 `pytest.fixture`）
- **非同步測試**：使用 `pytest-asyncio` + SQLite in-memory，無需真實資料庫
- **零外部依賴**：所有測試可在無網路、無 DB 的環境下執行

---

## 🔒 安全機制

### Pre-commit 安全掃描

`scripts/check-secrets.sh` 作為 pre-commit hook，在每次 commit 前自動掃描以下 8 種敏感資料模式：

| 掃描項目 | 偵測模式 |
|----------|---------|
| 明文密碼 | `password = "..."` |
| 硬編碼 Secret | `secret = "..."` |
| API Key | `api_key = "..."` |
| Token | `token = "..."` |
| 私鑰 | `-----BEGIN PRIVATE KEY-----` |
| AWS Access Key | `AKIA` 開頭的 20 字元字串 |
| GitHub Token | `ghp_` 開頭的 40 字元字串 |
| OpenAI API Key | `sk-` 開頭的 32+ 字元字串 |

### 啟用方式

```bash
# 方式一：透過 pre-commit 框架（推薦，dev-setup.sh 已自動安裝）
pre-commit install

# 方式二：手動安裝為 git hook
cp scripts/check-secrets.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# 手動執行掃描
bash scripts/check-secrets.sh
```

### 完整 Pre-commit 防護鏈

本專案的 `.pre-commit-config.yaml` 設定了四層防護：

```
第一層：基礎檔案檢查
  ├── trailing-whitespace      → 移除行尾空白
  ├── end-of-file-fixer        → 確保檔案以換行結尾
  ├── check-yaml/toml/json     → 驗證設定檔語法
  ├── check-merge-conflict     → 偵測未解決的合併衝突
  ├── check-added-large-files  → 阻擋超過 500KB 的檔案
  └── no-commit-to-branch      → 禁止直接 commit 到 main

第二層：程式碼品質
  ├── ruff --fix               → Linting + 自動修復
  └── ruff-format              → 程式碼格式化

第三層：型別安全
  └── mypy --strict            → 靜態型別檢查（嚴格模式）

第四層：安全掃描
  └── check-secrets.sh         → 8 種敏感資料模式偵測
```

---

## 🏗️ 工程實踐說明

本專案完整示範了以下六項核心工程實踐：

### 1. CI/CD Pipeline — 持續整合與持續部署

```
開發者 commit → pre-commit hooks 本地檢查
    → Push to GitHub → CI Pipeline 自動測試
    → 測試通過 → 文件站自動部署至 GitHub Pages
    → Commitizen 自動更新 CHANGELOG
```

- **CI**（`ci.yml`）：每次 push to main 或 PR 時自動執行 `pytest`
- **文件部署**（`deploy-docs.yml`）：自動將 MkDocs 文件站部署至 GitHub Pages
- **版本管理**（`release.yml`）：使用 Commitizen 解析 Conventional Commits，自動生成 CHANGELOG

### 2. 容器化（Containerization）

- **Multi-stage Build**：分離建置階段（安裝依賴）與運行階段（只複製必要檔案），最小化映像體積
- **非 root 使用者**：以 `appuser` 身份運行應用程式，降低容器逃逸攻擊面
- **HEALTHCHECK**：Docker 內建健康檢查，每 30 秒偵測 `/health` 端點，確保容器狀態可被 orchestrator 監控

### 3. Middleware 與可觀測性（Observability）

- **Request ID Middleware**：每個請求自動分配唯一 UUID，透過 Python `contextvars` 在整個非同步呼叫鏈中傳遞
- **Process Time Middleware**：自動計算處理耗時，注入 `X-Process-Time-Ms` Header
- **結構化 Logging**：格式為 `timestamp | level | request_id | module | message`，方便 ELK/Datadog 等工具解析

### 4. 三層架構（Layered Architecture）

```
api/       → HTTP 層：路由定義、狀態碼、Request/Response 處理
services/  → 業務層：純 Python 邏輯，不依賴任何 HTTP 框架
schemas/   → 資料層：Pydantic Model，輸入驗證與輸出序列化
```

- 每一層只依賴下一層，不反向依賴
- Service 層可在不啟動 HTTP server 的情況下直接單元測試
- 新增功能只需新增 router + service + schema，不修改現有程式碼（開放封閉原則 OCP）

### 5. 安全優先開發（Security-First）

- **Pre-commit hooks**：四層防護鏈（檔案檢查 → Linting → 型別檢查 → Secret 掃描）
- **Secret 掃描**：自訂腳本偵測 8 種常見敏感資料洩露模式
- **靜態分析**：Ruff linter + Mypy strict 模式，在 CI 層攔截潛在問題

### 6. 架構決策紀錄（ADR）

每個重要的技術決策都記錄在 `docs/playbook/adr/` 中，包含：

| ADR | 決策內容 | 核心理由 |
|-----|---------|---------|
| [ADR-001](docs/playbook/adr/ADR-001-layered-architecture.md) | 三層架構設計 | 解耦業務邏輯與 HTTP 細節，支援獨立測試 |
| [ADR-002](docs/playbook/adr/ADR-002-async-database.md) | 非同步資料庫 | SQLAlchemy 2.0 async + asyncpg，提升 I/O 效能 |
| [ADR-003](docs/playbook/adr/ADR-003-cicd-design.md) | CI/CD 設計 | GitHub Actions 原生整合，零額外基礎設施成本 |

---

## 📋 如何使用 Template 建立新服務

`template/` 是一個可直接複製的標準 Python 專案模板，包含三層架構、資料庫層、環境變數管理：

```bash
# 1. 複製模板
cp -r template/ ../your-new-service
cd ../your-new-service

# 2. 設定環境變數
cp .env.example .env
# 編輯 .env，填入實際的資料庫連線字串等設定

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 啟動服務
uvicorn app.main:app --reload

# 5. 驗證
curl -i http://localhost:8000/health
```

**Template 內建功能：**

| 功能 | 檔案 | 說明 |
|------|------|------|
| 路由層 | `app/api/health.py` | FastAPI Router 範例 |
| 業務層 | `app/services/health_service.py` | 純 Python 業務邏輯 |
| 資料層 | `app/schemas/health.py` | Pydantic 資料結構 |
| 資料庫 | `app/database/` | SQLAlchemy 2.0 非同步連線 + ORM Model + CRUD |
| 設定管理 | `app/config/settings.py` | pydantic-settings 環境變數管理 |
| 測試 | `tests/test_health.py` | pytest 測試範例 |

---

## 📚 本地文件站預覽

```bash
# 安裝 MkDocs Material
pip install mkdocs-material

# 啟動本地預覽伺服器
mkdocs serve
# 開啟瀏覽器 http://127.0.0.1:8000

# 或透過 Docker Compose（port 8080）
docker compose up docs
# 開啟瀏覽器 http://localhost:8080
```

---

## 📝 版本紀錄

| 版本 | 重點更新 |
|------|---------|
| **v2.0.0** | 🏆 Golden Release：MIT License、面試展示優化、維護者感言、正式封存 |
| v1.6.0 | 架構視覺化：Mermaid 時序圖、Commitizen 自動 CHANGELOG、badges 優化、型別全覆蓋 |
| v1.5.0 | 純粹工程架構：pre-commit、ADR ×3、dev-setup.sh、Item CRUD demo、擴充指南 |
| v1.4.0 | 生產級可靠性：Request ID Middleware、非同步 DB 測試、Dev Container、Reliability Playbook |
| v1.3.0 | 極致自動化：cookiecutter、SQLAlchemy async DB 層、技術架構白皮書 |
| v1.2.0 | 實戰驗證：Mypy 型別檢查、完整 type hints、badges |
| v1.1.0 | 專案治理：Issue/PR 模板、GitHub Pages 自動部署、pyproject.toml、CONTRIBUTING.md |
| v1.0.0 | 正式穩定版：Docker 化、資安規範、pre-commit 掃描、完整 Playbook |
| v0.3.0 | CI/CD、三層架構模板、MkDocs 文件站 |
| v0.1.0 | 基礎骨架：FastAPI MVP、Playbook、SSOT 結構 |

---

## 🎯 給面試官的閱讀指南

這個 repository 是我工程思維的完整展示。以下是建議的閱讀路徑：

| 想了解的面向 | 建議閱讀 | 你會看到什麼 |
|-------------|---------|-------------|
| **技術決策能力** | [`docs/playbook/adr/`](docs/playbook/adr/) | 三份 ADR 記錄了層次架構、非同步資料庫、CI/CD 的選擇原因，以及考慮過但拒絕的替代方案 |
| **自動化治理能力** | [`.github/workflows/`](.github/workflows/) | CI 測試、GitHub Pages 自動部署、CHANGELOG 自動生成、pre-commit hooks 完整防護鏈 |
| **Clean Architecture 實踐** | [`demo/`](demo/) | 三層分離（api / services / schemas）、Request ID 追蹤、結構化 Logging、全域 Exception Handler，每個設計都有對應的測試 |
| **工程規範體系** | [`docs/playbook/`](docs/playbook/) | 從命名規範、Git Commit、架構設計、可觀測性到災難復原，五份文件構成一套可執行的工程文化 |
| **容器化與部署** | [`demo/Dockerfile`](demo/Dockerfile) + [`docker-compose.yml`](docker-compose.yml) | Multi-stage build、非 root 使用者、HEALTHCHECK、一鍵啟動 |

---

## 🤝 貢獻指南

所有變更請遵循以下流程：

1. Fork 本專案
2. 建立功能分支：`git checkout -b feat/your-feature`
3. 遵循 [Conventional Commits](https://www.conventionalcommits.org/) 規範撰寫 commit message
4. 確保所有測試通過：`pytest demo/tests/ -v`
5. 確保 pre-commit hooks 通過：`pre-commit run --all-files`
6. 提交 Pull Request

詳細規範請參考 [`docs/playbook/01-standard-workflow`](https://hank3160-ux.github.io/engineering-playbook-system/playbook/01-standard-workflow/)。

---

## 💬 開發歷程

EPS 從一個空的 Git 骨架，歷經十個迭代，演進為一套涵蓋規範文件、可執行示範、自動化測試、容器化部署、靜態分析、架構決策紀錄與資料庫層的完整工程體系。

每一個決策都有其原因，記錄在 [`docs/playbook/adr/`](docs/playbook/adr/)。每一行程式碼都有對應的測試與文件，確保下一位接手的工程師不需要猜測。

這個專案是人與 AI 協作的產物。感謝 Kiro 在每一個迭代中提供精準的工程建議、嚴謹的型別標注與一致的架構思維；感謝每一位閱讀這份 repository 的開發者，你們的目光是讓這份工作有意義的原因。

EPS 不是一個完成品，而是一個持續演進的基準線。它應該被挑戰、被修正、被超越。這才是工程文化真正的樣子。

---

*v2.0.0 Golden Release — Maintained with SSOT principle. GitHub is the source of truth.*
