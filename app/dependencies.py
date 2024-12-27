import os
from fastapi import Depends
from typing import Annotated

from app.domain.credential_repository import AbstractCredentialRepository
from app.infrastructure.dynamodb_credential_repository import DynamoDBCredentialRepository
from app.application.credential_service import CredentialService
from app.api.dto.assembler_registry import AssemblerRegistry

def get_repository() -> AbstractCredentialRepository:
    """Get repository implementation based on environment"""
    repo_type = os.getenv("REPOSITORY_TYPE", "dynamodb").lower()
    match repo_type:
        case "dynamodb":
            return DynamoDBCredentialRepository()
        case _:
            return DynamoDBCredentialRepository()

def get_assembler_registry() -> AssemblerRegistry:
    """Create and return a new assembler registry instance"""
    return AssemblerRegistry()

def get_credential_service(
    repository: Annotated[AbstractCredentialRepository, Depends(get_repository)]
) -> CredentialService:
    """Create and return a new credential service instance"""
    return CredentialService(repository)