from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.dto.AssemblerRegistry import AssemblerRegistry
from app.application.CredentialService import CredentialService
from app.api.dto.CredentialDTO import CredentialDTO

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
    # credential: Credential = CredentialService.get_credential(credential_id)
    credential: CredentialDTO = CredentialDTO(credential_id=str(id), status="active", credential_type="driversLicense", credential_entity="Provincial", issuee_first_name="John", issuee_last_name="Doe", issuee_address="", drivers_license_type="A")
    return credential

@router.post("/credentials", response_model=CredentialDTO)
async def create_credential(credential_type: str, credential_dto: CredentialDTO, registry: AssemblerRegistry = Depends(get_assembler_registry)):
    return JSONResponse(content=credential_dto.model_dump(), status_code=201)
