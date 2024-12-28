from typing import Optional

from pydantic import BaseModel


class CredentialDTO(BaseModel):
    issuer_id: str
    holder_id: str
    valid_from: str # ISO 8601
    valid_until: str # ISO 8601
    status: Optional[str] = 'active'
    suspension_reason: Optional[str] = None
    revocation_reason: Optional[str] = None