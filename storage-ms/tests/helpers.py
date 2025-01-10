# Author: Nina Mislej
# Date created: 10.01.2025

from app.helpers import get_collection as gc
import secrets

USERNAME = str(secrets.token_hex(32))
NEW_USERNAME = str(secrets.token_hex(32))

# TODO: This should be included when the app reaches production.
#       Testing shouldn't be done on the same database.
#       It seems that this function should not be async but it can mimic one!
def get_collection():
    return gc()