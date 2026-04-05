# Reliability Checklist — 可靠性測試與災難復原準則

> 版本：1.0.0 | SSOT：GitHub

---

## 1. 負載測試（Load Testing）

### 目標

驗證系統在預期流量下能維持 SLO（延遲 P99 ≤ 500ms，錯誤率 ≤ 0.1%）。

### 工具推薦

| 工具 | 適用場景 |
|------|---------|
| [Locust](https://locust.io/) | Python 撰寫測試腳本，適合團隊維護 |
| [k6](https://k6.io/) | JavaScript 腳本，CI 整合友善 |
| [wrk](https://github.com/wg/wrk) | 快速基準測試，單指令執行 |

### Locust 基礎範例

```python
# locustfile.py
from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(0.5, 2)  # 模擬真實使用者思考時間

    @task(3)
    def health_check(self) -> None:
        self.client.get("/health")

    @task(1)
    def check_url(self) -> None:
        self.client.post("/url-checker/check", json={"url": "https://example.com"})
```

```bash
# 執行：100 個並發使用者，每秒新增 10 個，持續 60 秒
locust -f locustfile.py --headless -u 100 -r 10 -t 60s --host http://localhost:8000
```

### 負載測試通過標準

- P50 延遲 ≤ 100ms
- P99 延遲 ≤ 500ms
- 錯誤率 ≤ 0.1%
- CPU 使用率 ≤ 70%（留有緩衝空間）

---

## 2. 壓力測試（Stress Testing）

### 目標

找出系統的「斷點」— 在什麼流量下開始出現錯誤或延遲劇增。

### 測試策略

```
流量
  │
  │                    ← 斷點（開始出現錯誤）
  │               ╱‾‾‾
  │          ╱‾‾‾
  │     ╱‾‾‾
  │╱‾‾‾
  └──────────────────── 時間
  逐步增加流量，觀察延遲與錯誤率的變化點
```

### 執行步驟

1. 從正常負載的 50% 開始
2. 每 5 分鐘增加 25% 流量
3. 記錄每個階段的 P99 延遲與錯誤率
4. 找到錯誤率超過 1% 的臨界點
5. 斷點流量即為系統容量上限，SLO 應設為其 70%

### 觀察指標

```bash
# 即時監控（搭配 ProcessTimeMiddleware log）
tail -f app.log | grep "duration_ms" | awk -F'duration_ms=' '{print $2}'
```

---

## 3. 災難復原（Disaster Recovery）

### RTO / RPO 定義

| 指標 | 定義 | 建議目標 |
|------|------|---------|
| RTO（Recovery Time Objective） | 從故障到服務恢復的最長可接受時間 | ≤ 15 分鐘 |
| RPO（Recovery Point Objective） | 可接受的最大資料遺失時間範圍 | ≤ 5 分鐘 |

### DR 演練 Checklist

#### 每月執行

- [ ] 模擬 API 服務崩潰：`docker stop playbook-api`，驗證 HEALTHCHECK 觸發重啟
- [ ] 驗證 `/health` 在重啟後 30 秒內恢復回應
- [ ] 確認 log 中有完整的 shutdown / startup 記錄

#### 每季執行

- [ ] 模擬資料庫連線中斷，驗證 `pool_pre_ping=True` 自動重連
- [ ] 從備份還原測試資料庫，驗證 RPO 達標
- [ ] 執行完整的 `docker compose down && docker compose up --build`，驗證冷啟動時間

#### 每年執行

- [ ] 完整 DR 演練：模擬整個環境失效，從零重建服務
- [ ] 驗證 `cookiecutter` 模板可在 30 分鐘內生成並部署新服務
- [ ] 更新 RTO/RPO 目標，反映業務成長

### 快速復原 SOP

```bash
# 1. 確認服務狀態
docker compose ps

# 2. 查看最近 100 行 log
docker compose logs --tail=100 api

# 3. 強制重啟服務
docker compose restart api

# 4. 若映像損壞，重新建置
docker compose up --build --force-recreate api

# 5. 驗證恢復
curl -i http://localhost:8000/health
```

---

## 4. 可靠性設計原則

### Fail Fast

服務啟動時若缺少必要設定（如 `DATABASE_URL`），應立即拋出例外並停止啟動，而非在運行中途才崩潰。pydantic-settings 的型別驗證天然實現此原則。

### Graceful Degradation

當非核心依賴（如外部 API）失敗時，服務應降級而非完全崩潰：

```python
try:
    result = await external_service.call()
except Exception:
    logger.warning("External service unavailable, using fallback")
    result = fallback_value  # 回傳快取或預設值
```

### Circuit Breaker 概念

當下游服務連續失敗超過閾值，暫時停止呼叫（open circuit），避免雪崩效應。推薦使用 [tenacity](https://tenacity.readthedocs.io/) 實作重試與熔斷邏輯。

---

## 5. 可靠性 PR 合併前檢查

- [ ] 新功能已通過負載測試（至少 100 req/s，持續 60 秒）
- [ ] 異常路徑有對應的測試案例
- [ ] 所有外部呼叫有 timeout 設定
- [ ] 資料庫查詢有適當的 index（避免全表掃描）
- [ ] HEALTHCHECK 已驗證可正確反映服務狀態

---

*可靠性不是一次性工作，而是持續的工程實踐。*
