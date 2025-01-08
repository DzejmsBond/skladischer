# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException

from ..schemas import item_schemas as schema
from ..models.item import Item
from ..services import item_utils as utils
from ..helpers.error import ErrorResponse as Err

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/{user_id}/{storage_name}/create-item", status_code=204)
async def create_item(user_id: str, storage_name: str, item_schema: schema.ItemCreate):
    result = await utils.create_item(user_id, storage_name, item_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return {"detail": "Item successfully created."}

@router.get("/{user_id}/{storage_name}/{item_code}", response_model=Item)
async def get_storage(user_id: str, storage_name: str, item_code: str):
    result = await utils.get_item(user_id, storage_name, item_code)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.delete("/{user_id}/{storage_name}/{item_code}", status_code=204)
async def delete_storage(user_id: str, storage_name: str, item_code: str):
    result = await utils.delete_item(user_id, storage_name, item_code)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return {"detail": f"Item '{item_code}' successfully deleted."}

@router.put("/{user_id}/{storage_name}/update-item", status_code=204)
async def update_storage_name(user_id: str, storage_name: str,  item_code: str, item : schema.ItemUpdate):
    result = await utils.update_item(user_id, storage_name, item_code, item)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return {"detail": f"Item '{item_code}' successfully updated."}