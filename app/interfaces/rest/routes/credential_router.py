
from fastapi import APIRouter, Depends, Query, Body
from fastapi.responses import JSONResponse

from app.interfaces.rest.dto.assembler_registry import AssemblerRegistry
from app.interfaces.rest.dto.status_update_dto import StatusUpdateDTO
from app.application.services.credential_service import CredentialService
from app.dependencies import get_credential_service
from app.domain.models.credential import Credential
from app.domain.enums.credential_status import CredentialStatus
from app.domain.enums.credential_type import CredentialType

class CredentialRouter:
    def __init__(self, assembler_registry: AssemblerRegistry):
        self._assembler_registry = assembler_registry
        self._router = APIRouter(prefix="")

        self.setup_routes()

    @property
    def router(self):
        return self._router

    @property
    def assembler_registry(self):
        return self._assembler_registry

    def setup_routes(self):
        @self._router.get("/heartbeat")
        async def get_heartbeat():
            return {"message": "Service is up and running"}

        @self._router.get("/credentials/{credential_id}")
        async def get_credential(
                credential_id: str,
                credential_type: str = Query(..., description="Type of credential to get"),
                service: CredentialService = Depends(get_credential_service)):

            assembler = self.assembler_registry.get_assembler(credential_type)
            credential: Credential = service.get_credential(credential_id, CredentialType(credential_type))

            return assembler.to_dto(credential)

        @self._router.get("/credentials/validate/{credential_id}")
        async def validate_credential(
                credential_id: str,
                credential_type: str = Query(..., description="Type of credential to validate"),
                service: CredentialService = Depends(get_credential_service)):
            credential_status: CredentialStatus = service.validate_credential(credential_id, CredentialType(credential_type))

            return JSONResponse(content={"id": credential_id, "status": credential_status.value},
                                status_code=200)

        @self._router.post("/credentials")
        async def create_credential(
                credential_type: str = Query(..., description="Type of credential to create"),
                credential_dto: dict = Body(...),
                service: CredentialService = Depends(get_credential_service)):

            assembler = self.assembler_registry.get_assembler(credential_type)

            credential: Credential = assembler.to_domain(credential_dto)

            service.create_credential(credential)

            return JSONResponse(content={"message": "Credential created"},
                                status_code=201)

        @self._router.patch("/credentials/{credential_id}")
        async def update_credential(
                credential_id: str,
                credential_type: str = Query(..., description="Type of credential to update"),
                status_update_dict: dict = Body(...),
                service: CredentialService = Depends(get_credential_service)):

            service.update_credential(credential_id,
                                                               CredentialType(credential_type),
                                                               CredentialStatus(status_update_dict.get("status")),
                                                               status_update_dict.get("reason"))


            return StatusUpdateDTO(**status_update_dict)
