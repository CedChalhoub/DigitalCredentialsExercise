import pytest
from datetime import datetime, UTC

from app.rest.assemblers.passport_assembler import PassportAssembler
from app.domain.enums.credential_status import CredentialStatus
from app.domain.models.passport import Passport


@pytest.fixture
def passport():
    return Passport(
        issuer_id="test-issuer-789",
        holder_id="test-holder-012",
        valid_from=datetime(2024, 1, 1, tzinfo=UTC),
        valid_until=datetime(2034, 12, 31, tzinfo=UTC),
        nationality="Canadian",
        issuing_country="ca"
    )


class TestPassportAssembler:
    def test_given_passport_when_converting_to_dto_then_returns_correct_dto_format(
            self, passport):
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

    def test_given_dto_data_when_converting_to_domain_then_returns_correct_passport(
            self, passport):
        assembler = PassportAssembler()
        dto = {
            "issuer_id":passport.issuer_id,
            "holder_id":passport.holder_id,
            "valid_from":passport.valid_from.isoformat(),
            "valid_until":passport.valid_until.isoformat(),
            "nationality":passport.nationality,
            "issuing_country":passport.issuing_country
        }

        domain_obj = assembler.to_domain(dto)

        assert domain_obj.issuer_id == passport.issuer_id
        assert domain_obj.holder_id == passport.holder_id
        assert domain_obj.valid_from.isoformat() == passport.valid_from.isoformat()
        assert domain_obj.valid_until.isoformat() == passport.valid_until.isoformat()
        assert domain_obj.nationality == passport.nationality
        assert domain_obj.issuing_country == passport.issuing_country
        assert domain_obj.status == CredentialStatus.ACTIVE

    def test_given_revoked_passport_when_converting_to_dto_then_includes_revocation_details(
            self, passport):
        assembler = PassportAssembler()
        passport.revoke("Test revocation")
        dto = assembler.to_dto(passport)

        assert dto.status == CredentialStatus.REVOKED.value
        assert dto.revocation_reason == "Test revocation"
