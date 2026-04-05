"""
HealthService — 業務邏輯層。
路由層只負責 HTTP 細節，實際邏輯在此處理。
"""

import time
from datetime import datetime, timezone

from app.config.settings import settings
from app.schemas.health import HealthResponse

# 服務啟動時間（模組載入時記錄）
_start_time = time.time()


def get_health() -> HealthResponse:
    """回傳目前服務健康狀態。"""
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        uptime_seconds=round(time.time() - _start_time, 2),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
