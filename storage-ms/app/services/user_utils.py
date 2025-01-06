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

    user_dict = user.model_dump(by_alias=True)
    result = await db_users.insert_one(user_dict)
    if not result.acknowledged:
        return None
    return user


async def get_user(user_id : str):
    db_users = await get_users_collection()
    if db_users is None:
        return None

    # TODO: Technically, this is looking for an user which has "_id" : ObjectId equal to "user_id" : str.
    #   We should probably redefine PyObjectId type to support querying by PyObjectId.
    #   And fix this in all upcoming find_one() and related calls.
    result = await db_users.find_one({"_id": user_id})
    if not result:
        return None
    return result


async def delete_user(user_id : str):
    db_users = await get_users_collection()
    if db_users is None:
        return None

    result = await db_users.delete_one({"_id": user_id})
    if not result.acknowledged:
        return None
    return result
