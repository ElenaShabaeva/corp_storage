from pydantic import BaseModel, Field
from typing import Optional


class ProjectCreateRequestSchema(BaseModel):
    name: str = Field(min_length=1, max_length=65)
    description: Optional[str] = Field(default=None, max_length=200)
