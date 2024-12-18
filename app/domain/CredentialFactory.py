from app.domain import Credential
from app.domain.DriversLicense import DriversLicense
from app.domain.Passport import Passport


class CredentialFactory:
    def create(self, credential_type: str) -> Credential:
        match credential_type:
            case "Drivers License": return DriversLicense()
            case "Passport": return Passport()