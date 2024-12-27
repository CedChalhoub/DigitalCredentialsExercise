import pytest
from datetime import datetime, UTC

from app.api.dto.passport_assembler import PassportAssembler
from app.domain.credential_status import CredentialStatus
from app.domain.passport import Passport


@pytest.fixture
def passport():
    return Passport(
        issuer_id="test-issuer-789",
        holder_id="test-holder-012",
        valid_from=datetime(2024, 1, 1, tzinfo=UTC),
        valid_until=datetime(2034, 12, 31, tzinfo=UTC),
        nationality="Canadian",
        issuing_country="Canada"
    )


@pytest.fixture
def passport_dto():
    return {
        "issuer_id": "test-issuer-789",
        "holder_id": "test-holder-012",
        "valid_from": "2024-01-01T00:00:00+00:00",
        "valid_until": "2034-12-31T00:00:00+00:00",
        "nationality": "Canadian",
        "issuing_country": "Canada",
        "status": "active"
    }


class TestPassportAssembler:
    def test_to_dto(self, passport):
        assembler = PassportAssembler()
        dto = assembler.to_dto(passport)

        assert dto.issuer_id == passport.issuer_id
        assert dto.holder_id == passport.holder_id
        assert dto.valid_from == passport.valid_from.isoformat()
        assert dto.valid_until == passport.valid_until.isoformat()
        assert dto.status == passport.status.value
        assert dto.nationality == passport.nationality
        assert dto.issuing_country == passport.issuing_country
        assert dto.suspension_reason is None
        assert dto.revocation_reason is None

    def test_to_domain(self, passport_dto):
        assembler = PassportAssembler()
        domain_obj = assembler.to_domain(passport_dto)

        assert domain_obj.issuer_id == passport_dto["issuer_id"]
        assert domain_obj.holder_id == passport_dto["holder_id"]
        assert domain_obj.valid_from.isoformat() == passport_dto["valid_from"]
        assert domain_obj.valid_until.isoformat() == passport_dto["valid_until"]
        assert domain_obj.nationality == passport_dto["nationality"]
        assert domain_obj.issuing_country == passport_dto["issuing_country"]
        assert domain_obj.status == CredentialStatus.ACTIVE

    def test_to_dto_with_suspension(self, passport):
        assembler = PassportAssembler()
        passport.suspend("Passport suspended pending investigation")
        dto = assembler.to_dto(passport)

        assert dto.status == "suspended"
        assert dto.suspension_reason == "Passport suspended pending investigation"
        assert dto.revocation_reason is None

    def test_to_dto_with_revocation(self, passport):
        assembler = PassportAssembler()
        passport.revoke("Passport revoked due to fraud")
        dto = assembler.to_dto(passport)

        assert dto.status == "revoked"
        assert dto.revocation_reason == "Passport revoked due to fraud"
        assert dto.suspension_reason is None

    def test_to_domain_with_status(self, passport_dto):
        assembler = PassportAssembler()

        passport_dto["status"] = "suspended"
        passport_dto["suspension_reason"] = "Test suspension"
        suspended = assembler.to_domain(passport_dto)
        assert suspended.status == CredentialStatus.ACTIVE

        passport_dto["status"] = "revoked"
        passport_dto["revocation_reason"] = "Test revocation"
        revoked = assembler.to_domain(passport_dto)
        assert revoked.status == CredentialStatus.ACTIVE