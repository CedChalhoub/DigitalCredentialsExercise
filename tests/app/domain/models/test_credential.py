import pytest
from datetime import datetime, UTC, timedelta
from app.domain.models.credential import Credential
from app.domain.enums.credential_status import CredentialStatus
from app.domain.enums.credential_type import CredentialType


class ConcreteTestCredential(Credential):
    def _validate_issuer_id(self, holder_id: str) -> None:
        pass

    def get_credential_type(self) -> CredentialType:
        return CredentialType.DRIVERS_LICENSE


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
        valid_until=valid_dates['valid_until'],
        issuing_country="CA"
    )


class TestCredentialBase:
    def test_given_valid_credential_data_when_creating_credential_then_creates_with_correct_values(
            self, credential, valid_dates):
        assert credential.issuer_id == "test-issuer"
        assert credential.holder_id == "test-holder"
        assert credential.valid_from == valid_dates['valid_from']
        assert credential.valid_until == valid_dates['valid_until']
        assert credential.issuing_country == "ca"  # Should be lowercase
        assert credential.status == CredentialStatus.ACTIVE

    def test_given_naive_datetime_when_creating_credential_then_raises_value_error(self):
        with pytest.raises(ValueError, match="valid_from must be timezone-aware"):
            ConcreteTestCredential(
                issuer_id="test",
                holder_id="test",
                valid_from=datetime.now(),
                valid_until=datetime.now(UTC),
                issuing_country="CA"
            )

        with pytest.raises(ValueError, match="valid_until must be timezone-aware"):
            ConcreteTestCredential(
                issuer_id="test",
                holder_id="test",
                valid_from=datetime.now(UTC),
                valid_until=datetime.now(),
                issuing_country="CA"
            )

    def test_given_active_credential_when_suspending_then_updates_to_suspended_status(
            self, credential):
        credential.suspend("Test suspension")
        assert credential.status == CredentialStatus.SUSPENDED
        assert credential.suspension_reason == "Test suspension"
        assert credential.revocation_reason is None

    def test_given_active_credential_when_revoking_then_updates_to_revoked_status(
            self, credential):
        credential.revoke("Test revocation")
        assert credential.status == CredentialStatus.REVOKED
        assert credential.revocation_reason == "Test revocation"
        assert credential.suspension_reason is None

    def test_given_suspended_credential_when_reinstating_then_updates_to_active_status(
            self, credential):
        credential.suspend("Test suspension")
        credential.reinstate()
        assert credential.status == CredentialStatus.ACTIVE
        assert credential.suspension_reason is None
        assert credential.revocation_reason is None