from fastapi import APIRouter

from app.application.CredentialService import CredentialService
from app.domain.Credential import Credential

router = APIRouter(prefix="/credentials")
CredentialService = CredentialService()

# TODO: Implement DTO
@router.get("/{credential_id}")
async def get_credential(credential_id: str):
    credential: Credential = CredentialService.get_credential(credential_id)
    return credential