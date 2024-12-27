from unittest.mock import patch, Mock
from app.dependencies import get_repository, get_assembler_registry, get_credential_service
from app.infrastructure.dynamodb_credential_repository import DynamoDBCredentialRepository
from app.api.dto.assembler_registry import AssemblerRegistry
from app.application.credential_service import CredentialService


@patch('boto3.resource')
def test_get_repository_default(mock_boto):
    mock_table = Mock()
    mock_boto.return_value.Table.return_value = mock_table
    mock_boto.return_value.create_table.return_value = mock_table

    repo = get_repository()
    assert isinstance(repo, DynamoDBCredentialRepository)


@patch('boto3.resource')
@patch.dict('os.environ', {'REPOSITORY_TYPE': 'dynamodb'})
def test_get_repository_dynamodb(mock_boto):
    mock_table = Mock()
    mock_boto.return_value.Table.return_value = mock_table
    mock_boto.return_value.create_table.return_value = mock_table

    repo = get_repository()
    assert isinstance(repo, DynamoDBCredentialRepository)


@patch('boto3.resource')
@patch.dict('os.environ', {'REPOSITORY_TYPE': 'unknown'})
def test_get_repository_fallback(mock_boto):
    mock_table = Mock()
    mock_boto.return_value.Table.return_value = mock_table
    mock_boto.return_value.create_table.return_value = mock_table

    repo = get_repository()
    assert isinstance(repo, DynamoDBCredentialRepository)


def test_get_assembler_registry():
    registry = get_assembler_registry()
    assert isinstance(registry, AssemblerRegistry)


@patch('boto3.resource')
def test_get_credential_service(mock_boto):
    mock_table = Mock()
    mock_boto.return_value.Table.return_value = mock_table
    mock_boto.return_value.create_table.return_value = mock_table

    service = get_credential_service(get_repository())
    assert isinstance(service, CredentialService)