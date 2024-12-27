import pytest
from datetime import datetime, UTC
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
from app.domain.credential_type import CredentialType
from app.domain.drivers_license import DriversLicense
from app.infrastructure.dynamodb_credential_repository import DynamoDBCredentialRepository


@pytest.fixture
def mock_table():
    return Mock()


@pytest.fixture
def mock_dynamodb():
    with patch('boto3.resource') as mock_resource:
        mock_table = Mock()
        mock_resource.return_value.Table.return_value = mock_table
        mock_resource.return_value.create_table.return_value = mock_table
        yield mock_resource


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
        'revocation_reason': None
    }


class TestDynamoDBCredentialRepository:
    def test_get_credential_success(self, mock_dynamodb, dynamo_item):
        repo = DynamoDBCredentialRepository()
        repo._table.get_item.return_value = {'Item': dynamo_item}

        credential = repo.get_credential("test-issuer-123", CredentialType.DRIVERS_LICENSE)

        assert credential.issuer_id == "test-issuer-123"
        assert credential.holder_id == "test-holder-456"
        repo._table.get_item.assert_called_once_with(
            Key={
                'PK': 'CRED#test-issuer-123',
                'SK': 'METADATA#drivers_license'
            }
        )

    def test_get_credential_not_found(self, mock_dynamodb):
        repo = DynamoDBCredentialRepository()
        repo._table.get_item.return_value = {'Item': None}

        result = repo.get_credential("nonexistent", CredentialType.DRIVERS_LICENSE)
        assert result is None

    def test_get_credential_client_error(self, mock_dynamodb):
        repo = DynamoDBCredentialRepository()
        repo._table.get_item.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='GetItem'
        )

        result = repo.get_credential("test-id", CredentialType.DRIVERS_LICENSE)
        assert result is None

    def test_create_credential(self, mock_dynamodb, sample_drivers_license):
        repo = DynamoDBCredentialRepository()

        repo.create_credential(sample_drivers_license)

        repo._table.put_item.assert_called_once()
        put_item_args = repo._table.put_item.call_args[1]['Item']
        assert put_item_args['PK'] == f'CRED#{sample_drivers_license.issuer_id}'
        assert put_item_args['SK'] == 'METADATA#drivers_license'

    def test_create_credential_error(self, mock_dynamodb, sample_drivers_license):
        repo = DynamoDBCredentialRepository()
        repo._table.put_item.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='PutItem'
        )

        with pytest.raises(ClientError):
            repo.create_credential(sample_drivers_license)

    def test_update_credential_status(self, mock_dynamodb, sample_drivers_license):
        repo = DynamoDBCredentialRepository()
        sample_drivers_license.suspend("Test suspension")

        repo.update_credential_status(sample_drivers_license)

        repo._table.update_item.assert_called_once()
        update_args = repo._table.update_item.call_args[1]
        assert update_args['Key']['PK'] == f'CRED#{sample_drivers_license.issuer_id}'
        assert update_args['Key']['SK'] == 'METADATA#drivers_license'
        assert update_args['ExpressionAttributeValues'][':status'] == 'suspended'
        assert update_args['ExpressionAttributeValues'][':suspension_reason'] == 'Test suspension'

    def test_update_credential_status_error(self, mock_dynamodb, sample_drivers_license):
        repo = DynamoDBCredentialRepository()
        repo._table.update_item.side_effect = ClientError(
            error_response={'Error': {'Message': 'Test error'}},
            operation_name='UpdateItem'
        )

        with pytest.raises(ClientError):
            repo.update_credential_status(sample_drivers_license)