from fastapi import Depends
from typing import Annotated

from app.domain.credential_repository import AbstractCredentialRepository
from app.infrastructure.database.database_config import DatabaseConfig
from app.infrastructure.database.dynamodb_manager import DynamoDBManager
from app.infrastructure.dynamodb_credential_repository import DynamoDBCredentialRepository
from app.application.credential_service import CredentialService
from app.api.dto.assembler_registry import AssemblerRegistry

def get_db_config() -> DatabaseConfig:
    return DatabaseConfig.from_environment()

def get_db_manager(
    config: Annotated[DatabaseConfig, Depends(get_db_config)]
) -> DynamoDBManager:
    return DynamoDBManager(config)

def get_repository(
    db_manager: Annotated[DynamoDBManager, Depends(get_db_manager)]
) -> AbstractCredentialRepository:
    return DynamoDBCredentialRepository(db_manager)

def get_assembler_registry() -> AssemblerRegistry:
    return AssemblerRegistry()

def get_credential_service(
    repository: Annotated[AbstractCredentialRepository, Depends(get_repository)]
) -> CredentialService:
    return CredentialService(repository)