import pytest
from datetime import datetime, UTC, timedelta
from app.domain.credential import Credential
from app.domain.credential_status import CredentialStatus
from app.domain.credential_type import CredentialType
from app.domain.entity_type import EntityType
from app.domain.exceptions.credential.expired_credential_exception import ExpiredCredentialException
from typing import List


class ConcreteTestCredential(Credential):
    def _validate_holder_id(self, holder_id: str) -> None:
        pass

    def get_credential_type(self) -> CredentialType:
        return CredentialType.DRIVERS_LICENSE

    @property
    def authorized_issuers(self) -> List[EntityType]:
        return [EntityType.PROVINCIAL]


@pytest.fixture
def valid_dates():
    now = datetime.now(UTC)
    return {
        'valid_from': now,
        'valid_until': now + timedelta(days=365)
    }


@pytest.fixture
def credential(valid_dates):
    return ConcreteTestCredential(
        issuer_id="test-issuer",
        holder_id="test-holder",
        valid_from=valid_dates['valid_from'],
        valid_until=valid_dates['valid_until']
    )


class TestCredentialBase:
    def test_create_credential(self, credential, valid_dates):
        assert credential.issuer_id == "test-issuer"
        assert credential.holder_id == "test-holder"
        assert credential.valid_from == valid_dates['valid_from']
        assert credential.valid_until == valid_dates['valid_until']
        assert credential.status == CredentialStatus.ACTIVE

    def test_timezone_aware_dates(self):
        with pytest.raises(ValueError, match="valid_from must be timezone-aware"):
            ConcreteTestCredential(
                issuer_id="test",
                holder_id="test",
                valid_from=datetime.now(),
                valid_until=datetime.now(UTC)
            )

        with pytest.raises(ValueError, match="valid_until must be timezone-aware"):
            ConcreteTestCredential(
                issuer_id="test",
                holder_id="test",
                valid_from=datetime.now(UTC),
                valid_until=datetime.now()
            )

    def test_suspend_credential(self, credential):
        credential.suspend("Test suspension")
        assert credential.status == CredentialStatus.SUSPENDED
        assert credential.suspension_reason == "Test suspension"
        assert credential.revocation_reason is None

    def test_revoke_credential(self, credential):
        credential.revoke("Test revocation")
        assert credential.status == CredentialStatus.REVOKED
        assert credential.revocation_reason == "Test revocation"
        assert credential.suspension_reason is None

    def test_reinstate_credential(self, credential):
        credential.suspend("Test suspension")
        credential.reinstate()
        assert credential.status == CredentialStatus.ACTIVE
        assert credential.suspension_reason is None
        assert credential.revocation_reason is None

    def test_is_valid(self, credential):
        assert credential.is_valid() is True

        credential.suspend("Test")
        assert credential.is_valid() is False

        credential.reinstate()
        assert credential.is_valid() is True

        credential.revoke("Test")
        assert credential.is_valid() is False

    def test_is_valid_dates(self, valid_dates):
        # Test past credential
        past_credential = ConcreteTestCredential(
            issuer_id="test",
            holder_id="test",
            valid_from=valid_dates['valid_from'] - timedelta(days=730),
            valid_until=valid_dates['valid_from'] - timedelta(days=365)
        )
        with pytest.raises(ExpiredCredentialException):
            past_credential.is_valid()

        # Test future credential
        future_credential = ConcreteTestCredential(
            issuer_id="test",
            holder_id="test",
            valid_from=valid_dates['valid_from'] + timedelta(days=365),
            valid_until=valid_dates['valid_from'] + timedelta(days=730)
        )
        assert future_credential.is_valid() is False

    def test_update_status(self, credential):
        credential.update_status(CredentialStatus.SUSPENDED, "Test suspension")
        assert credential.status == CredentialStatus.SUSPENDED
        assert credential.suspension_reason == "Test suspension"

        credential.update_status(CredentialStatus.ACTIVE, None)
        assert credential.status == CredentialStatus.ACTIVE
        assert credential.suspension_reason is None

        credential.update_status(CredentialStatus.REVOKED, "Test revocation")
        assert credential.status == CredentialStatus.REVOKED
        assert credential.revocation_reason == "Test revocation"