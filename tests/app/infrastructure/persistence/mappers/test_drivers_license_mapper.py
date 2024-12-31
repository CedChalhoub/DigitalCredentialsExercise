import pytest
from datetime import datetime, UTC
from app.domain.enums.credential_status import CredentialStatus
from app.domain.enums.credential_type import CredentialType
from app.domain.models.drivers_license import DriversLicense
from app.infrastructure.persistence.mappers.drivers_license_mapper import DriversLicenseMapper


@pytest.fixture
def drivers_license():
    return DriversLicense(
        issuer_id="test-issuer-123",
        holder_id="test-holder-456",
        valid_from=datetime(2024, 1, 1, tzinfo=UTC),
        valid_until=datetime(2029, 12, 31, tzinfo=UTC),
        vehicle_classes=["A", "B"],
        issuing_country="ca",
        issuing_region="on"
    )


class TestDriversLicenseMapper:
    def test_to_dynamo(self, drivers_license):
        mapper = DriversLicenseMapper()
        dynamo_item = mapper.to_dynamo(drivers_license)

        assert dynamo_item['PK'] == f'CRED#ca#{drivers_license.issuer_id}'
        assert dynamo_item['SK'] == 'METADATA#drivers_license'
        assert dynamo_item['issuing_country'] == 'ca'
        assert dynamo_item['issuing_region'] == 'on'

    def test_to_domain(self, drivers_license):
        mapper = DriversLicenseMapper()
        dynamo_item = mapper.to_dynamo(drivers_license)

        reconstructed = mapper.to_domain(dynamo_item)

        assert reconstructed.issuer_id == drivers_license.issuer_id
        assert reconstructed.holder_id == drivers_license.holder_id
        assert reconstructed.valid_from == drivers_license.valid_from
        assert reconstructed.valid_until == drivers_license.valid_until
        assert reconstructed.status == drivers_license.status
        assert reconstructed.vehicle_classes == drivers_license.vehicle_classes
        assert reconstructed.issuing_country == drivers_license.issuing_country
        assert reconstructed.issuing_region == drivers_license.issuing_region

    def test_to_dynamo_with_suspension(self, drivers_license):
        mapper = DriversLicenseMapper()
        drivers_license.suspend("Test suspension")
        dynamo_item = mapper.to_dynamo(drivers_license)

        assert dynamo_item['status'] == CredentialStatus.SUSPENDED.value
        assert dynamo_item['suspension_reason'] == "Test suspension"

    def test_to_domain_with_suspension(self, drivers_license):
        mapper = DriversLicenseMapper()
        dynamo_item = {
            'issuer_id': 'test-issuer-123',
            'holder_id': 'test-holder-456',
            'valid_from': '2024-01-01T00:00:00+00:00',
            'valid_until': '2029-12-31T00:00:00+00:00',
            'vehicle_classes': ['A', 'B'],
            'issuing_country': 'CA',
            'issuing_region': 'ON',
            'status': CredentialStatus.SUSPENDED.value,
            'suspension_reason': 'Test suspension',
            'revocation_reason': None
        }

        credential = mapper.to_domain(dynamo_item)
        assert credential.status == CredentialStatus.SUSPENDED
        assert credential.suspension_reason == "Test suspension"
