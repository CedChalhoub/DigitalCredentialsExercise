from abc import abstractmethod

from app.domain import Credential
from app.infrastructure.DynamoDBCredentialRepository import DynamoDBCredentialRepository


class AbstractCredentialRepository(DynamoDBCredentialRepository):
    @abstractmethod
    def get_credential(self, credential_id: str) -> Credential:
        pass

    @abstractmethod
    def new_credential(self, credential: Credential):
        pass
