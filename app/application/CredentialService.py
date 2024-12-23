from app.domain import Credential
from app.domain.CredentialStatus import CredentialStatus
from app.domain.AbstractCredentialRepository import AbstractCredentialRepository


class CredentialService:
    def __init__(self):
        # TODO: Use dependency injection here
        self._abstractCredentialRepository = AbstractCredentialRepository()


    def get_credential(self, credential_id: str) -> Credential:
        return self._abstractCredentialRepository.get_credential(credential_id)

    def verify_credential(self, credential: Credential) -> CredentialStatus:
        pass

    def create_credential(self, credential: Credential) -> Credential:
        return self._abstractCredentialRepository.new_credential(credential)

