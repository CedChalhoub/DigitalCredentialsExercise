# app/dependencies.py
from fastapi import Depends
from typing import Annotated

from app.domain.repositories.credential_repository import AbstractCredentialRepository
from app.domain.repositories.api_key_repository import AbstractApiKeyRepository
from app.infrastructure.persistence.dynamodb.database_config import DatabaseConfig
from app.infrastructure.persistence.dynamodb.dynamodb_manager import DynamoDBManager
from app.infrastructure.persistence.repositories.dynamodb_credential_repository import DynamoDBCredentialRepository
from app.infrastructure.persistence.repositories.dynamodb_api_key_repository import DynamoDBApiKeyRepository
from app.application.services.credential_service import CredentialService
from app.application.services.api_auth_service import ApiAuthService
from app.interfaces.rest.dto.assembler_registry import AssemblerRegistry
from app.interfaces.rest.exceptions.api_auth_middleware import verify_api_key


def get_db_config() -> DatabaseConfig:
    return DatabaseConfig.from_environment()

def get_db_manager(
    config: Annotated[DatabaseConfig, Depends(get_db_config)]
) -> DynamoDBManager:
    return DynamoDBManager(config)

def get_credential_repository(
    db_manager: Annotated[DynamoDBManager, Depends(get_db_manager)]
) -> AbstractCredentialRepository:
    return DynamoDBCredentialRepository(db_manager)

def get_api_key_repository(
    db_manager: Annotated[DynamoDBManager, Depends(get_db_manager)]
) -> AbstractApiKeyRepository:
    return DynamoDBApiKeyRepository(db_manager)

def get_assembler_registry() -> AssemblerRegistry:
    return AssemblerRegistry()

def get_credential_service(
    repository: Annotated[AbstractCredentialRepository, Depends(get_credential_repository)]
) -> CredentialService:
    return CredentialService(repository)

def get_api_key_service(
    repository: Annotated[AbstractApiKeyRepository, Depends(get_api_key_repository)]
) -> ApiAuthService:
    return ApiAuthService(repository)

def get_api_key_verifier():
    auth_service = get_api_key_service(get_api_key_repository(get_db_manager(get_db_config())))
    return verify_api_key(auth_service)