# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException
from pydantic.config import JsonDict

from ..schemas import user_schemas as schema
from ..services import user_utils as utils
from ..models.user import User
from ..models.storage import Storage
from ..models.item import Item

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

### USERS ###
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

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str):
    result = await utils.delete_user(user_id)
    if result:
        print(f"Deleted user with id: {user_id}.")
        return {"detail": "User successfully deleted."}
    else:
        raise HTTPException(status_code=400, detail="User could not be deleted.")

### STORAGES ###
@router.post("/{user_id}/create-storage", response_model=Storage)
async def create_storage(user_id: str, storage_schema : schema.StorageCreate):
    result = await utils.create_storage(user_id, storage_schema)
    print(f"Created storage: {result}")
    if result is None:
        raise HTTPException(status_code=400, detail="Storage could not be created.")
    return result

@router.get("/{user_id}/{storage_id}", response_model=Storage)
async def get_storage(user_id: str, storage_id: str):
    result = await utils.get_storage(user_id, storage_id)
    print(f"Got storage: {result}")
    if result is None:
        raise HTTPException(status_code=404, detail="Storage could not be found.")
    return result

@router.delete("/{user_id}/{storage_id}", status_code=204)
async def delete_storage(user_id: str, storage_id: str):
    result = await utils.delete_storage(user_id, storage_id)
    if result:
        print(f"Deleted storage with id: {storage_id} from user: {user_id}.")
        return {"detail": "Storage successfully deleted."}
    else:
        raise HTTPException(status_code=400, detail="Storage could not be deleted.")

### ITEMS ###
@router.post("/{user_id}/{storage_id}/create-item", response_model=Item)
async def create_item(user_id: str, storage_id: str, item_schema: schema.ItemCreate):
    result = await utils.create_item(user_id, storage_id, item_schema)
    print(f"Created item: {result} in storage {storage_id} of user {user_id}.")
    if result is None:
        raise HTTPException(status_code=400, detail="Item could not be created.")
    return result
