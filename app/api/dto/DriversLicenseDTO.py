from typing import List

from app.api.dto.CredentialDTO import CredentialDTO


class DriversLicenseDTO(CredentialDTO):
    vehicle_classes: List[str]
    issuing_province: str
