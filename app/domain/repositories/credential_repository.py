from abc import abstractmethod

from app.domain.models.credential import Credential
from app.domain.enums.credential_type import CredentialType


class AbstractCredentialRepository:
    @abstractmethod
    def get_credential(self, credential_id: str, credential_type: CredentialType, issuing_country: str) -> Credential:
        pass

    @abstractmethod
    def create_credential(self, credential: Credential):
        pass

    @abstractmethod
    def update_credential_status(self, credential: Credential):
        pass
