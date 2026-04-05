# ADR-002: 異步資料庫選擇

| 欄位 | 內容 |
|------|------|
| 狀態 | Accepted |
| 日期 | 2026-04-05 |
| 決策者 | Engineering Team |

---

## 背景

FastAPI 基於 asyncio，若資料庫操作使用同步驅動（如 psycopg2），會阻塞 event loop，在高並發場景下造成嚴重的效能瓶頸。

## 決策

採用 **SQLAlchemy 2.x + asyncpg** 作為異步資料庫解決方案：

```python
engine = create_async_engine(
    "postgresql+asyncpg://...",
    pool_pre_ping=True,
    pool_size=10,
)
```

Session 透過 FastAPI `Depends` 注入，生命週期由框架管理：

```python
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session
        await session.commit()
```

## 考慮過的替代方案

| 方案 | 拒絕原因 |
|------|---------|
| SQLAlchemy 1.x（同步） | 阻塞 event loop，不適合 async FastAPI |
| Tortoise ORM | 生態系較小，SQLAlchemy 社群更成熟 |
| databases 套件 | 功能較陽春，缺乏完整 ORM 支援 |
| Prisma（Python client） | 仍在早期階段，穩定性不足 |

## 測試策略

生產使用 PostgreSQL + asyncpg，測試使用 SQLite + aiosqlite（in-memory），確保測試環境與生產完全隔離，且無需啟動真實資料庫：

```python
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
```

## 後果

- 正面：資料庫操作不阻塞 event loop，支援高並發
- 正面：`pool_pre_ping=True` 自動處理 stale connection
- 負面：異步 ORM 的 debug 比同步版本複雜
- 演進路徑：加入 Alembic 管理 schema migration
