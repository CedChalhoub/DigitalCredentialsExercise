# app/infrastructure/persistence/repositories/dynamodb_api_key_repository.py
from datetime import datetime
from botocore.exceptions import ClientError
from app.domain.models.api_key import ApiKey
from app.domain.repositories.api_key_repository import AbstractApiKeyRepository
from app.infrastructure.persistence.dynamodb.dynamodb_manager import DynamoDBManager
from app.infrastructure.exceptions.database_exception import DatabaseException


class DynamoDBApiKeyRepository(AbstractApiKeyRepository):
    def __init__(self, db_manager: DynamoDBManager):
        self.dynamodb = db_manager.client
        self._table = self._create_api_keys_table()

    def _create_api_keys_table(self):
        try:
            # Create the table
            table = self.dynamodb.create_table(
                TableName="ApiKeys",
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
            table.meta.client.get_waiter('table_exists').wait(TableName='ApiKeys')
            return table
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                # Table already exists
                return self.dynamodb.Table('ApiKeys')
            raise DatabaseException(f"Error creating table: {str(e)}")
        except Exception as e:
            raise DatabaseException(f"Error creating table: {str(e)}")

    def store_api_key(self, api_key: ApiKey) -> None:
        try:
            item = {
                'PK': f'APIKEY#{api_key.key}',
                'SK': 'METADATA',
                'key': api_key.key,
                'created_at': api_key.created_at.isoformat(),
                'description': api_key.description
            }
            if api_key.last_used:
                item['last_used'] = api_key.last_used.isoformat()

            self._table.put_item(Item=item)
        except Exception as e:
            raise DatabaseException(f"Error storing API key: {str(e)}")

    def get_api_key(self, key: str) -> ApiKey | None:
        try:
            response = self._table.get_item(
                Key={
                    'PK': f'APIKEY#{key}',
                    'SK': 'METADATA'
                }
            )

            if 'Item' not in response:
                return None

            item = response['Item']

            # Safely parse the datetime fields
            created_at = datetime.fromisoformat(item['created_at'])
            last_used = (datetime.fromisoformat(item['last_used'])
                         if item.get('last_used') else None)

            return ApiKey(
                key=item['key'],
                created_at=created_at,
                last_used=last_used,
                description=item.get('description')
            )
        except Exception as e:
            raise DatabaseException(f"Error getting API key: {str(e)}")

    def update_api_key(self, key: str, timestamp: datetime) -> None:
        try:
            self._table.update_item(
                Key={
                    'PK': f'APIKEY#{key}',
                    'SK': 'METADATA'
                },
                UpdateExpression='SET last_used = :timestamp',
                ExpressionAttributeValues={
                    ':timestamp': timestamp.isoformat()
                }
            )
        except Exception as e:
            raise DatabaseException(f"Error updating API key last used: {str(e)}")