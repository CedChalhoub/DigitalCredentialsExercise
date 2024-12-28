import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    endpoint_url: str | None
    region: str
    access_key_id: str | None
    secret_access_key: str | None
    max_retries: int = 1

    @classmethod
    def from_environment(cls) -> 'DatabaseConfig':
        is_local = os.getenv('AWS_SAM_LOCAL') == 'true'
        region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1').lower()

        if is_local:
            config = cls(
                endpoint_url="http://host.docker.internal:8000",
                region=region,
                access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            return config

        return cls(
            endpoint_url=None,
            region=region,
            access_key_id=None,
            secret_access_key=None
        )