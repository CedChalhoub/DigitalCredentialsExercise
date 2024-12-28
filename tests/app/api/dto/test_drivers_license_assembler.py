import pytest
from datetime import datetime, UTC

from app.interfaces.rest.dto.drivers_license_assembler import DriversLicenseAssembler
from app.domain.enums.credential_status import CredentialStatus
from app.domain.models.drivers_license import DriversLicense


@pytest.fixture
def drivers_license():
    return DriversLicense(
        issuer_id="test-issuer-123",
        holder_id="test-holder-456",
        valid_from=datetime(2024, 1, 1, tzinfo=UTC),
        valid_until=datetime(2029, 12, 31, tzinfo=UTC),
        vehicle_classes=["A", "B"],
        issuing_province="ON"
    )


@pytest.fixture
def drivers_license_dto():
    return {
        "issuer_id": "test-issuer-123",
        "holder_id": "test-holder-456",
        "valid_from": "2024-01-01T00:00:00+00:00",
        "valid_until": "2029-12-31T00:00:00+00:00",
        "vehicle_classes": ["A", "B"],
        "issuing_province": "ON",
        "status": "active"
    }


class TestDriversLicenseAssembler:
    def test_to_dto(self, drivers_license):
        assembler = DriversLicenseAssembler()
        dto = assembler.to_dto(drivers_license)

        assert dto.issuer_id == drivers_license.issuer_id
        assert dto.holder_id == drivers_license.holder_id
        assert dto.valid_from == drivers_license.valid_from.isoformat()
        assert dto.valid_until == drivers_license.valid_until.isoformat()
        assert dto.status == drivers_license.status.value
        assert dto.vehicle_classes == drivers_license.vehicle_classes
        assert dto.issuing_province == drivers_license.issuing_province
        assert dto.suspension_reason is None
        assert dto.revocation_reason is None

    def test_to_domain(self, drivers_license_dto):
        assembler = DriversLicenseAssembler()
        domain_obj = assembler.to_domain(drivers_license_dto)

        assert domain_obj.issuer_id == drivers_license_dto["issuer_id"]
        assert domain_obj.holder_id == drivers_license_dto["holder_id"]
        assert domain_obj.valid_from.isoformat() == drivers_license_dto["valid_from"]
        assert domain_obj.valid_until.isoformat() == drivers_license_dto["valid_until"]
        assert domain_obj.vehicle_classes == drivers_license_dto["vehicle_classes"]
        assert domain_obj.issuing_province == drivers_license_dto["issuing_province"]
        assert domain_obj.status == CredentialStatus.ACTIVE

    def test_to_dto_with_suspension(self, drivers_license):
        assembler = DriversLicenseAssembler()
        drivers_license.suspend("License suspended due to violations")
        dto = assembler.to_dto(drivers_license)

        assert dto.status == "suspended"
        assert dto.suspension_reason == "License suspended due to violations"
        assert dto.revocation_reason is None

    def test_to_dto_with_revocation(self, drivers_license):
        assembler = DriversLicenseAssembler()
        drivers_license.revoke("License revoked permanently")
        dto = assembler.to_dto(drivers_license)

        assert dto.status == "revoked"
        assert dto.revocation_reason == "License revoked permanently"
        assert dto.suspension_reason is None

    def test_to_domain_with_status(self, drivers_license_dto):
        assembler = DriversLicenseAssembler()

        # Test suspended status
        drivers_license_dto["status"] = "suspended"
        drivers_license_dto["suspension_reason"] = "Test suspension"
        suspended = assembler.to_domain(drivers_license_dto)
        assert suspended.status == CredentialStatus.ACTIVE  # Initial state is always active

        # Test revoked status
        drivers_license_dto["status"] = "revoked"
        drivers_license_dto["revocation_reason"] = "Test revocation"
        revoked = assembler.to_domain(drivers_license_dto)
        assert revoked.status == CredentialStatus.ACTIVE  # Initial state is always active