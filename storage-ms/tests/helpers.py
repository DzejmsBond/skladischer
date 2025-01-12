# Author: Nina Mislej
# Date created: 10.01.2025

from app.helpers import get_collection as gc
from pathlib import Path
import secrets

USERNAME = str(secrets.token_hex(32))
NEW_USERNAME = str(secrets.token_hex(32))
QUERY_PATH = Path(__file__).resolve().parent / 'helpers.graphql'

# TODO: This should be included when the app reaches production.
#       Testing shouldn't be done on the same database.
#       It seems that this function should not be async but it can mimic one!
def get_collection():
    """
    This function mimics the behavior of an async function and returns
    the database collection using a helper.

    Returns:
        Collection: The database collection instance.
    """

    return gc()

def generate_item_code():
    """
    This function mimics the behavior of the code generation call
    that is routed to another microservice.

    Returns:
        str: 'This is a test code id.' string used for testing.
    """

    return "This is a test code id."

def get_filter_vars(user_id, storage_name, name, amount):
    return {
        "user_id": user_id,
        "storage_name": storage_name,
        "filtering": {
            "name": name,
            "amount": amount
        }
    }