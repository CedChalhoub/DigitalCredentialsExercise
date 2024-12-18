from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.application.CredentialService import CredentialService
from app.domain.CredentialDTO import CredentialDTO
from app.domain.Credential import Credential

router = APIRouter(prefix="")
CredentialService = CredentialService()


@router.get("/heartbeat")
async def get_heartbeat():
    return {"message": "Service is up and running"}

# TODO: Implement DTO
@router.get("/credentials/{credential_id}")
async def get_credential(credential_id: str):
    credential: Credential = CredentialService.get_credential(credential_id)
    return credential

@router.post("/credentials", response_model=CredentialDTO)
async def new_credential(credentialDTO: CredentialDTO):

    return JSONResponse(content=credentialDTO.model_dump(), status_code=201)
