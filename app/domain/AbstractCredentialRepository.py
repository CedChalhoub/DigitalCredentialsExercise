from abc import abstractmethod

from app.domain import Credential
from app.domain.CredentialType import CredentialType


class AbstractCredentialRepository:
    @abstractmethod
    def get_credential(self, credential_id: str, credential_type: CredentialType) -> Credential:
        pass

    @abstractmethod
    def create_credential(self, credential: Credential):
        pass
