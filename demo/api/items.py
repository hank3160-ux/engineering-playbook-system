"""
Items router — 通用 CRUD 路由示範。
展示 api 層只處理 HTTP 細節，業務邏輯委派給 service。
"""

from fastapi import APIRouter, HTTPException

from demo.schemas.item import ItemCreate, ItemResponse
from demo.services.item_service import create_item, delete_item, get_item, list_items

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/", response_model=list[ItemResponse])
async def get_items() -> list[ItemResponse]:
    """列出所有 Items。"""
    return list_items()


@router.post("/", response_model=ItemResponse, status_code=201)
async def create_new_item(payload: ItemCreate) -> ItemResponse:
    """建立新 Item。"""
    return create_item(payload)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_single_item(item_id: int) -> ItemResponse:
    """依 ID 取得 Item，不存在時回傳 404。"""
    item = get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=204)
async def remove_item(item_id: int) -> None:
    """刪除 Item，不存在時回傳 404。"""
    if not delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
