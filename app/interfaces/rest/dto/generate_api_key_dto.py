from typing import Optional

from pydantic import BaseModel

class GenerateApiKeyDto(BaseModel):
    description: Optional[str] = None