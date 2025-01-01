import pytest
from datetime import datetime, UTC
from unittest.mock import Mock
from app.domain.models.api_key import ApiKey
from app.application.services.api_auth_service import ApiAuthService
from app.infrastructure.exceptions.database_exception import DatabaseException


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def auth_service(mock_repository):
    return ApiAuthService(mock_repository)


@pytest.fixture
def sample_api_key():
    return ApiKey(
        key="test-key-123",
        created_at=datetime.now(UTC),
        description="Test key"
    )


class TestApiAuthService:
    def test_generate_api_key_success(self, auth_service, mock_repository):
        # Test successful API key generation
        result = auth_service.generate_api_key("Test description")

        assert result.key is not None
        assert len(result.key) == 32
        assert result.description == "Test description"
        assert isinstance(result.created_at, datetime)
        mock_repository.store_api_key.assert_called_once()

    def test_generate_api_key_no_description(self, auth_service, mock_repository):
        # Test API key generation without description
        result = auth_service.generate_api_key()

        assert result.key is not None
        assert result.description is None
        mock_repository.store_api_key.assert_called_once()

    def test_generate_api_key_database_error(self, auth_service, mock_repository):
        # Test handling of database errors during key generation
        mock_repository.store_api_key.side_effect = DatabaseException("Test error")

        with pytest.raises(DatabaseException):
            auth_service.generate_api_key()

    def test_validate_api_key_success(self, auth_service, mock_repository, sample_api_key):
        # Test successful API key validation
        mock_repository.get_api_key.return_value = sample_api_key

        result = auth_service.validate_api_key("test-key-123")

        assert result is True
        mock_repository.get_api_key.assert_called_once_with("test-key-123")
        mock_repository.update_api_key.assert_called_once()

    def test_validate_api_key_not_found(self, auth_service, mock_repository):
        # Test validation of non-existent API key
        mock_repository.get_api_key.return_value = None

        result = auth_service.validate_api_key("invalid-key")

        assert result is False
        mock_repository.get_api_key.assert_called_once_with("invalid-key")
        mock_repository.update_api_key.assert_not_called()

    def test_validate_api_key_database_error(self, auth_service, mock_repository):
        # Test handling of database errors during validation
        mock_repository.get_api_key.side_effect = DatabaseException("Test error")

        with pytest.raises(DatabaseException):
            auth_service.validate_api_key("test-key-123")
