from app.domain.credential import Credential
from app.domain.credential_status import CredentialStatus
from app.domain.credential_repository import AbstractCredentialRepository
from app.domain.credential_type import CredentialType

class CredentialService:
    def __init__(self, repository: AbstractCredentialRepository):
        self._repository = repository

    def get_credential(self, credential_id: str, credential_type: CredentialType) -> Credential:
        return self._repository.get_credential(credential_id, credential_type)

    def validate_credential(self, credential_id: str, credential_type: CredentialType) -> CredentialStatus:
        credential: Credential = self._repository.get_credential(credential_id, credential_type)
        return credential.status

    def create_credential(self, credential: Credential) -> Credential:
        return self._repository.create_credential(credential)

    def update_credential(self, credential_id: str, credential_type: CredentialType, new_status: CredentialStatus, update_reason: str):
        credential: Credential = self._repository.get_credential(credential_id, credential_type)
        credential.update_status(new_status, update_reason)
        self._repository.update_credential_status(credential)
        return credential


