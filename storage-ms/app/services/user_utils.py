# Author: Jure
# Date created: 4.12.2024

from ..schemas import user_schemas as schema
from ..models.user import User
from .database_helpers import get_users_collection

async def create_user(user_create : schema.UserCreate):
    ref_id = user_create.ref_id
    display_name = user_create.display_name
    user = User(ref_id=ref_id, display_name=display_name, storages=[] )
    db_users = get_users_collection()
    result = await db_users.insert_one(user.model_dump())
    if result.acknowledged: return None
    return user
