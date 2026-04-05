"""
ORM Models — 使用 SQLAlchemy 2.x Mapped 型別語法。
"""

from datetime import datetime, timezone

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class User(Base):
    """使用者資料表。"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
