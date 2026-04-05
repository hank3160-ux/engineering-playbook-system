"""
Settings — 使用 pydantic-settings 管理環境變數。
所有設定從 .env 檔案或環境變數讀取，禁止 hardcode。
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # 應用程式基本資訊
    app_name: str = "your-service-name"
    app_version: str = "0.1.0"
    debug: bool = False

    # 伺服器設定
    host: str = "0.0.0.0"
    port: int = 8000

    # 日誌等級
    log_level: str = "INFO"

    # 資料庫（選用，include_database=yes 時啟用）
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/mydb"


# 單例 — 全域共用同一份設定
settings = Settings()
