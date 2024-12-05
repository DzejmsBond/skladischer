# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter, HTTPException
from ..schemas import user_schemas as schema
from ..services import user_utils as utils
from ..models.user import User

router = APIRouter(
    prefix="/useres",
    tags=["users"]
)

@router.post("/create-user", response_model=User)
async def create_user(user_schema : schema.UserCreate):
    result = await utils.create_user(user_schema)
    print(f"Created user: {result}")
    if result is None:
        raise HTTPException(status_code=400, detail="User could not be created.")
    return result