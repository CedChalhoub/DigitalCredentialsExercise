from app.domain.enums.credential_type import CredentialType
from app.infrastructure.persistence.mappers.credential_mapper import CredentialMapper
from app.infrastructure.persistence.mappers.drivers_license_mapper import DriversLicenseMapper
from app.infrastructure.persistence.mappers.passport_mapper import PassportMapper


class CredentialMapperProvider:
    def get_mapper(self, credential_type: CredentialType) -> CredentialMapper:
        match credential_type:
            case CredentialType.DRIVERS_LICENSE:
                return DriversLicenseMapper()
            case CredentialType.PASSPORT:
                return PassportMapper()