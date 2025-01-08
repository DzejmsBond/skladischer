# Author: Nina Mislej
# Date created: 07.01.2024
# To so DTO.

from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    amount: Optional[int] = None
    description: Optional[str] = None

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[int] = None
    description: Optional[str] = None