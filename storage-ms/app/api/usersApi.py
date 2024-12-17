# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException
from ..schemas import user_schemas as schema
from ..services import user_utils as utils
from ..models.user import User
from ..models.storage import Storage

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/create-user", response_model=User)
async def create_user(user_schema : schema.UserCreate):
    result = await utils.create_user(user_schema)
    print(f"Created user: {result}")
    if result is None:
        raise HTTPException(status_code=400, detail="User could not be created.")
    return result

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    result = await utils.get_user(user_id)
    print(f"Got user: {result}")
    if result is None:
        raise HTTPException(status_code=404, detail="User could not be found.")
    return result

@router.post("/{user_id}/create-storage", response_model=Storage)
async def create_storage(user_id: str, storage_schema : schema.StorageCreate):
    result = await utils.create_storage(user_id, storage_schema)
    print(f"Created storage: {result}")
    if result is None:
        raise HTTPException(status_code=400, detail="Storage could not be created.")
    return result
