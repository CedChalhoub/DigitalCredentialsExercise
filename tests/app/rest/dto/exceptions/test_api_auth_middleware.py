import pytest
from fastapi import HTTPException
from unittest.mock import Mock

from app.infrastructure.exceptions.database_exception import DatabaseException
from app.rest.exceptions.api_auth_middleware import verify_api_key
from app.application.services.api_auth_service import ApiAuthService


@pytest.fixture
def mock_auth_service():
    return Mock(spec=ApiAuthService)


class TestApiAuthMiddleware:
    @pytest.mark.asyncio
    async def test_given_valid_api_key_when_verifying_then_returns_key(
            self, mock_auth_service):
        mock_auth_service.validate_api_key.return_value = True
        verify_key = verify_api_key(mock_auth_service)

        result = await verify_key("valid-api-key")

        assert result == "valid-api-key"
        mock_auth_service.validate_api_key.assert_called_once_with("valid-api-key")

    @pytest.mark.asyncio
    async def test_given_invalid_api_key_when_verifying_then_raises_unauthorized_exception(
            self, mock_auth_service):
        mock_auth_service.validate_api_key.return_value = False
        verify_key = verify_api_key(mock_auth_service)

        with pytest.raises(HTTPException) as exc_info:
            await verify_key("invalid-api-key")

        assert exc_info.value.status_code == 401
        assert "Invalid API key" in exc_info.value.detail
        mock_auth_service.validate_api_key.assert_called_once_with("invalid-api-key")

    @pytest.mark.asyncio
    async def test_given_database_error_when_verifying_api_key_then_raises_database_exception(
            self, mock_auth_service):
        mock_auth_service.validate_api_key.side_effect = DatabaseException("Database error")
        verify_key = verify_api_key(mock_auth_service)

        with pytest.raises(DatabaseException):
            await verify_key("test-api-key")