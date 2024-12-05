# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import APIRouter
from ..schemas import user_schemas as schema
from ..services import user_utils as utils

router = APIRouter(
    prefix="/useres",
    tags=["users"]
)

@router.post("/create-user")
async def create_user(user_schema : schema.UserCreate):
    result = utils.create_user(user_schema)