import pytest
from datetime import datetime, UTC
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
from app.domain.enums.credential_type import CredentialType
from app.domain.exceptions.credential.credential_not_found_exception import CredentialNotFoundException
from app.domain.models.drivers_license import DriversLicense
from app.infrastructure.exceptions.database_exception import DatabaseException
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
def sample_drivers_license():
    return DriversLicense(
        issuer_id="test-issuer-123",
        holder_id="test-holder-456",
        valid_from=datetime(2024, 1, 1, tzinfo=UTC),
        valid_until=datetime(2029, 12, 31, tzinfo=UTC),
        vehicle_classes=["A", "B"],
        issuing_country="CA",
        issuing_region="ON"
    )


@pytest.fixture
def dynamo_item():
    return {
        'PK': 'CRED#CA#test-issuer-123',
        'SK': 'METADATA#drivers_license',
        'credential_type': 'drivers_license',
        'issuer_id': 'test-issuer-123',
        'holder_id': 'test-holder-456',
        'valid_from': '2024-01-01T00:00:00+00:00',
        'valid_until': '2029-12-31T00:00:00+00:00',
        'status': 'active',
        'vehicle_classes': ['A', 'B'],
        'issuing_country': 'CA',
        'issuing_region': 'ON',
        'suspension_reason': None,
        'revocation_reason': None,
        'version': 1
    }


class TestDynamoDBCredentialRepository:
    def test_given_existing_credential_when_retrieving_then_returns_credential(
            self, mock_db_manager, dynamo_item):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().get_item.return_value = {'Item': dynamo_item}

        credential = repo.get_credential("test-issuer-123", CredentialType.DRIVERS_LICENSE, "ca")

        assert credential.issuer_id == "test-issuer-123"
        assert credential.holder_id == "test-holder-456"
        assert credential.issuing_country == "ca"
        mock_db_manager._dynamodb.Table().get_item.assert_called_once_with(
            Key={
                'PK': 'CRED#ca#test-issuer-123',
                'SK': 'METADATA#drivers_license'
            }
        )

    def test_given_nonexistent_credential_when_retrieving_then_raises_not_found_exception(
            self, mock_db_manager):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().get_item.return_value = {}

        with pytest.raises(CredentialNotFoundException) as exc_info:
            repo.get_credential("nonexistent", CredentialType.DRIVERS_LICENSE, "ca")

        assert "not found" in str(exc_info.value)

    def test_given_database_error_when_retrieving_credential_then_raises_database_exception(
            self, mock_db_manager):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().get_item.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='GetItem'
        )

        with pytest.raises(DatabaseException) as exc_info:
            repo.get_credential("test-id", CredentialType.DRIVERS_LICENSE, "ca")

        assert "Error getting credential" in str(exc_info.value)

    def test_given_valid_credential_when_creating_then_stores_in_dynamodb(
            self, mock_db_manager, sample_drivers_license):
        repo = DynamoDBCredentialRepository(mock_db_manager)

        repo.create_credential(sample_drivers_license)

        mock_db_manager._dynamodb.Table().put_item.assert_called_once()
        put_item_args = mock_db_manager._dynamodb.Table().put_item.call_args[1]['Item']
        assert put_item_args['PK'] == f'CRED#ca#{sample_drivers_license.issuer_id}'
        assert put_item_args['SK'] == 'METADATA#drivers_license'

    def test_given_database_error_when_creating_credential_then_raises_database_exception(
            self, mock_db_manager, sample_drivers_license):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().put_item.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='PutItem'
        )

        with pytest.raises(DatabaseException) as exc_info:
            repo.create_credential(sample_drivers_license)

        assert "Error creating credential" in str(exc_info.value)

    def test_given_valid_credential_when_updating_status_then_updates_in_dynamodb(
            self, mock_db_manager, sample_drivers_license):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        sample_drivers_license.suspend("Test suspension")

        repo.update_credential_status(sample_drivers_license)

        mock_db_manager._dynamodb.Table().update_item.assert_called_once()
        update_args = mock_db_manager._dynamodb.Table().update_item.call_args[1]
        assert update_args['Key']['PK'] == f'CRED#ca#{sample_drivers_license.issuer_id}'
        assert update_args['Key']['SK'] == 'METADATA#drivers_license'

    def test_given_database_error_when_updating_status_then_raises_database_exception(
            self, mock_db_manager, sample_drivers_license):
        repo = DynamoDBCredentialRepository(mock_db_manager)
        mock_db_manager._dynamodb.Table().update_item.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='UpdateItem'
        )

        with pytest.raises(DatabaseException) as exc_info:
            repo.update_credential_status(sample_drivers_license)

        assert "Error updating item in DynamoDB" in str(exc_info.value)