from abc import ABC, abstractmethod

from app.domain.Credential import Credential


class AbstractCredentialMapper(ABC):
    @abstractmethod
    def to_dynamo(self, credential: Credential) -> dict:
        pass

    @abstractmethod
    def to_domain(self, dynamo_dict: dict) -> Credential:
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass