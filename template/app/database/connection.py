"""
Async database connection — SQLAlchemy 2.x 異步連線設定。
使用 asyncpg 驅動連接 PostgreSQL。

依賴：
    pip install sqlalchemy[asyncio] asyncpg
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config.settings import settings


# ---------------------------------------------------------------------------
# Engine & Session Factory
# ---------------------------------------------------------------------------

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,       # debug=True 時印出 SQL
    pool_pre_ping=True,        # 連線前先 ping，避免 stale connection
    pool_size=10,
    max_overflow=20,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,    # 避免 commit 後需重新 query
    autoflush=False,
)


# ---------------------------------------------------------------------------
# Base Model — 所有 ORM Model 繼承此類
# ---------------------------------------------------------------------------

class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Dependency — FastAPI 路由注入用
# ---------------------------------------------------------------------------

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency，提供 async DB session。

    用法：
        @router.get("/items")
        async def list_items(db: AsyncSession = Depends(get_db_session)):
            ...
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
