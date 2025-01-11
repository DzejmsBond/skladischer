# Author: Nina Mislej
# Date created: 5.12.2024

# GraphQL dependencies.
from ariadne import QueryType, ObjectType
from typing import List, Dict, Optional

# Internal dependencies.
from ...helpers.error import ErrorResponse as Err
from ...services import item_utils as utils
from ...schemas import item_schemas

query = QueryType()
items = ObjectType("Item")

@query.field("items")
async def resolve_items(_, info, user_id: str, storage_name: str, filtering: dict):
    """
       Resolver for fetching and filtering items in a storage.
    """
    try:
        flt = item_schemas.ItemFilter(**filtering)
    except Exception as e:
        raise Exception(f"This filter does not adhere to the filtering possibilities.")

    result = await utils.filter_items(user_id, storage_name, flt)
    if isinstance(result, Err):
        raise Exception(f"{result.message}")
    return result

@query.field("reachable")
def resolve_reachable(*_):
    return "GraphQL is reachable."