# Observability & Security — 可觀測性與資安規範

> 版本：1.0.0 | SSOT：GitHub

---

## 1. 日誌規範

### 格式標準

所有服務使用統一格式，方便 log aggregator（如 CloudWatch、Datadog）解析：

```
YYYY-MM-DDTHH:MM:SS | LEVEL    | module | message | key=value pairs
```

### 必要欄位

每個請求的 log 必須包含：

| 欄位 | 說明 | 範例 |
|------|------|------|
| `method` | HTTP 方法 | `GET` |
| `path` | 請求路徑 | `/health` |
| `status` | HTTP 狀態碼 | `200` |
| `duration_ms` | 處理耗時（毫秒） | `12.34` |

### 禁止出現在 Log 中的資料

- 密碼、API key、token
- 個人識別資訊（PII）：姓名、Email、電話、身分證號
- 信用卡號或任何金融資料

### Log 等級使用規範

```
DEBUG   → 開發環境除錯，正式環境關閉
INFO    → 正常業務事件（請求進入、服務啟動）
WARNING → 可恢復的異常（重試、降級、慢查詢）
ERROR   → 需人工介入（例外捕捉、外部服務失敗）
```

---

## 2. 監控指標：SLIs / SLOs

### 概念定義

- **SLI（Service Level Indicator）**：衡量服務品質的具體指標
- **SLO（Service Level Objective）**：SLI 的目標值，違反時觸發告警
- **SLA（Service Level Agreement）**：對外承諾的服務水準（通常 ≤ SLO）

### 建議 SLIs 與 SLOs

| SLI | 量測方式 | SLO 目標 |
|-----|---------|---------|
| 可用性（Availability） | 成功請求數 / 總請求數 | ≥ 99.9% |
| 延遲（Latency P99） | 第 99 百分位請求耗時 | ≤ 500ms |
| 錯誤率（Error Rate） | 5xx 回應數 / 總請求數 | ≤ 0.1% |
| 健康檢查（Health） | `/health` 回應時間 | ≤ 200ms |

### 實作建議

```python
# 在 ProcessTimeMiddleware 中記錄可量測的指標
logger.info(
    "request | method=%s | path=%s | status=%d | duration_ms=%.2f",
    request.method, request.url.path, response.status_code, duration_ms
)
# 搭配 log aggregator 建立 dashboard 與告警規則
```

---

## 3. 金鑰管理 SOP

### 原則

1. **Zero Secrets in Code** — 任何 secret 絕不出現在原始碼或 git history
2. **Least Privilege** — 每個服務只持有最小必要權限的金鑰
3. **Rotation** — 所有金鑰定期輪換，建議週期 ≤ 90 天

### 金鑰分層管理

| 環境 | 儲存方式 | 注入方式 |
|------|---------|---------|
| Local | `.env`（不 commit） | pydantic-settings 讀取 |
| CI/CD | GitHub Actions Secrets | `${{ secrets.KEY_NAME }}` |
| Production | AWS Secrets Manager / Vault | 環境變數或 SDK 讀取 |

### 緊急洩露處置 SOP

1. **立即撤銷**：在金鑰管理平台撤銷洩露的金鑰
2. **輪換**：產生新金鑰並更新所有使用端
3. **稽核**：檢查 git log，確認洩露範圍
4. **通報**：依公司政策通報資安團隊
5. **事後檢討**：更新 pre-commit hook 防止再次發生

---

## 4. 資安防禦清單

### 4.1 輸入驗證

```python
# 使用 Pydantic 自動驗證輸入，拒絕不合法資料
from pydantic import BaseModel, Field, constr

class CreateItemRequest(BaseModel):
    name: constr(min_length=1, max_length=100)  # 限制長度
    quantity: int = Field(gt=0, le=10000)        # 限制範圍
```

- 所有 API 輸入透過 Pydantic schema 驗證
- 不信任任何來自 client 的資料
- 檔案上傳需驗證 MIME type 與大小上限

### 4.2 Rate Limiting 建議

```python
# 使用 slowapi（基於 limits 的 FastAPI rate limiter）
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/health")
@limiter.limit("60/minute")  # 每 IP 每分鐘最多 60 次
async def health_check(request: Request):
    ...
```

建議限制：
- 公開 API：60 req/min per IP
- 認證 API：300 req/min per user
- 登入端點：5 req/min per IP（防暴力破解）

### 4.3 HTTP 安全標頭

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# 建議加入的 Response Headers
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

### 4.4 依賴安全掃描

```bash
# 定期執行，檢查已知 CVE
pip install pip-audit
pip-audit -r requirements.txt
```

### 4.5 Pre-commit 安全檢查

使用 `scripts/check-secrets.sh` 在 commit 前自動掃描敏感資料（詳見 `scripts/` 目錄）。

---

## 5. PR 合併前資安檢查清單

- [ ] `scripts/check-secrets.sh` 通過（無明文 secret）
- [ ] 所有輸入透過 Pydantic schema 驗證
- [ ] Log 中無 PII 或敏感資料
- [ ] 依賴版本已鎖定並通過 `pip-audit`
- [ ] 無 `DEBUG=true` 出現在正式環境設定

---

*資安規範變更須通知資安負責人，並透過 PR 審查。*
