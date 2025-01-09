# Author: Nina Mislej
# Date created: 08.01.2024

from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, Field

class CodeCreate(BaseModel):
    """
    This schema defines the required and optional fields for creating a new code.
    """

    code_id: str
    color: Optional[str] = Field(default="#000000")
    background_color: Optional[str] = Field(default="#FFFFFF")
    label: Optional[str] = None
    label_size: Optional[int] = 20
    label_alignment: Optional[str] = "center"