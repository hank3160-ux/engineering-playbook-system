"""
Structured logging module — 統一 logging 設定。
自動在每條 log 注入當前請求的 request_id（透過 contextvars）。
"""

import logging
import sys

from demo.context import get_request_id


class RequestIdFilter(logging.Filter):
    """將當前 request_id 注入每條 LogRecord。"""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id() or "-"
        return True


def get_logger(name: str, level: str | None = None) -> logging.Logger:
    """
    取得已設定的 logger 實例。

    Args:
        name:  logger 名稱，建議使用 __name__
        level: log 等級（DEBUG/INFO/WARNING/ERROR），預設 INFO
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_level = getattr(logging, (level or "INFO").upper(), logging.INFO)
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.addFilter(RequestIdFilter())
    handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(request_id)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    ))
    logger.addHandler(handler)
    return logger
