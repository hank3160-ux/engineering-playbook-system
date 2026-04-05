"""
異步資料庫測試範例 — 使用 pytest-asyncio + SQLite in-memory。
測試環境與生產環境完全分離：使用 aiosqlite 取代 asyncpg，無需真實 DB。

依賴：
    pip install pytest-asyncio aiosqlite
"""

import pytest
import pytest_asyncio
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# 使用 SQLite in-memory，測試環境與生產完全隔離
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    每個測試函式取得獨立的 in-memory DB session。
    測試結束後自動清除，確保測試間互不干擾。
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    # 動態 import，避免在沒有 sqlalchemy 時整個測試模組失敗
    from template.app.database.connection import Base  # noqa: PLC0415

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession) -> None:
    """建立使用者後應可查詢到。"""
    from template.app.database.crud import create_user, get_user_by_id  # noqa: PLC0415

    user = await create_user(db_session, username="alice", email="alice@example.com")
    assert user.id is not None
    assert user.username == "alice"
    assert user.is_active is True

    fetched = await get_user_by_id(db_session, user.id)
    assert fetched is not None
    assert fetched.email == "alice@example.com"


@pytest.mark.asyncio
async def test_get_nonexistent_user_returns_none(db_session: AsyncSession) -> None:
    """查詢不存在的 ID 應回傳 None，而非拋出例外。"""
    from template.app.database.crud import get_user_by_id  # noqa: PLC0415

    result = await get_user_by_id(db_session, user_id=9999)
    assert result is None


@pytest.mark.asyncio
async def test_deactivate_user(db_session: AsyncSession) -> None:
    """停用使用者後 is_active 應為 False。"""
    from template.app.database.crud import create_user, deactivate_user  # noqa: PLC0415

    user = await create_user(db_session, username="bob", email="bob@example.com")
    deactivated = await deactivate_user(db_session, user.id)

    assert deactivated is not None
    assert deactivated.is_active is False


@pytest.mark.asyncio
async def test_deactivate_nonexistent_user_returns_none(db_session: AsyncSession) -> None:
    """停用不存在的使用者應回傳 None。"""
    from template.app.database.crud import deactivate_user  # noqa: PLC0415

    result = await deactivate_user(db_session, user_id=9999)
    assert result is None


@pytest.mark.asyncio
async def test_get_user_by_username(db_session: AsyncSession) -> None:
    """依 username 查詢應回傳正確使用者。"""
    from template.app.database.crud import create_user, get_user_by_username  # noqa: PLC0415

    await create_user(db_session, username="carol", email="carol@example.com")
    user = await get_user_by_username(db_session, "carol")

    assert user is not None
    assert user.email == "carol@example.com"
