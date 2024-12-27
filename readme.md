# Digital Credentials API

REST API for managing digital credentials (passports, driver's licenses, etc.) with support for issuing, validating, and updating credential status.

## Features

- Issue digital credentials (passports, driver's licenses)
- Validate credential status
- Update credential status (suspend/revoke)
- DDD architecture with AWS deployment support

## Prerequisites

- Python 3.9+
- Docker
- AWS CLI configured
- DynamoDB Local (for development)

## Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Local Development

1. Start DynamoDB Local:
```bash
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
```
Note: Requires Java Runtime Environment (JRE) version 8.x or newer

2. Run the FastAPI application:
```bash
sam local start-api
```

The API will be available at `http://localhost:3000`

## API Endpoints

### GET /heartbeat
Health check endpoint.

### GET /credentials/{credential_id}
Retrieve a credential by ID.

**Parameters:**
- `credential_id`: Credential identifier
- `credential_type`: Query parameter specifying the type (`drivers_license` or `passport`)

### GET /credentials/validate/{credential_id}
Validate a credential's status.

**Parameters:**
- `credential_id`: Credential identifier
- `credential_type`: Query parameter specifying the type (`drivers_license` and `passport` currently supported, more to come)

### POST /credentials
Create a new credential.

**Parameters:**
- `credential_type`: Query parameter specifying the type (`drivers_license` or `passport`)

**Body (Driver's License):**
```json
{
  "issuer_id": "string",
  "holder_id": "string",
  "valid_from": "2024-01-01T00:00:00Z",
  "valid_until": "2029-01-01T00:00:00Z",
  "vehicle_classes": ["A", "B"],
  "issuing_province": "string"
}
```

**Body (Passport):**
```json
{
  "issuer_id": "string",
  "holder_id": "string",
  "valid_from": "2024-01-01T00:00:00Z",
  "valid_until": "2034-01-01T00:00:00Z",
  "nationality": "string",
  "issuing_country": "string"
}
```

### PATCH /credentials/{credential_id}
Update a credential's status.

**Parameters:**
- `credential_id`: Credential identifier
- `credential_type`: Query parameter specifying the type

**Body:**
```json
{
  "status": "active|suspended|revoked",
  "reason": "string"
}
```

## Testing

Run unit tests:
```bash
pytest
```

Run integration tests:
```bash
pytest tests/integration
```

## AWS Deployment

1. Package the application:
```bash
sam build
```

2. Deploy to AWS:
```bash
sam deploy --guided
```

This will deploy:
- API Gateway
- Lambda function
- DynamoDB table
- Required IAM roles

## Architecture

The application follows Domain-Driven Design principles:

- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and service orchestration
- **Infrastructure Layer**: External services integration (DynamoDB)
- **API Layer**: REST endpoints and DTOs
