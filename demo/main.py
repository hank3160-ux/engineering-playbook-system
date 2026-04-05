"""
Engineering Playbook System — FastAPI MVP (v1.4.0)
新增：Request ID Middleware、Trace ID 自動注入 logger
"""

import time
import uuid
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from demo.api.items import router as items_router
from demo.context import get_request_id, request_id_var
from demo.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Engineering Playbook System",
    description="工程標準系統 MVP — SSOT Demo",
    version="1.4.0",
)

_start_time = time.time()


# ---------------------------------------------------------------------------
# Middleware 1 — Request ID：生成並注入 contextvars，寫入 Response Header
# ---------------------------------------------------------------------------

@app.middleware("http")
async def request_id_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    # 優先使用 client 傳入的 X-Request-ID，否則自動生成
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    token = request_id_var.set(request_id)
    try:
        response = await call_next(request)
    finally:
        request_id_var.reset(token)

    response.headers["X-Request-ID"] = request_id
    return response


# ---------------------------------------------------------------------------
# Middleware 2 — Process Time：記錄耗時並寫入 Response Header
# ---------------------------------------------------------------------------

@app.middleware("http")
async def process_time_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)

    response.headers["X-Process-Time-Ms"] = str(duration_ms)
    logger.info(
        "Request completed | method=%s | path=%s | status=%d | duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


# ---------------------------------------------------------------------------
# Exception Handler
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "Unhandled exception | path=%s | error=%s | request_id=%s",
        request.url.path,
        exc,
        get_request_id(),
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "detail": "An unexpected error occurred",
            "request_id": get_request_id(),
        },
    )


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Service starting up — Engineering Playbook System v1.4.0")


@app.on_event("shutdown")
async def on_shutdown() -> None:
    logger.info("Service shutting down")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    timestamp: str


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check() -> HealthResponse:
    """
    回傳系統健康狀態。
    Response Headers:
    - X-Request-ID: 本次請求的唯一追蹤 ID
    - X-Process-Time-Ms: 處理耗時（毫秒）
    """
    uptime = round(time.time() - _start_time, 2)
    now = datetime.now(timezone.utc).isoformat()
    logger.info("Health check requested | uptime=%.2fs", uptime)

    return HealthResponse(
        status="ok",
        version="1.4.0",
        uptime_seconds=uptime,
        timestamp=now,
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(items_router)
