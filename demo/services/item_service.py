"""
ItemService — 通用 CRUD 業務邏輯示範。
使用 in-memory dict 模擬資料層，展示 service 層的職責分離。
生產環境請替換為 SQLAlchemy CRUD（參考 template/app/database/crud.py）。
"""

from demo.schemas.item import ItemCreate, ItemResponse

# in-memory store（示範用，非生產）
_store: dict[int, ItemResponse] = {}
_next_id: int = 1


def create_item(payload: ItemCreate) -> ItemResponse:
    global _next_id
    item = ItemResponse(id=_next_id, name=payload.name, description=payload.description)
    _store[_next_id] = item
    _next_id += 1
    return item

def get_item(item_id: int) -> ItemResponse | None:
    return _store.get(item_id)


def list_items() -> list[ItemResponse]:
    return list(_store.values())


def delete_item(item_id: int) -> bool:
    if item_id not in _store:
        return False
    del _store[item_id]
    return True
