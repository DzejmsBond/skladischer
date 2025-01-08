# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException

from ..schemas import storage_schemas as schema
from ..services import storage_utils as utils
from ..models.storage import Storage
from ..helpers.error import ErrorResponse as Err

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/{user_id}/create-storage", status_code=204)
async def create_storage(user_id: str, storage_schema : schema.StorageCreate):
    result = await utils.create_storage(user_id, storage_schema)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return {"detail": f"Storage successfully created."}

@router.get("/{user_id}/{storage_name}", response_model=Storage)
async def get_storage(user_id: str, storage_name: str):
    result = await utils.get_storage(user_id, storage_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return result

@router.delete("/{user_id}/{storage_name}", status_code=204)
async def delete_storage(user_id: str, storage_name: str):
    result = await utils.delete_storage(user_id, storage_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return {"detail": f"Storage '{storage_name}' successfully deleted."}

@router.put("/{user_id}/{storage_name}/update-name", status_code=204)
async def update_storage_name(user_id: str, storage_name: str, new_name : str):
    result = await utils.update_storage_name(user_id, storage_name, new_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return {"detail": f"Storage successfully updated with name '{new_name}'."}

@router.put("/{user_id}/{storage_name}/empty-storage", status_code=204)
async def empty_storage(user_id: str, storage_name: str, new_name : str):
    result = await utils.empty_storage(user_id, storage_name)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)

    return {"detail": f"Storage successfully emptied."}