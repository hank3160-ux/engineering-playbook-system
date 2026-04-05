"""
異步資料庫測試範例 — 使用 pytest-asyncio + SQLite in-memory。
測試環境與生產環境完全分離：使用 aiosqlite，無需真實 DB 或外部設定。
"""

from collections.abc import AsyncGenerator
from datetime import datetime, timezone

import pytest
import pytest_asyncio
from sqlalchemy import String, func
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# ---------------------------------------------------------------------------
# 測試專用 Base + Model（與 template/ 完全隔離，不依賴外部 import）
# ---------------------------------------------------------------------------

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )


# ---------------------------------------------------------------------------
# CRUD helpers（測試用，與 template/app/database/crud.py 邏輯相同）
# ---------------------------------------------------------------------------

async def _create_user(db: AsyncSession, username: str, email: str) -> User:
    user = User(username=username, email=email)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def _get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    from sqlalchemy import select  # noqa: PLC0415
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def _get_user_by_username(db: AsyncSession, username: str) -> User | None:
    from sqlalchemy import select  # noqa: PLC0415
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def _deactivate_user(db: AsyncSession, user_id: int) -> User | None:
    user = await _get_user_by_id(db, user_id)
    if user is None:
        return None
    user.is_active = False
    await db.flush()
    return user


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """每個測試取得獨立的 in-memory DB，測試結束自動清除。"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession) -> None:
    user = await _create_user(db_session, username="alice", email="alice@example.com")
    assert user.id is not None
    assert user.username == "alice"
    assert user.is_active is True

    fetched = await _get_user_by_id(db_session, user.id)
    assert fetched is not None
    assert fetched.email == "alice@example.com"


@pytest.mark.asyncio
async def test_get_nonexistent_user_returns_none(db_session: AsyncSession) -> None:
    result = await _get_user_by_id(db_session, user_id=9999)
    assert result is None


@pytest.mark.asyncio
async def test_deactivate_user(db_session: AsyncSession) -> None:
    user = await _create_user(db_session, username="bob", email="bob@example.com")
    deactivated = await _deactivate_user(db_session, user.id)
    assert deactivated is not None
    assert deactivated.is_active is False


@pytest.mark.asyncio
async def test_deactivate_nonexistent_user_returns_none(db_session: AsyncSession) -> None:
    result = await _deactivate_user(db_session, user_id=9999)
    assert result is None


@pytest.mark.asyncio
async def test_get_user_by_username(db_session: AsyncSession) -> None:
    await _create_user(db_session, username="carol", email="carol@example.com")
    user = await _get_user_by_username(db_session, "carol")
    assert user is not None
    assert user.email == "carol@example.com"
