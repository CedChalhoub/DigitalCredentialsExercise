from abc import ABC
from datetime import datetime
from typing import List

from app.domain.models.credential import Credential
from app.domain.enums.credential_type import CredentialType


class DriversLicense(Credential, ABC):
    def __init__(self, issuer_id: str, holder_id: str, valid_from: datetime, valid_until: datetime, vehicle_classes: List[str], issuing_country: str, issuing_region: str):
        super().__init__(issuer_id, holder_id, valid_from, valid_until, issuing_country)
        self._vehicle_classes = vehicle_classes
        self._issuing_region = issuing_region

    def _validate_issuer_id(self, holder_id: str) -> None:
        # match the validation for drivers' licenses
        pass

    def get_credential_type(self) -> CredentialType:
        return CredentialType.DRIVERS_LICENSE

    @property
    def vehicle_classes(self) -> List[str]:
        return self._vehicle_classes

    @property
    def issuing_region(self) -> str:
        return self._issuing_region


