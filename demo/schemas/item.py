"""Item schema — 通用 CRUD 示範的資料結構。"""

from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: str = ""


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
