from typing import List

from app.api.dto.credential_dto import CredentialDTO


class DriversLicenseDTO(CredentialDTO):
    vehicle_classes: List[str]
    issuing_province: str
