import pytest
from datetime import datetime, UTC
from app.domain.credential_status import CredentialStatus
from app.domain.credential_type import CredentialType
from app.domain.passport import Passport
from app.infrastructure.passport_mapper import PassportMapper


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


class TestPassportMapper:
    def test_to_dynamo(self, passport):
        mapper = PassportMapper()
        dynamo_item = mapper.to_dynamo(passport)

        assert dynamo_item['PK'] == f'CRED#{passport.issuer_id}'
        assert dynamo_item['SK'] == 'METADATA#passport'
        assert dynamo_item['credential_type'] == CredentialType.PASSPORT.value
        assert dynamo_item['issuer_id'] == passport.issuer_id
        assert dynamo_item['holder_id'] == passport.holder_id
        assert dynamo_item['valid_from'] == '2024-01-01T00:00:00+00:00'
        assert dynamo_item['valid_until'] == '2034-12-31T00:00:00+00:00'
        assert dynamo_item['status'] == CredentialStatus.ACTIVE.value
        assert dynamo_item['nationality'] == 'Canadian'
        assert dynamo_item['issuing_country'] == 'Canada'
        assert dynamo_item['version'] == 1

    def test_to_domain(self, passport):
        mapper = PassportMapper()
        dynamo_item = mapper.to_dynamo(passport)

        reconstructed = mapper.to_domain(dynamo_item)

        assert reconstructed.issuer_id == passport.issuer_id
        assert reconstructed.holder_id == passport.holder_id
        assert reconstructed.valid_from == passport.valid_from
        assert reconstructed.valid_until == passport.valid_until
        assert reconstructed.status == passport.status
        assert reconstructed.nationality == passport.nationality
        assert reconstructed.issuing_country == passport.issuing_country

    def test_to_dynamo_with_revocation(self, passport):
        mapper = PassportMapper()
        passport.revoke("Test revocation")
        dynamo_item = mapper.to_dynamo(passport)

        assert dynamo_item['status'] == CredentialStatus.REVOKED.value
        assert dynamo_item['revocation_reason'] == "Test revocation"

    def test_to_domain_with_revocation(self, passport):
        mapper = PassportMapper()
        dynamo_item = {
            'issuer_id': 'test-issuer-789',
            'holder_id': 'test-holder-012',
            'valid_from': '2024-01-01T00:00:00+00:00',
            'valid_until': '2034-12-31T00:00:00+00:00',
            'nationality': 'Canadian',
            'issuing_country': 'Canada',
            'status': CredentialStatus.REVOKED.value,
            'revocation_reason': 'Test revocation',
            'suspension_reason': None
        }

        credential = mapper.to_domain(dynamo_item)
        assert credential.status == CredentialStatus.REVOKED
        assert credential.revocation_reason == "Test revocation"