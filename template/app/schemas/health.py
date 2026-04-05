"""Health endpoint 的 Pydantic schema — 定義輸入/輸出資料結構。"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    uptime_seconds: float
    timestamp: str
