from typing import Optional

from pydantic import BaseModel


class CredentialDTO(BaseModel):
    credential_id: str
    valid_from: str # ISO 8601
    valid_until: str # ISO 8601
    issuing_country: str
    status: Optional[str] = 'active'
    suspension_reason: Optional[str] = None
    revocation_reason: Optional[str] = None