from datetime import datetime, UTC

from botocore.exceptions import ClientError
from botocore.config import Config

from app.application.credential_mapper import AbstractCredentialMapper
import boto3

from app.domain.credential import Credential
from app.domain.credential_repository import AbstractCredentialRepository
from app.domain.credential_type import CredentialType
from app.infrastructure.database.dynamodb_manager import DynamoDBManager
from app.infrastructure.mapper_factory import MapperFactory


class DynamoDBCredentialRepository(AbstractCredentialRepository):
    def __init__(self, db_manager: DynamoDBManager):
        self.dynamodb = db_manager.client
        self._table = self.create_credentials_table()
        self._mapperFactory = MapperFactory()

    def get_credential(self, credential_id: str, credential_type: CredentialType) -> Credential | None:
        try:
            response = self._table.get_item(
                Key={
                    'PK': f'CRED#{credential_id}',
                    'SK': f'METADATA#{credential_type.value}'
                })
            print(response)
            item = response.get('Item')

            if not item:
                return None

            mapper = self._mapperFactory.get_mapper(CredentialType(item.get('credential_type')))
            credential = mapper.to_domain(item)
            return credential
        except ClientError as e:
            print(f"Error getting item from DynamoDB: {e.response['Error']['Message']}")
            return None

        except Exception as e:
            print(f"Unexpected error: {str(e)}")

    def create_credentials_table(self):
        """
        Creates the Credentials table if it doesn't exist
        """
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
            else:
                raise
    def create_credential(self, credential: Credential):
        try:
            credential_mapper: AbstractCredentialMapper = self._mapperFactory.get_mapper(credential.get_credential_type())
            credential_item = credential_mapper.to_dynamo(credential)
            response = self._table.put_item(Item=credential_item)
            print("Sample credential inserted successfully!")
            return response
        except ClientError as e:
            print(f"Error putting item: {e}")
            raise

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
                    'PK': f'CRED#{str(credential.issuer_id)}',
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
            print(response)
            return response
        except ClientError as e:
            print(f"Error updating item in DynamoDB: {e.response['Error']['Message']}")
            raise