from datetime import datetime, UTC

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.dto.AssemblerRegistry import AssemblerRegistry
from app.application.CredentialService import CredentialService
from app.api.dto.CredentialDTO import CredentialDTO
from app.domain.Credential import Credential


def get_assembler_registry():
    return AssemblerRegistry()

router = APIRouter(prefix="")
CredentialService = CredentialService()


@router.get("/heartbeat")
async def get_heartbeat():
    return {"message": "Service is up and running"}

# TODO: Implement DTO
@router.get("/credentials/{id}")
async def get_credential(id: int):
    credential: Credential = CredentialService.get_credential(id)
    # TODO: Map credential domain model to response dto to show specific info
    return credential

@router.post("/credentials", response_model=CredentialDTO)
async def create_credential(credential_type: str, credential_dto: CredentialDTO, registry: AssemblerRegistry = Depends(get_assembler_registry)):
    credential: Credential = registry.get_assembler(credential_type).to_domain(credential_dto)
    CredentialService.create_credential(credential)
    return JSONResponse(content={"message": "Object created successfully"}, status_code=201)
