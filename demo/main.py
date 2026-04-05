"""
Engineering Playbook System — FastAPI MVP (v2)
新增：ProcessTimeMiddleware、Global Exception Handler、URL Checker
"""

import time
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from demo.api.url_checker import router as url_checker_router
from demo.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Engineering Playbook System",
    description="工程標準系統 MVP — SSOT Demo",
    version="1.1.0",
)

_start_time = time.time()


# ---------------------------------------------------------------------------
# Middleware — 記錄每個請求的處理耗時，並寫入 Response Header
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
# Exception Handler — 確保所有未捕捉例外回傳 JSON，而非 HTML
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "Unhandled exception | path=%s | error=%s",
        request.url.path,
        exc,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "detail": "An unexpected error occurred",
        },
    )


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Service starting up — Engineering Playbook System v1.1.0")


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
    Response Header `X-Process-Time-Ms` 包含本次請求處理耗時（毫秒）。
    """
    uptime = round(time.time() - _start_time, 2)
    now = datetime.now(timezone.utc).isoformat()
    logger.info("Health check requested | uptime=%.2fs", uptime)

    return HealthResponse(
        status="ok",
        version="1.1.0",
        uptime_seconds=uptime,
        timestamp=now,
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(url_checker_router)
