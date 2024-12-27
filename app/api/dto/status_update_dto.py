from typing import Optional

from pydantic import BaseModel

class StatusUpdateDTO(BaseModel):
    status: str
    reason: Optional[str] = None