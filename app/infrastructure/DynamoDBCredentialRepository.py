import logging
from datetime import datetime, UTC
from uuid import UUID

from botocore.exceptions import ClientError
from botocore.config import Config

from app.application.AbstractCredentialMapper import AbstractCredentialMapper
from app.domain import Credential
import boto3

from app.domain.AbstractCredentialRepository import AbstractCredentialRepository
from app.domain.CredentialType import CredentialType
from app.infrastructure.MapperFactory import MapperFactory


class DynamoDBCredentialRepository(AbstractCredentialRepository):
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url='http://host.docker.internal:8000',  # Using 127.0.0.1 instead of localhost
            region_name='local',
            aws_access_key_id='dummy',
            aws_secret_access_key='dummy',
            config=Config(
                retries=dict(
                    max_attempts=1  # Fail fast in local development
                )
            ) )
        self._table = self.create_credentials_table()
        self._mapperFactory = MapperFactory()

    def get_credential(self, credential_id: str, credential_type: CredentialType) -> Credential:
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