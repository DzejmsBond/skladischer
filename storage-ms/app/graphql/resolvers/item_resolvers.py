# Author: Nina Mislej
# Date created: 5.12.2024

# GraphQL dependencies.
from ariadne import QueryType
from ..services.item_graphql import filter_items

@query.field("items")
async def resolve_items(_, info, user_id: str, storage_name: str, filtering: Optional[dict]):

    result = await filter_items(user_id, storage_name, filtering)
    if isinstance(result, Err):
        raise HTTPException(status_code=result.code, detail=result.message)
    return result