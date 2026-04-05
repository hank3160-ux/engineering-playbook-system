# Engineering Playbook System

> v1.0 穩定版 — 以 GitHub 為核心的單一事實來源（SSOT）平台，統一管理開發規範、流程自動化與可驗證的 MVP 示範。

![CI](https://github.com/hank3160-ux/engineering-playbook-system/actions/workflows/ci.yml/badge.svg)

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

---

## Quick Start

```bash
# 安裝依賴並啟動
pip install -r demo/requirements.txt
uvicorn demo.main:app --reload

# 驗證（Response Header 含 X-Process-Time-Ms）
curl -i http://localhost:8000/health
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

## Contributing

所有變更請遵循 [`playbook/01-standard-workflow.md`](playbook/01-standard-workflow.md) 中定義的規範，並透過 Pull Request 提交。

---

## Changelog

| 版本 | 說明 |
|------|------|
| v1.0.0 | 正式穩定版：Docker 化、資安規範、pre-commit 掃描、完整 Playbook |
| v0.3.0 | CI/CD、三層架構模板、MkDocs 文件站 |
| v0.2.0 | ProcessTimeMiddleware、Exception Handler、pydantic-settings |
| v0.1.0 | 基礎骨架：FastAPI MVP、Playbook、SSOT 結構 |

---

*v1.0 穩定版 — Maintained with SSOT principle. GitHub is the source of truth.*
