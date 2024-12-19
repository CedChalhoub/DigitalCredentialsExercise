from datetime import datetime
from typing import List
from uuid import UUID

from app.domain.Credential import Credential
from app.domain.CredentialType import EntityType


class DriversLicense(Credential):
    def __init__(self, issuer_id: UUID, holder_id: str, valid_from: datetime, valid_until: datetime, vehicle_classes: List[str], issuing_province: str):
        super().__init__(issuer_id, holder_id, valid_from, valid_until)
        self._vehicle_classes = vehicle_classes
        self._issuing_province = issuing_province

    def _validate_holder_id(self, holder_id: str) -> None:
        # match the validation for drivers' licenses
        pass

    @property
    def vehicle_classes(self) -> List[str]:
        return self._vehicle_classes

    @property
    def issuing_province(self) -> str:
        return self._issuing_province

    @property
    def authorized_issuers(self) -> List[EntityType]:
        return [EntityType.PROVINCIAL]