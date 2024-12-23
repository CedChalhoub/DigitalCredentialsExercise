from botocore.exceptions import ClientError

from app.domain import Credential
import boto3

class DynamoDBCredentialRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def get_credential(self, credential_id: str) -> Credential:
        table = self.dynamodb.Table('Credentials')
        try:
            response = table.get_item(Key={'credential_id': credential_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting item from DynamoDB: {e.response['Error']['Message']}")
            return None

    def new_credential(self, credential: Credential):
        pass
