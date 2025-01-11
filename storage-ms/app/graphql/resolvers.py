# Author: Nina Mislej
# Date created: 5.12.2024

# GraphQL dependencies.
from ariadne import QueryType, ObjectType
from typing import List, Dict, Optional

# Internal dependencies.
from ..helpers.error import ErrorResponse as Err
from ..services import item_utils as utils
from ..schemas import item_schemas

query = QueryType()
items = ObjectType("Item")

@query.field("items")
async def resolve_items(_, info, user_id: str, storage_name: str, filtering: dict):
    """
    Resolver for fetching and filtering items in a storage.
    This resolver processes a GraphQL query to retrieve items stored in a specific
    user's storage, applying filtering criteria if provided. It validates the
    filtering input against the `ItemFilter` schema and delegates the filtering
    logic to the utility function `filter_items`.

    Args:
        _ (Any): Placeholder for the parent resolver.
        info (GraphQLResolveInfo): Metadata about the query.
        user_id (str): The identifier of the user owning the storage.
        storage_name (str): The name of the storage to fetch items from.
        filtering (dict): A dictionary containing filtering criteria for items.
            This is validated against the `ItemFilter` schema.

    Raises:
        Exception: If the filtering criteria do not match the `ItemFilter` schema.
        Exception: If the utility function `filter_items` returns an error.

    Returns:
        list[dict]: A list of items that match the filtering criteria. Each item
            is represented as a dictionary, adhering to the `Item` GraphQL schema.
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
    """
       This resolver is used as a simple health check to confirm that the
       GraphQL server is operational. It responds with a fixed string when
       queried.
    """

    return "GraphQL is reachable."