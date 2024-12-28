from abc import ABC, abstractmethod

from app.domain.models.credential import Credential
from app.interfaces.rest.dto.credential_dto import CredentialDTO


class CredentialAssembler(ABC):

    @abstractmethod
    def to_dto(self, credential: Credential) -> CredentialDTO:
        pass

    @abstractmethod
    def to_domain(self, credential_dto: dict) -> Credential:
        pass