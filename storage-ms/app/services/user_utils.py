# Author: Jure
# Date created: 4.12.2024

from ..schemas import user_schemas as schema
from ..models.user import User
from .database_helpers import get_users_collection
from .error import ErrorResponse as Err
from bson import ObjectId as Id

# TODO: What would be better than None?
#       Returning 'user' seems to be misleading because it is not really part of the result.
async def create_user(user_create : schema.UserCreate):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    display_name = user_create.display_name
    user = User(display_name=display_name, storages=[])
    user_dict = user.model_dump(by_alias=True)
    result = await db_users.insert_one(user_dict)
    if not result.acknowledged:
        return Err(message=f"Creating user failed.")
    # NOTE: await get_user(result.inserted_id)
    return None


async def get_user(user_id : str):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    result = await db_users.find_one({"_id": Id(user_id)})
    if not result:
        return Err(message=f"Getting user '{user_id}' failed.")
    return result


async def delete_user(user_id : str):
    db_users = await get_users_collection()
    if db_users is None:
        return Err(message=f"Cannot get DB collection.")

    result = await db_users.delete_one({"_id": Id(user_id)})
    if not result.acknowledged:
        return Err(message=f"Deleting user '{user_id}' failed.")
    return None
