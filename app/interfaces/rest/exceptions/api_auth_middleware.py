# app/interfaces/rest/middleware/api_auth.py
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.application.services.api_auth_service import ApiAuthService
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_api_key(auth_service: ApiAuthService):
    async def verify_key(api_key: str = Security(api_key_header)) -> str:
        logger.debug(f"Validating API key: {api_key[:5]}...")
        if auth_service.validate_api_key(api_key):
            return api_key
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return verify_key