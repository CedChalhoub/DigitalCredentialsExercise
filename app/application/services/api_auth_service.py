# app/application/services/api_auth_service.py
from datetime import datetime, UTC
import logging
import traceback
from app.domain.models.api_key import ApiKey
from app.domain.repositories.api_key_repository import AbstractApiKeyRepository
from app.infrastructure.exceptions.database_exception import DatabaseException

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ApiAuthService:
    def __init__(self, api_key_repository: AbstractApiKeyRepository):
        self._repository = api_key_repository
        logger.info("ApiAuthService initialized")

    def generate_api_key(self, description: str | None = None) -> ApiKey:
        """Generate and store a new API key"""
        try:
            logger.info("Generating new API key")
            api_key = ApiKey.generate(description)
            self._repository.store_api_key(api_key)
            logger.info(f"Generated and stored new API key: {api_key.key}...")
            return api_key
        except Exception as e:
            logger.error(f"Error generating API key: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def validate_api_key(self, key: str) -> bool:
        """Validate the provided API key and update last used timestamp"""
        try:
            logger.debug(f"Starting validation for API key: {key}...")

            api_key = self._repository.get_api_key(key)
            logger.debug(f"Repository get_api_key result: {api_key is not None}")

            if not api_key:
                logger.warning(f"API key not found: {key}...")
                return False

            # Update last used timestamp
            now = datetime.now(UTC)
            try:
                self._repository.update_api_key(key, now)
                logger.debug("Updated last_used timestamp successfully")
            except Exception as e:
                logger.warning(f"Failed to update last_used timestamp: {str(e)}")
                # Continue even if update_last_used fails

            return True

        except DatabaseException as e:
            logger.error(f"Database error validating API key: {str(e)}")
            logger.error(traceback.format_exc())
            raise
        except Exception as e:
            logger.error(f"Unexpected error validating API key: {str(e)}")
            logger.error(traceback.format_exc())
            raise
