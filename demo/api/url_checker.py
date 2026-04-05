"""
URL Checker router — 路由層，業務邏輯委派給 service。
"""

from fastapi import APIRouter

from demo.schemas.url_checker import UrlCheckRequest, UrlCheckResponse
from demo.services.url_checker_service import check_url

router = APIRouter(prefix="/url-checker", tags=["URL Checker"])


@router.post("/check", response_model=UrlCheckResponse)
async def check_url_endpoint(payload: UrlCheckRequest) -> UrlCheckResponse:
    """
    檢查網址是否使用 HTTPS 協定。

    - **url**: 待檢查的網址（例如 `https://example.com`）
    """
    return check_url(payload.url)
