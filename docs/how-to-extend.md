# 如何擴充此架構

本章說明如何從 `template/` 出發，快速開發任何種類的 Web 服務。

---

## 核心概念

每個新功能遵循相同的四步流程：

```
1. schemas/   → 定義資料結構（輸入驗證 + 輸出序列化）
2. services/  → 實作業務邏輯（純 Python，不依賴 HTTP）
3. api/       → 定義路由（HTTP 細節，呼叫 service）
4. main.py    → include_router 掛載
```

---

## 步驟一：從模板建立新服務

```bash
cp -r template/ ../my-new-service
cd ../my-new-service
cp .env.example .env
pip install -r requirements.txt
```

---

## 步驟二：新增一個功能模組

以「文章管理」為例：

### 2a. 定義 Schema

```python
# app/schemas/article.py
from pydantic import BaseModel

class ArticleCreate(BaseModel):
    title: str
    content: str

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
```

### 2b. 實作 Service

```python
# app/services/article_service.py
from app.schemas.article import ArticleCreate, ArticleResponse

_store: dict[int, ArticleResponse] = {}
_next_id = 1

def create_article(payload: ArticleCreate) -> ArticleResponse:
    global _next_id
    article = ArticleResponse(id=_next_id, **payload.model_dump())
    _store[_next_id] = article
    _next_id += 1
    return article
```

### 2c. 定義 Router

```python
# app/api/articles.py
from fastapi import APIRouter, HTTPException
from app.schemas.article import ArticleCreate, ArticleResponse
from app.services.article_service import create_article

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.post("/", response_model=ArticleResponse, status_code=201)
async def create(payload: ArticleCreate) -> ArticleResponse:
    return create_article(payload)
```

### 2d. 掛載 Router

```python
# app/main.py
from app.api.articles import router as articles_router
app.include_router(articles_router)
```

---

## 步驟三：加入資料庫持久化

將 in-memory store 替換為 SQLAlchemy：

```python
# app/database/models.py — 新增 Article model
class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
```

```python
# app/api/articles.py — 注入 DB session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db_session

@router.post("/", response_model=ArticleResponse, status_code=201)
async def create(
    payload: ArticleCreate,
    db: AsyncSession = Depends(get_db_session),
) -> ArticleResponse:
    return await create_article(db, payload)
```

---

## 步驟四：加入測試

```python
# tests/test_articles.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_article() -> None:
    response = client.post("/articles/", json={"title": "Hello", "content": "World"})
    assert response.status_code == 201
    assert response.json()["title"] == "Hello"
```

---

## 常見擴充場景

| 場景 | 需要新增的元件 |
|------|--------------|
| 新增 CRUD 資源 | schema + service + api router |
| 加入認證 | middleware 或 Depends 注入 |
| 加入背景任務 | FastAPI `BackgroundTasks` 或 Celery |
| 加入快取 | Redis + 在 service 層加入 cache decorator |
| 加入 WebSocket | 新增 `@app.websocket()` 路由 |
| 加入排程任務 | APScheduler 或 Celery Beat |

---

## 架構演進路徑

```
MVP（in-memory）
  ↓
加入 SQLAlchemy（持久化）
  ↓
加入 Alembic（schema migration）
  ↓
加入 Redis（快取 / 排程）
  ↓
拆分微服務（每個 domain 獨立部署）
```

每個階段都可以獨立完成，不需要一次到位。
