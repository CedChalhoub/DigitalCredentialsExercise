from abc import abstractmethod

from app.domain.credential import Credential
from app.domain.credential_type import CredentialType


class AbstractCredentialRepository:
    @abstractmethod
    def get_credential(self, credential_id: str, credential_type: CredentialType) -> Credential:
        pass

    @abstractmethod
    def create_credential(self, credential: Credential):
        pass

    @abstractmethod
    def update_credential_status(self, credential: Credential):
        pass
