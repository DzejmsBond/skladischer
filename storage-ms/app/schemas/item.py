# Author: Jure
# Date created: 4.12.2024
# To so DTO.

from pydantic import BaseModel

# TODO: placeholder
class ItemCreate(BaseModel):
    id: int

class ItemUpdate(BaseModel):
    id: int
