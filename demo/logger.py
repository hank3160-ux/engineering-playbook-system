"""
Structured logging module — 統一 logging 設定。
所有服務模組應從此處取得 logger，確保格式一致。
"""

import logging
import sys


def get_logger(name: str, level: str | None = None) -> logging.Logger:
    """
    取得已設定的 logger 實例。

    Args:
        name: logger 名稱，建議使用 __name__
        level: log 等級（DEBUG/INFO/WARNING/ERROR），預設 INFO

    Returns:
        設定完成的 Logger 實例
    """
    logger = logging.getLogger(name)

    # 避免重複添加 handler
    if logger.handlers:
        return logger

    log_level = getattr(logging, (level or "INFO").upper(), logging.INFO)
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
