import pytest
from datetime import datetime, UTC
from unittest.mock import Mock

from app.application.services.credential_service import CredentialService
from app.domain.enums.credential_status import CredentialStatus
from app.domain.enums.credential_type import CredentialType
from app.domain.models.drivers_license import DriversLicense


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def credential_service(mock_repository):
    return CredentialService(mock_repository)


@pytest.fixture
def sample_drivers_license():
    return DriversLicense(
        credential_id="test-issuer-123",
        valid_from=datetime(2024, 1, 1, tzinfo=UTC),
        valid_until=datetime(2029, 12, 31, tzinfo=UTC),
        vehicle_classes=["A", "B"],
        issuing_country="CA",
        issuing_region="ON"
    )


class TestCredentialService:
    def test_given_valid_credential_id_when_getting_credential_then_returns_credential(
            self, credential_service, mock_repository, sample_drivers_license):
        mock_repository.get_credential.return_value = sample_drivers_license

        credential = credential_service.get_credential(
            "test-id",
            CredentialType.DRIVERS_LICENSE,
            "ca"
        )

        mock_repository.get_credential.assert_called_once_with(
            "test-id",
            CredentialType.DRIVERS_LICENSE,
            "ca"
        )
        assert credential == sample_drivers_license

    def test_given_valid_credential_id_when_validating_credential_then_returns_status(
            self, credential_service, mock_repository, sample_drivers_license):
        mock_repository.get_credential.return_value = sample_drivers_license

        status = credential_service.validate_credential(
            "test-id",
            CredentialType.DRIVERS_LICENSE,
            "CA"
        )

        mock_repository.get_credential.assert_called_once_with(
            "test-id",
            CredentialType.DRIVERS_LICENSE,
            "CA"
        )
        assert status == CredentialStatus.ACTIVE

    def test_given_valid_credential_when_creating_credential_then_returns_created_credential(
            self, credential_service, mock_repository, sample_drivers_license):
        mock_repository.create_credential.return_value = sample_drivers_license

        created = credential_service.create_credential(sample_drivers_license)

        mock_repository.create_credential.assert_called_once_with(sample_drivers_license)
        assert created == sample_drivers_license

    def test_given_active_credential_when_suspending_then_updates_status_to_suspended(
            self, credential_service, mock_repository, sample_drivers_license):
        mock_repository.get_credential.return_value = sample_drivers_license

        credential_service.update_credential(
            "test-id",
            "CA",
            CredentialType.DRIVERS_LICENSE,
            CredentialStatus.SUSPENDED,
            "Test suspension"
        )

        assert sample_drivers_license.status == CredentialStatus.SUSPENDED
        assert sample_drivers_license.suspension_reason == "Test suspension"
        mock_repository.update_credential_status.assert_called_once_with(sample_drivers_license)

    def test_given_active_credential_when_revoking_then_updates_status_to_revoked(
            self, credential_service, mock_repository, sample_drivers_license):
        mock_repository.get_credential.return_value = sample_drivers_license

        credential_service.update_credential(
            "test-id",
            "CA",
            CredentialType.DRIVERS_LICENSE,
            CredentialStatus.REVOKED,
            "Test revocation"
        )

        assert sample_drivers_license.status == CredentialStatus.REVOKED
        assert sample_drivers_license.revocation_reason == "Test revocation"
        mock_repository.update_credential_status.assert_called_once_with(sample_drivers_license)

    def test_given_suspended_credential_when_reinstating_then_updates_status_to_active(
            self, credential_service, mock_repository, sample_drivers_license):
        mock_repository.get_credential.return_value = sample_drivers_license
        sample_drivers_license.suspend("Initial suspension")

        credential_service.update_credential(
            "test-id",
            "CA",
            CredentialType.DRIVERS_LICENSE,
            CredentialStatus.ACTIVE,
            None
        )

        assert sample_drivers_license.status == CredentialStatus.ACTIVE