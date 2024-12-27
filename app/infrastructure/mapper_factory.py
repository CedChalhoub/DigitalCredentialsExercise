from app.domain.credential_type import CredentialType
from app.infrastructure.drivers_license_mapper import DriversLicenseMapper
from app.infrastructure.passport_mapper import PassportMapper


class MapperFactory:
    def get_mapper(self, credential_type: CredentialType):
        match credential_type:
            case CredentialType.DRIVERS_LICENSE:
                return DriversLicenseMapper()
            case CredentialType.PASSPORT:
                return PassportMapper()