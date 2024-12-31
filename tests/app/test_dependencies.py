import pytest
from unittest.mock import patch, Mock

from app.application.services.credential_service import CredentialService
from app.dependencies import get_credential_service
from app.infrastructure.persistence.dynamodb.database_config import DatabaseConfig
from app.infrastructure.persistence.dynamodb.dynamodb_manager import DynamoDBManager
from app.infrastructure.persistence.repositories.dynamodb_credential_repository import DynamoDBCredentialRepository


@pytest.fixture
def mock_db_manager():
    with patch('boto3.resource') as mock_resource:
        mock_table = Mock()
        mock_resource.return_value.Table.return_value = mock_table
        mock_resource.return_value.create_table.return_value = mock_table

        config = DatabaseConfig(
            endpoint_url='http://localhost:8000',
            region='local',
            access_key_id='dummy',
            secret_access_key='dummy'
        )
        db_manager = DynamoDBManager(config)
        db_manager._dynamodb = mock_resource.return_value
        return db_manager


@pytest.fixture
def mock_repository(mock_db_manager):
    return DynamoDBCredentialRepository(mock_db_manager)


def test_get_credential_service(mock_repository):
    service = get_credential_service(mock_repository)
    assert isinstance(service, CredentialService)
    assert isinstance(service._repository, DynamoDBCredentialRepository)