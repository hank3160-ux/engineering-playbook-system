"""
UrlCheckerService — 業務邏輯層。
判斷給定網址是否使用 HTTPS 協定。
"""

from demo.schemas.url_checker import UrlCheckResponse


def check_url(url: str) -> UrlCheckResponse:
    """
    檢查網址是否為 HTTPS。

    Args:
        url: 待檢查的網址字串

    Returns:
        UrlCheckResponse 包含檢查結果與說明訊息
    """
    normalized = url.strip().lower()
    is_https = normalized.startswith("https://")

    return UrlCheckResponse(
        url=url,
        is_https=is_https,
        message="Secure (HTTPS)" if is_https else "Insecure — HTTPS required",
    )
