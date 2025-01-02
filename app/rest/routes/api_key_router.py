from fastapi import APIRouter, Depends

from app.application.services.api_auth_service import ApiAuthService
from app.dependencies import get_api_key_service
from app.rest.dto.api_key_dto import ApiKeyDto
from app.rest.dto.generate_api_key_dto import GenerateApiKeyDto


class ApiKeyRouter:
    def __init__(self):
        self._router = APIRouter(prefix="/api-keys")
        self.setup_routes()

    @property
    def router(self):
        return self._router

    def setup_routes(self):
        @self._router.post("", response_model=ApiKeyDto)
        async def generate_api_key(
                request: GenerateApiKeyDto,
                auth_service: ApiAuthService = Depends(get_api_key_service)):
            api_key = auth_service.generate_api_key(request.description)
            print(api_key)
            return {
                "key": api_key.key,
                "description": api_key.description,
                "created_at": api_key.created_at.isoformat(),
                "last_used": api_key.last_used.isoformat() if api_key.last_used else None
            }