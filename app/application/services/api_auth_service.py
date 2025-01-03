from datetime import datetime, UTC
from app.domain.models.api_key import ApiKey
from app.domain.repositories.api_key_repository import AbstractApiKeyRepository
from app.infrastructure.exceptions.database_exception import DatabaseException

class ApiAuthService:
    def __init__(self, api_key_repository: AbstractApiKeyRepository):
        self._repository = api_key_repository

    def generate_api_key(self, description: str | None = None) -> ApiKey:
        try:
            api_key = ApiKey.generate(description)
            self._repository.store_api_key(api_key)
            return api_key
        except Exception as e:
            raise

    def validate_api_key(self, key: str) -> bool:
        """Validate the provided API key and update last used timestamp"""
        try:
            api_key = self._repository.get_api_key(key)
            if not api_key:
                return False

            # Update last used timestamp
            now = datetime.now(UTC)
            try:
                self._repository.update_api_key(key, now)
            except Exception as e:
                pass
                # Continue even if update_last_used fails

            return True

        except DatabaseException as e:
            raise e
        except Exception as e:
            raise e
