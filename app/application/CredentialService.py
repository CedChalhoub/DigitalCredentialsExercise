from app.domain import Credential
from app.domain.ICredentialRepository import ICredentialRepository


class CredentialService:
    def __init__(self):
        self._ICredentialRepository = ICredentialRepository()


    def get_credential(self, credential_id: str) -> Credential:
        return self._ICredentialRepository.get_credential(credential_id)