from abc import ABC
from datetime import datetime

from app.domain.models.credential import Credential
from app.domain.enums.credential_type import CredentialType


class Passport(Credential, ABC):
    def __init__(self, issuer_id: str, holder_id: str, valid_from: datetime, valid_until: datetime, nationality: str, issuing_country: str):
        super().__init__(issuer_id, holder_id, valid_from, valid_until, issuing_country)
        self._nationality = nationality

    def _validate_holder_id(self, holder_id: str) -> None:
        # match the validation for passports
        pass

    def get_credential_type(self) -> CredentialType:
        return CredentialType.PASSPORT

    @property
    def nationality(self) -> str:
        return self._nationality
