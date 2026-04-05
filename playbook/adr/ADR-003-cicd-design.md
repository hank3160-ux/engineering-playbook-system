# ADR-003: CI/CD 流程設計

| 欄位 | 內容 |
|------|------|
| 狀態 | Accepted |
| 日期 | 2026-04-05 |
| 決策者 | Engineering Team |

---

## 背景

需要一套自動化流程，確保每次 push 都能：
1. 驗證代碼品質（lint、type check、test）
2. 自動部署文件站，保持文件與代碼同步

## 決策

使用 **GitHub Actions** 實作兩條獨立 pipeline：

### Pipeline 1：CI（`ci.yml`）

觸發條件：push to main、PR to main

```
checkout → setup Python → install deps → pytest
```

- 使用 `actions/setup-python@v5` 的 pip cache 加速
- 測試範圍：`demo/tests/`（含異步 DB 測試）

### Pipeline 2：Deploy Docs（`deploy-docs.yml`）

觸發條件：push to main

```
checkout (fetch-depth=0) → install mkdocs-material → mkdocs gh-deploy
```

- `fetch-depth: 0` 保留完整 git history，供 mkdocs git-dates 插件使用
- 部署至 `gh-pages` 分支，由 GitHub Pages 服務

## 考慮過的替代方案

| 方案 | 拒絕原因 |
|------|---------|
| Jenkins | 需自建維護 CI 伺服器，成本高 |
| CircleCI | 需額外帳號，GitHub Actions 已內建 |
| 單一合併 pipeline | CI 失敗會阻擋文件部署，職責不清 |
| GitLab CI | 需遷移 repository |

## Pre-commit 整合

本地開發透過 `.pre-commit-config.yaml` 在 commit 前執行 ruff、mypy 與 secret 掃描，在 CI 之前提前攔截問題，縮短回饋循環：

```
本地 commit → pre-commit hooks → push → GitHub Actions CI
```

## 後果

- 正面：兩條 pipeline 職責分離，互不阻擋
- 正面：pre-commit + CI 雙重防護，問題在最早期被攔截
- 正面：GitHub Actions 免費額度對開源專案足夠
- 演進路徑：加入 `deploy.yml` 實作正式環境自動部署
