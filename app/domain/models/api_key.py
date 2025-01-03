import secrets
import string
from dataclasses import dataclass
from datetime import datetime, UTC


@dataclass
class ApiKey:
    key: str
    created_at: datetime
    last_used: datetime | None = None
    description: str | None = None

    @staticmethod
    def generate(description: str | None = None) -> 'ApiKey':
        alphabet = string.ascii_letters + string.digits
        key = ''.join(secrets.choice(alphabet) for i in range(32))

        return ApiKey(
            key=key,
            created_at=datetime.now(tz=UTC),
            description=description
        )