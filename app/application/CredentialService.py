from fastapi import Depends

from app.domain import Credential
from app.domain.CredentialStatus import CredentialStatus
from app.domain.AbstractCredentialRepository import AbstractCredentialRepository
from app.domain.CredentialType import CredentialType


class CredentialService:
    def __init__(self, repository: AbstractCredentialRepository):
        self._repository = repository

    def get_credential(self, credential_id: str, credential_type: CredentialType) -> Credential:
        return self._repository.get_credential(credential_id, credential_type)

    def verify_credential(self, credential: Credential) -> CredentialStatus:
        pass

    def create_credential(self, credential: Credential) -> Credential:
        return self._repository.create_credential(credential)

