import pytest
from datetime import datetime, UTC
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
from app.domain.models.api_key import ApiKey
from app.infrastructure.exceptions.database_exception import DatabaseException
from app.infrastructure.persistence.dynamodb.database_config import DatabaseConfig
from app.infrastructure.persistence.dynamodb.dynamodb_manager import DynamoDBManager
from app.infrastructure.persistence.repositories.dynamodb_api_key_repository import DynamoDBApiKeyRepository


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
def sample_api_key():
    return ApiKey(
        key="test-key-123",
        created_at=datetime.now(UTC),
        description="Test key"
    )


class TestDynamoDBApiKeyRepository:
    def test_given_valid_api_key_when_storing_then_stores_successfully(
            self, mock_db_manager, sample_api_key):
        repo = DynamoDBApiKeyRepository(mock_db_manager)

        repo.store_api_key(sample_api_key)

        mock_db_manager._dynamodb.Table().put_item.assert_called_once()
        put_item_args = mock_db_manager._dynamodb.Table().put_item.call_args[1]['Item']
        assert put_item_args['PK'] == f'APIKEY#{sample_api_key.key}'
        assert put_item_args['SK'] == 'METADATA'

    def test_given_database_error_when_storing_api_key_then_raises_exception(
            self, mock_db_manager, sample_api_key):
        repo = DynamoDBApiKeyRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().put_item.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='PutItem'
        )

        with pytest.raises(DatabaseException) as exc_info:
            repo.store_api_key(sample_api_key)

        assert "Error storing API key" in str(exc_info.value)

    def test_given_existing_api_key_when_retrieving_then_returns_api_key(
            self, mock_db_manager, sample_api_key):
        repo = DynamoDBApiKeyRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().get_item.return_value = {
            'Item': {
                'key': sample_api_key.key,
                'created_at': sample_api_key.created_at.isoformat(),
                'description': sample_api_key.description
            }
        }

        result = repo.get_api_key(sample_api_key.key)

        assert result.key == sample_api_key.key
        assert result.description == sample_api_key.description
        mock_db_manager._dynamodb.Table().get_item.assert_called_once_with(
            Key={'PK': f'APIKEY#{sample_api_key.key}', 'SK': 'METADATA'}
        )

    def test_given_nonexistent_api_key_when_retrieving_then_returns_none(
            self, mock_db_manager):
        repo = DynamoDBApiKeyRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().get_item.return_value = {}

        result = repo.get_api_key("nonexistent-key")

        assert result is None

    def test_given_valid_api_key_when_updating_then_updates_last_used_timestamp(
            self, mock_db_manager):
        repo = DynamoDBApiKeyRepository(mock_db_manager)
        timestamp = datetime.now(UTC)

        repo.update_api_key("test-key", timestamp)

        mock_db_manager._dynamodb.Table().update_item.assert_called_once()
        update_args = mock_db_manager._dynamodb.Table().update_item.call_args[1]
        assert update_args['Key']['PK'] == 'APIKEY#test-key'
        assert update_args['ExpressionAttributeValues'][':timestamp'] == timestamp.isoformat()

    def test_given_database_error_when_updating_api_key_then_raises_exception(
            self, mock_db_manager):
        repo = DynamoDBApiKeyRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().update_item.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='UpdateItem'
        )

        with pytest.raises(DatabaseException) as exc_info:
            repo.update_api_key("test-key", datetime.now(UTC))

        assert "Error updating API key" in str(exc_info.value)