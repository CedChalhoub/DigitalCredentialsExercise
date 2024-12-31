from typing import List

from app.interfaces.rest.dto.credential_dto import CredentialDTO


class DriversLicenseDTO(CredentialDTO):
    vehicle_classes: List[str]
    issuing_region: str
