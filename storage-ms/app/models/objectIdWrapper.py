# Author: Nina Mislej
# Date created: 5.12.2024

from typing import Any
from bson import ObjectId

def str_to_oid(v: Any):
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    return None

def oid_to_str(oid: ObjectId):
    return str(oid)

