"""
Request context — 使用 contextvars 在同一請求的 async 呼叫鏈中傳遞 request_id。
不需要手動傳參，任何地方 import 後直接取值。
"""

from contextvars import ContextVar

# 每個請求獨立的 context variable，預設值為空字串
request_id_var: ContextVar[str] = ContextVar("request_id", default="")


def get_request_id() -> str:
    return request_id_var.get()
