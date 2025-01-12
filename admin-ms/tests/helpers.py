# Author: Nina Mislej
# Date created: 10.01.2025

from app.helpers import get_collection as gc
from pathlib import Path
import secrets

USERNAME = str(secrets.token_hex(32))
PASSWORD = str(secrets.token_hex(32))

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