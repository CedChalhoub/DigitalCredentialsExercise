from abc import ABC, abstractmethod

from app.domain.Credential import Credential
from app.api.dto.CredentialDTO import CredentialDTO


class CredentialAssembler(ABC):

    @abstractmethod
    def to_dto(self, credential: Credential) -> CredentialDTO:
        pass

    @abstractmethod
    def to_domain(self, credential_dto: dict) -> Credential:
        pass