# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException

from ..schemas import item_schemas as schema
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