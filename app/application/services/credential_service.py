from app.domain.models.credential import Credential
from app.domain.enums.credential_status import CredentialStatus
from app.domain.repositories.credential_repository import AbstractCredentialRepository
from app.domain.enums.credential_type import CredentialType

class CredentialService:
    def __init__(self, repository: AbstractCredentialRepository):
        self._repository = repository

    def get_credential(self, credential_id: str, credential_type: CredentialType, issuing_country: str) -> Credential:
        return self._repository.get_credential(credential_id, credential_type, issuing_country)

    def validate_credential(self, credential_id: str, credential_type: CredentialType, issuing_country: str) -> CredentialStatus:
        return self._repository.get_credential(credential_id, credential_type, issuing_country).status

    def create_credential(self, credential: Credential) -> Credential:
        return self._repository.create_credential(credential)

    def update_credential(self, credential_id: str, issuing_country: str, credential_type: CredentialType, new_status: CredentialStatus, update_reason: str | None):
        credential: Credential = self._repository.get_credential(credential_id, credential_type, issuing_country)
        credential.update_status(new_status, update_reason)
        self._repository.update_credential_status(credential)
        return credential


