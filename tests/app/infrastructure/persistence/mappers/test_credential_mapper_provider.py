import pytest
from app.domain.enums.credential_type import CredentialType
from app.infrastructure.persistence.mappers.credential_mapper_provider import CredentialMapperProvider

from app.infrastructure.persistence.mappers.drivers_license_mapper import DriversLicenseMapper
from app.infrastructure.persistence.mappers.passport_mapper import PassportMapper

@pytest.fixture
def mapper_provider():
    return CredentialMapperProvider()

class TestCredentialMapperProvider:
    def test_given_drivers_license_type_when_getting_mapper_then_returns_drivers_license_mapper(
            self, mapper_provider):
        mapper = mapper_provider.get_mapper(CredentialType.DRIVERS_LICENSE)
        assert isinstance(mapper, DriversLicenseMapper)

    def test_given_passport_type_when_getting_mapper_then_returns_passport_mapper(
            self, mapper_provider):
        mapper = mapper_provider.get_mapper(CredentialType.PASSPORT)
        assert isinstance(mapper, PassportMapper)