from uuid import UUID

from app.domain.Credential import Credential
from app.domain.CredentialType import EntityType


class Entity:
    def __init__(self, id: UUID, name: str, type: EntityType):
        self._id = id
        self._name = name
        self._type = type

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> EntityType:
        return self._type

    def can_issue_credential(self, credential: Credential) -> bool:
        return self._type in credential.authorized_issuers

    def verify_credential(self, credential: Credential) -> bool:
        return credential.is_valid()