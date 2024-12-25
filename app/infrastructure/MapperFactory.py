from app.domain.CredentialType import CredentialType
from app.infrastructure.DriversLicenseMapper import DriversLicenseMapper
from app.infrastructure.PassportMapper import PassportMapper


class MapperFactory:
    def get_mapper(self, credential_type: CredentialType):
        match credential_type:
            case CredentialType.DRIVERS_LICENSE:
                return DriversLicenseMapper()
            case CredentialType.PASSPORT:
                return PassportMapper()