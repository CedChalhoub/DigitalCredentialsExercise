from uuid import UUID

from app.domain import Credential
from app.domain.CredentialStatus import CredentialStatus
from app.domain.AbstractCredentialRepository import AbstractCredentialRepository
from app.domain.CredentialType import CredentialType
from app.domain.Entity import Entity
from app.domain.EntityType import EntityType


class CredentialService:
    def __init__(self, repository: AbstractCredentialRepository):
        self._repository = repository

    def get_credential(self, credential_id: str, credential_type: CredentialType) -> Credential:
        return self._repository.get_credential(credential_id, credential_type)

    def validate_credential(self, credential_id: str, credential_type: CredentialType) -> CredentialStatus:
        credential: Credential = self._repository.get_credential(credential_id, credential_type)
        print(credential)
        return credential.status
    def create_credential(self, credential: Credential) -> Credential:
        return self._repository.create_credential(credential)

