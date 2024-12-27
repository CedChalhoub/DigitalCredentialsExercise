from abc import ABC
from datetime import datetime
from typing import List

from app.domain.Credential import Credential
from app.domain.CredentialType import CredentialType
from app.domain.EntityType import EntityType


class Passport(Credential, ABC):
    def __init__(self, issuer_id: str, holder_id: str, valid_from: datetime, valid_until: datetime, nationality: str, issuing_country: str):
        super().__init__(issuer_id, holder_id, valid_from, valid_until)
        self._nationality = nationality
        self._issuing_country = issuing_country

    def _validate_holder_id(self, holder_id: str) -> None:
        # match the validation for passports
        pass

    def get_credential_type(self) -> CredentialType:
        return CredentialType.PASSPORT

    @property
    def nationality(self) -> str:
        return self._nationality

    @property
    def issuing_country(self) -> str:
        return self._issuing_country

    @property
    def authorized_issuers(self) -> List[EntityType]:
        return [EntityType.FEDERAL]
