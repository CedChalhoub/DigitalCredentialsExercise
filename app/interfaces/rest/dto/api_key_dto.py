from typing import Optional

from pydantic import BaseModel

class ApiKeyDto(BaseModel):
    key: str
    description: Optional[str] = None
    created_at: str
    last_used: Optional[str] = None