from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.models.api_key import ApiKey

class AbstractApiKeyRepository(ABC):
    @abstractmethod
    def store_api_key(self, api_key: ApiKey) -> None:
        pass

    @abstractmethod
    def get_api_key(self, key: str) -> ApiKey | None:
        pass

    @abstractmethod
    def update_api_key(self, key: str, timestamp: datetime) -> None:
        pass