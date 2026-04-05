"""
Template — FastAPI 應用程式入口。
職責：組裝 app、掛載 middleware、註冊 exception handler、include routers。
業務邏輯請放在 app/services/，資料結構請放在 app/schemas/。
"""

import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from app.api.health import router as health_router
from app.config.settings import settings
from app.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


# ---------------------------------------------------------------------------
# Middleware
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
        request.method, request.url.path, response.status_code, duration_ms,
    )
    return response


# ---------------------------------------------------------------------------
# Exception Handler
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception | path=%s | error=%s", request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": "An unexpected error occurred"},
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(health_router)
