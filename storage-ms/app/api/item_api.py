# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException

from ..schemas import item_schemas as schema
from ..services import item_utils as utils
from ..models.item import Item

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/{user_id}/{storage_id}/create-item", response_model=Item)
async def create_item(user_id: str, storage_id: str, item_schema: schema.ItemCreate):
    result = await utils.create_item(user_id, storage_id, item_schema)
    print(f"Created item: {result} in storage {storage_id} of user {user_id}.")
    if result is None:
        raise HTTPException(status_code=400, detail="Item could not be created.")
    return result