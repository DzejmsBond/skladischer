# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException

from ..schemas import user_schemas as schema
from ..services import user_utils as utils
from ..models.user import User

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

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str):
    result = await utils.delete_user(user_id)
    if result:
        print(f"Deleted user with id: {user_id}.")
        return {"detail": "User successfully deleted."}
    else:
        raise HTTPException(status_code=400, detail="User could not be deleted.")
