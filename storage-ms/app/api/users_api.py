# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException

from ..schemas import user_schemas as schema
from ..services import user_utils as utils
from ..models.user import User
from ..services.error import ErrorResponse as Err

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/create-user", status_code=204)
async def create_user(user_schema : schema.UserCreate):
    result = await utils.create_user(user_schema)
    if isinstance(result, Err):
        print(f"Creating user failed.")
        raise HTTPException(status_code=result.code, detail=result.message)

    print(f"Created user: {result}")
    return {"detail": f"User successfully created."}

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    result = await utils.get_user(user_id)
    if isinstance(result, Err):
        print(f"Getting user {user_id} failed.")
        raise HTTPException(status_code=result.code, detail=result.message)

    print(f"Got user: {result}")
    return result

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str):
    result = await utils.delete_user(user_id)
    if isinstance(result, Err):
        print(f"Deleting user {user_id} failed.")
        raise HTTPException(status_code=result.code, detail=result.message)

    print(f"Deleted user with id: {user_id}.")
    return {"detail": "User successfully deleted."}
