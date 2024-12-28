import pytest
from datetime import datetime, UTC
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
from app.domain.credential_type import CredentialType
from app.domain.drivers_license import DriversLicense
from app.domain.exceptions.credential.credential_not_found_exception import CredentialNotFoundException
from app.infrastructure.exceptions.database_exception import DatabaseException
from app.infrastructure.dynamodb_credential_repository import DynamoDBCredentialRepository
from app.infrastructure.database.database_config import DatabaseConfig
from app.infrastructure.database.dynamodb_manager import DynamoDBManager


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
        # Set the private attribute instead of the property
        db_manager._dynamodb = mock_resource.return_value
        return db_manager


@pytest.fixture
def sample_drivers_license():
    return DriversLicense(
        issuer_id="test-issuer-123",
        holder_id="test-holder-456",
        valid_from=datetime(2024, 1, 1, tzinfo=UTC),
        valid_until=datetime(2029, 12, 31, tzinfo=UTC),
        vehicle_classes=["A", "B"],
        issuing_province="ON"
    )


@pytest.fixture
def dynamo_item():
    return {
        'PK': 'CRED#test-issuer-123',
        'SK': 'METADATA#drivers_license',
        'credential_type': 'drivers_license',
        'issuer_id': 'test-issuer-123',
        'holder_id': 'test-holder-456',
        'valid_from': '2024-01-01T00:00:00+00:00',
        'valid_until': '2029-12-31T00:00:00+00:00',
        'status': 'active',
        'vehicle_classes': ['A', 'B'],
        'issuing_province': 'ON',
        'suspension_reason': None,
        'revocation_reason': None,
        'version': 1
    }


class TestDynamoDBCredentialRepository:
    def test_get_credential_success(self, mock_db_manager, dynamo_item):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().get_item.return_value = {'Item': dynamo_item}

        credential = repo.get_credential("test-issuer-123", CredentialType.DRIVERS_LICENSE)

        assert credential.issuer_id == "test-issuer-123"
        assert credential.holder_id == "test-holder-456"
        mock_db_manager._dynamodb.Table().get_item.assert_called_once_with(
            Key={
                'PK': 'CRED#test-issuer-123',
                'SK': 'METADATA#drivers_license'
            }
        )

    def test_get_credential_not_found(self, mock_db_manager):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().get_item.return_value = {}

        with pytest.raises(CredentialNotFoundException):
            repo.get_credential("nonexistent", CredentialType.DRIVERS_LICENSE)

    def test_get_credential_client_error(self, mock_db_manager):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().get_item.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='GetItem'
        )

        with pytest.raises(DatabaseException):
            repo.get_credential("test-id", CredentialType.DRIVERS_LICENSE)

    def test_create_credential(self, mock_db_manager, sample_drivers_license):
        repo = DynamoDBCredentialRepository(mock_db_manager)

        repo.create_credential(sample_drivers_license)

        mock_db_manager._dynamodb.Table().put_item.assert_called_once()
        put_item_args = mock_db_manager._dynamodb.Table().put_item.call_args[1]['Item']
        assert put_item_args['PK'] == f'CRED#{sample_drivers_license.issuer_id}'
        assert put_item_args['SK'] == 'METADATA#drivers_license'

    def test_create_credential_error(self, mock_db_manager, sample_drivers_license):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().put_item.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='PutItem'
        )

        with pytest.raises(DatabaseException):
            repo.create_credential(sample_drivers_license)

    def test_update_credential_status(self, mock_db_manager, sample_drivers_license):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        sample_drivers_license.suspend("Test suspension")

        repo.update_credential_status(sample_drivers_license)

        mock_db_manager._dynamodb.Table().update_item.assert_called_once()
        update_args = mock_db_manager._dynamodb.Table().update_item.call_args[1]
        assert update_args['Key']['PK'] == f'CRED#{sample_drivers_license.issuer_id}'
        assert update_args['Key']['SK'] == 'METADATA#drivers_license'
        assert update_args['ExpressionAttributeValues'][':status'] == 'suspended'
        assert update_args['ExpressionAttributeValues'][':suspension_reason'] == 'Test suspension'

    def test_update_credential_status_error(self, mock_db_manager, sample_drivers_license):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().update_item.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='UpdateItem'
        )

        with pytest.raises(DatabaseException):
            repo.update_credential_status(sample_drivers_license)