# Author: Jure
# Date created: 4.12.2024


from ..schemas import user_schemas as schema
from ..models.user import User
from .database_helpers import get_users_collection

async def create_user(user_create : schema.UserCreate):
    ref_id = user_create.ref_id
    display_name = user_create.display_name
    user = User(ref_id=ref_id, display_name=display_name, storages=[] )
    db_users = await get_users_collection()
    if db_users is None:
        return None

    user_dict = user.model_dump()
    result = await db_users.insert_one(user_dict)
    if not result.acknowledged:
        return None

    user.set_id(result.inserted_id)
    return user
