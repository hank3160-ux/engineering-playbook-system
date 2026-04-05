"""
Health router — 路由層只處理 HTTP 細節，業務邏輯委派給 service。
"""

from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.services.health_service import get_health

router = APIRouter(tags=["System"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    回傳服務健康狀態。
    Response Header `X-Process-Time-Ms` 包含本次請求處理耗時。
    """
    return get_health()
