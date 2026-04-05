# Engineering Playbook System

> v1.4.0 (Stable) — 以 GitHub 為核心的單一事實來源（SSOT）平台，統一管理開發規範、流程自動化與可驗證的 MVP 示範。

📖 **文件站**：[https://hank3160-ux.github.io/engineering-playbook-system](https://hank3160-ux.github.io/engineering-playbook-system)

![CI](https://github.com/hank3160-ux/engineering-playbook-system/actions/workflows/ci.yml/badge.svg?branch=main)
![Deploy Docs](https://github.com/hank3160-ux/engineering-playbook-system/actions/workflows/deploy-docs.yml/badge.svg?branch=main)
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-v1.4.0-indigo)

---

## Vision

打造一套可執行、可驗證、可演進的工程標準體系：

- 所有規範以 Markdown 文件存活於 `playbook/`，版本由 Git 管控
- 所有示範以可運行的程式碼存活於 `demo/`，確保文件與實作一致
- 任何變更皆透過 Pull Request 審查，保持 SSOT 原則

---

## Architecture

```
engineering-playbook-system/
│
├── .github/workflows/
│   └── ci.yml                          # GitHub Actions CI（push to main 自動測試）
│
├── playbook/                           # 工程規範文件（SSOT）
│   ├── 01-standard-workflow.md         # 命名、Git Commit、環境安全
│   ├── 02-architecture-and-quality.md  # 架構規範、錯誤處理、日誌標準
│   └── 03-observability-and-security.md # 可觀測性、SLI/SLO、資安防禦
│
├── demo/                               # 可執行的 MVP 示範
│   ├── Dockerfile                      # Multi-stage build
│   ├── main.py                         # FastAPI 入口（middleware & exception handler）
│   ├── logger.py                       # 統一 logging 設定
│   ├── requirements.txt                # 依賴清單
│   └── tests/
│       └── test_health.py              # pytest 測試
│
├── template/                           # 標準 Python 專案模板
│   ├── app/
│   │   ├── main.py                     # FastAPI 入口（組裝層）
│   │   ├── logger.py                   # logging 模組
│   │   ├── api/health.py               # 路由層
│   │   ├── services/health_service.py  # 業務邏輯層
│   │   ├── schemas/health.py           # Pydantic 資料結構
│   │   └── config/settings.py          # pydantic-settings 環境變數管理
│   ├── tests/test_health.py            # pytest 範例
│   ├── .env.example                    # 環境變數範本
│   └── requirements.txt
│
├── scripts/
│   └── check-secrets.sh                # Pre-commit 敏感資料掃描
│
├── docker-compose.yml                  # 一鍵啟動 API + Docs
├── mkdocs.yml                          # MkDocs Material 文件站設定
└── README.md                           # 專案首頁（本文件）
```

### 資料流

```
開發者
  │
  ├─► scripts/check-secrets.sh  ──► Pre-commit 安全掃描
  │
  ├─► playbook/  ──► 規範定義（命名、Commit、架構、資安）
  │
  └─► demo/      ──► 實作驗證（FastAPI /health API）
                        │
                        └─► GitHub Actions CI（自動測試）
```

---

## 目錄導覽

| 路徑 | 說明 |
|------|------|
| [`playbook/01-standard-workflow.md`](playbook/01-standard-workflow.md) | 專案命名準則、Git Commit 規範、環境安全指引 |
| [`playbook/02-architecture-and-quality.md`](playbook/02-architecture-and-quality.md) | 架構規範、錯誤處理機制、日誌追蹤標準 |
| [`playbook/03-observability-and-security.md`](playbook/03-observability-and-security.md) | 可觀測性、SLI/SLO、金鑰管理 SOP、資安防禦清單 |
| [`demo/`](demo/) | FastAPI MVP — ProcessTimeMiddleware、Exception Handler、pytest |
| [`template/`](template/) | 標準 Python 專案模板（三層架構，可直接複製） |
| [`scripts/check-secrets.sh`](scripts/check-secrets.sh) | Pre-commit 敏感資料掃描腳本 |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | 貢獻指南 — 如何使用 template/ 啟動新專案 |
| [`pyproject.toml`](pyproject.toml) | ruff linter 與 pytest 統一設定 |

---

## Quick Start

```bash
# 安裝依賴並啟動
pip install -r demo/requirements.txt
uvicorn demo.main:app --reload

# 驗證（Response Headers 含 X-Request-ID 與 X-Process-Time-Ms）
curl -i http://localhost:8000/health

# 傳入自訂 Request ID（方便分散式追蹤）
curl -i -H "X-Request-ID: my-trace-123" http://localhost:8000/health
```

---

## Docker

```bash
# 一鍵啟動 API（port 8000）與文件站（port 8080）
docker compose up --build

# API 健康檢查
curl http://localhost:8000/health

# 文件站
open http://localhost:8080
```

---

## Using the Template

```bash
cp -r template/ ../your-new-service
cp your-new-service/.env.example your-new-service/.env
pip install -r your-new-service/requirements.txt
uvicorn app.main:app --reload
```

---

## Security

啟用 pre-commit 安全掃描：

```bash
# 安裝為 git hook
cp scripts/check-secrets.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# 或手動執行
bash scripts/check-secrets.sh
```

掃描項目：明文密碼、API key、AWS Access Key、GitHub Token、OpenAI Key、私鑰等。

---

## Local Docs Preview

```bash
pip install mkdocs-material
mkdocs serve
# 開啟 http://127.0.0.1:8000
```

---

## Engineering Practices

此專案完整示範了以下五項核心工程實踐：

**1. CI/CD Pipeline**
GitHub Actions 在每次 push to main 時自動執行 pytest，並將 MkDocs 文件站部署至 GitHub Pages，實現從 commit 到上線的全自動化流程。

**2. Containerization with Docker**
採用 Multi-stage build 最小化映像體積，以非 root 使用者運行降低攻擊面，並配置 HEALTHCHECK 確保容器健康狀態可被 orchestrator 監控。

**3. Middleware & Observability**
`ProcessTimeMiddleware` 自動在每個 Response Header 注入 `X-Process-Time-Ms`，搭配結構化 logging（`key=value` 格式），為 SLI/SLO 監控提供可量測的基礎數據。

**4. Layered Architecture**
`template/` 示範三層分離：`api/`（路由/HTTP 細節）→ `services/`（業務邏輯）→ `schemas/`（Pydantic 資料結構），確保各層職責單一、可獨立測試。

**5. Security-First Development**
`scripts/check-secrets.sh` 作為 pre-commit hook 掃描 8 種常見 secret 洩露模式；`pyproject.toml` 統一 ruff linter 與 mypy 靜態型別檢查，在 CI 層攔截潛在問題。

---

## Contributing

所有變更請遵循 [`playbook/01-standard-workflow.md`](playbook/01-standard-workflow.md) 中定義的規範，並透過 Pull Request 提交。

---

## Changelog

| 版本 | 說明 |
|------|------|
| v1.4.0 | 生產級可靠性：Request ID Middleware、異步 DB 測試、Dev Container、Reliability Playbook |
| v1.3.0 | 極致自動化：cookiecutter、SQLAlchemy async DB 層、技術架構白皮書 |
| v1.2.0 | 實戰驗證：url_checker 服務、mypy 型別檢查、完整 type hints、badges |
| v1.1.0 | 專案治理：Issue/PR 模板、GitHub Pages 自動部署、pyproject.toml、CONTRIBUTING.md |
| v1.0.0 | 正式穩定版：Docker 化、資安規範、pre-commit 掃描、完整 Playbook |
| v0.3.0 | CI/CD、三層架構模板、MkDocs 文件站 |
| v0.2.0 | ProcessTimeMiddleware、Exception Handler、pydantic-settings |
| v0.1.0 | 基礎骨架：FastAPI MVP、Playbook、SSOT 結構 |

---

## A Note on This Journey

EPS 從一個空的 Git 骨架，歷經七個迭代，演進為一套涵蓋規範文件、可執行示範、自動化測試、容器化部署、靜態分析、專案生成與資料庫層的完整工程體系。

每一個決策都有其原因，記錄在 [`playbook/04-technical-decisions.md`](playbook/04-technical-decisions.md)。每一行代碼都有對應的測試與文件，確保下一位接手的工程師不需要猜測。

從今天起，EPS 正式從「開發階段」轉向「長期維護與實踐階段」。它不是一個完成品，而是一個持續演進的基準線 — 隨著團隊的成長、技術的更迭，它應該被挑戰、被修正、被超越。

這才是工程文化真正的樣子。

---

*Maintained with SSOT principle. GitHub is the source of truth.*
