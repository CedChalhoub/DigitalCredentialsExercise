from fastapi import APIRouter, Depends, Query, Body
from fastapi.responses import JSONResponse

from app.api.dto.AssemblerRegistry import AssemblerRegistry
from app.api.dto.DriversLicenseDTO import DriversLicenseDTO
from app.api.dto.PassportDTO import PassportDTO
from app.application.CredentialService import CredentialService
from app.api.dto.CredentialDTO import CredentialDTO
from app.dependencies import get_credential_service
from app.domain.Credential import Credential
from app.domain.CredentialType import CredentialType

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

        # TODO: Implement DTO
        @self._router.get("/credentials/{credential_id}")
        async def get_credential(
                credential_id: str,
                credential_type: str = Query(..., description="Type of credential to get"),
                service: CredentialService = Depends(get_credential_service)):

            credential: Credential = service.get_credential(credential_id, CredentialType(credential_type))
            print(credential)
            # TODO: Map credential domain model to response dto to show specific info

            return credential

        @self._router.post("/credentials")
        async def create_credential(
                credential_type: str = Query(..., description="Type of credential to create"),
                credential_dto: dict = Body(...),
                service: CredentialService = Depends(get_credential_service)):

            assembler = self.assembler_registry.get_assembler(credential_type)

            credential: Credential = assembler.to_domain(credential_dto)

            service.create_credential(credential)

            return JSONResponse(content={"message": "Credential created"}, status_code=201)
