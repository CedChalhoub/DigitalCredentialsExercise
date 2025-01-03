from datetime import datetime, UTC

from botocore.exceptions import ClientError

from app.infrastructure.persistence.mappers.credential_mapper import CredentialMapper

from app.domain.models.credential import Credential
from app.domain.repositories.credential_repository import AbstractCredentialRepository
from app.domain.enums.credential_type import CredentialType
from app.domain.exceptions.credential.credential_not_found_exception import CredentialNotFoundException
from app.infrastructure.persistence.dynamodb.dynamodb_manager import DynamoDBManager
from app.infrastructure.exceptions.database_exception import DatabaseException
from app.infrastructure.persistence.mappers.credential_mapper_provider import CredentialMapperProvider


class DynamoDBCredentialRepository(AbstractCredentialRepository):
    def __init__(self, db_manager: DynamoDBManager):
        self.dynamodb = db_manager.client
        self._table = self._create_credentials_table()
        self._mapperFactory = CredentialMapperProvider()

    def get_credential(self, credential_id: str, credential_type: CredentialType, issuing_country: str) -> Credential | None:
        try:
            response = self._table.get_item(
                Key={
                    'PK': f'CRED#{issuing_country}#{str(credential_id)}',
                    'SK': f'METADATA#{credential_type.value}'
                })

            item = response.get('Item')

            if not item:
                raise CredentialNotFoundException(credential_id, credential_type.value)

            mapper = self._mapperFactory.get_mapper(CredentialType(item.get('credential_type')))
            credential = mapper.to_domain(item)
            return credential
        except CredentialNotFoundException:
            # Let CredentialNotFoundException bubble up
            raise
        except (ClientError, Exception) as e:
            raise DatabaseException(
                f"Error getting credential: {str(e)}")

    def _create_credentials_table(self):
        try:
            # Create the table
            table = self.dynamodb.create_table(
                TableName="Credentials",
                KeySchema=[
                    {
                        'AttributeName': 'PK',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'SK',
                        'KeyType': 'RANGE'  # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'PK',
                        'AttributeType': 'S'  # String
                    },
                    {
                        'AttributeName': 'SK',
                        'AttributeType': 'S'  # String
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

            # Wait for the table to be created
            table.meta.client.get_waiter('table_exists').wait(TableName='Credentials')
            return table
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                return self.dynamodb.Table('Credentials')
            raise DatabaseException(f"Error creating table: {str(e)}")
        except Exception as e:
            raise DatabaseException(f"Error creating table: {str(e)}")
    def create_credential(self, credential: Credential):
        try:
            credential_mapper: CredentialMapper = self._mapperFactory.get_mapper(credential.get_credential_type())
            credential_item = credential_mapper.to_dynamo(credential)
            response = self._table.put_item(Item=credential_item)
            return response
        except (ClientError, Exception) as e:
            raise DatabaseException(f"Error creating credential: {str(e)}")

    def update_credential_status(self, credential: Credential) -> None:
        update_expression = """
            SET #status = :status,
                suspension_reason = :suspension_reason,
                revocation_reason = :revocation_reason,
                updated_at = :updated_at
        """

        try:
            response = self._table.update_item(
                Key={
                    'PK': f'CRED#{credential.issuing_country}#{str(credential.credential_id)}',
                    'SK': f'METADATA#{credential.get_credential_type().value}'
                },
                UpdateExpression=update_expression,
                ExpressionAttributeNames={
                    '#status': 'status'
                },
                ExpressionAttributeValues={
                    ':status': credential.status.value,
                    ':suspension_reason': credential.suspension_reason,
                    ':revocation_reason': credential.revocation_reason,
                    ':updated_at': datetime.now(UTC).isoformat()
                },
                ReturnValues="UPDATED_NEW"
            )
            return response
        except (ClientError, Exception) as e:
            raise DatabaseException(f"Error updating item in DynamoDB: {e.response['Error']['Message']}")
