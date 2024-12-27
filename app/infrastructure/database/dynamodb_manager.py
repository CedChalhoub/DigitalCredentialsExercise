import boto3
from botocore.config import Config

from app.infrastructure.database.database_config import DatabaseConfig


class DynamoDBManager:
    def __init__(self, config: DatabaseConfig):
        print("\nDynamoDB Manager Configuration:")
        print(f"Endpoint URL: {config.endpoint_url}")
        print(f"Region: {config.region}")
        print(f"Access Key ID: {config.access_key_id}")
        print(f"Secret Access Key: {config.secret_access_key}")

        self._dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=config.endpoint_url,
            region_name=config.region,
            aws_access_key_id=config.access_key_id,
            aws_secret_access_key=config.secret_access_key,
            config=Config(retries={'max_attempts': config.max_retries})
        )
        print("DynamoDB resource created")

    @property
    def client(self):
        return self._dynamodb