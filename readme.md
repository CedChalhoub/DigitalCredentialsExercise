# Digital Credentials API

REST API for managing digital credentials (passports, driver's licenses, etc.) with support for issuing, validating, and updating credential status.

## Features

- Issue digital credentials (passports, driver's licenses)
- Validate credential status
- Update credential status (suspend/revoke)
- API key authentication
- DDD architecture with AWS deployment support

## Prerequisites

- Python 3.9+
- Docker (installed and running)
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

1. Ensure Docker is running on your machine
2. Start DynamoDB Local:
    ```bash
    java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
    ```
   Note: Requires Java Runtime Environment (JRE) version 8.x or newer

3. Run the FastAPI application:
    ```bash
    sam local start-api
    ```

The API will be available at `http://localhost:3000`

## Authentication

The API uses API key authentication for protected endpoints. To use protected endpoints, you must first generate an API key and include it in your requests.

### Generating an API Key

Send a POST request to `/api-keys` to generate a new API key:

```json
{
  "description": "Optional description for the API key"
}
```

The response will include your API key:

```json
{
  "key": "generated-api-key",
  "description": "Optional description for the API key",
  "created_at": "2024-01-01T00:00:00Z",
  "last_used": null
}
```

### Using API Keys

For protected endpoints, include your API key in the `X-API-Key` header:

```
X-API-Key: your-api-key
```

## API Endpoints

### GET /
Health check endpoint. No authentication required.

### POST /api-keys
Generate a new API key. No authentication required.

**Body (optional):**
```json
{
  "description": "string"
}
```

### GET /credentials/{issuing_country}/{credential_id}
Retrieve a credential by ID. No authentication required.

**Parameters:**
- `credential_id`: Credential identifier
- `issuing_country`: Country where credential was issued
- `credential_type`: Query parameter specifying the type (`drivers_license` or `passport`)

### GET /credentials/validate/{issuing_country}/{credential_id}
Validate a credential's status. No authentication required.

**Parameters:**
- `credential_id`: Credential identifier
- `issuing_country`: Country where credential was issued
- `credential_type`: Query parameter specifying the type (`drivers_license` and `passport` currently supported, more to come)

### POST /credentials
Create a new credential. Requires API key authentication.

**Headers:**
- `X-API-Key`: Your API key

**Parameters:**
- `credential_type`: Query parameter specifying the type (`drivers_license` or `passport`)

**Body (Driver's License):**
```json
{
  "credential_id": "string",
  "valid_from": "2024-01-01T00:00:00Z",
  "valid_until": "2029-01-01T00:00:00Z",
  "vehicle_classes": ["A", "B"],
  "issuing_region": "string",
  "issuing_country": "Canada"
}
```

**Body (Passport):**
```json
{
  "credential_id": "string",
  "valid_from": "2024-01-01T00:00:00Z",
  "valid_until": "2034-01-01T00:00:00Z",
  "nationality": "string",
  "issuing_country": "string"
}
```

### PATCH /credentials/{issuing_country}/{credential_id}
Update a credential's status. Requires API key authentication.

**Headers:**
- `X-API-Key`: Your API key

**Parameters:**
- `credential_id`: Credential identifier
- `issuing_country`: Country where credential was issued
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
python -m pytest tests/
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
