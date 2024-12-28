import pytest
from app.domain.enums.credential_type import CredentialType
from app.infrastructure.persistence.mappers.mapper_factory import MapperFactory
from app.infrastructure.persistence.mappers.drivers_license_mapper import DriversLicenseMapper
from app.infrastructure.persistence.mappers.passport_mapper import PassportMapper

@pytest.fixture
def mapper_factory():
    return MapperFactory()

class TestMapperFactory:
    def test_get_drivers_license_mapper(self, mapper_factory):
        mapper = mapper_factory.get_mapper(CredentialType.DRIVERS_LICENSE)
        assert isinstance(mapper, DriversLicenseMapper)

    def test_get_passport_mapper(self, mapper_factory):
        mapper = mapper_factory.get_mapper(CredentialType.PASSPORT)
        assert isinstance(mapper, PassportMapper)