"""
CRUD helpers — User 資料表的基礎操作。
所有函式接受 AsyncSession，由路由層透過 Depends 注入。
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """依 ID 查詢使用者，不存在時回傳 None。"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """依 username 查詢使用者。"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, email: str) -> User:
    """建立新使用者並回傳已持久化的實例。"""
    user = User(username=username, email=email)
    db.add(user)
    await db.flush()   # 取得 DB 產生的 id，但尚未 commit
    await db.refresh(user)
    return user


async def deactivate_user(db: AsyncSession, user_id: int) -> User | None:
    """停用使用者（軟刪除），不存在時回傳 None。"""
    user = await get_user_by_id(db, user_id)
    if user is None:
        return None
    user.is_active = False
    await db.flush()
    return user
