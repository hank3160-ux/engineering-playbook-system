"""URL Checker — Pydantic schemas。"""

from pydantic import BaseModel, HttpUrl


class UrlCheckRequest(BaseModel):
    url: str


class UrlCheckResponse(BaseModel):
    url: str
    is_https: bool
    message: str
