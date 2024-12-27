from abc import abstractmethod, ABC
from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from app.domain.CredentialStatus import CredentialStatus
from app.domain.CredentialType import CredentialType
from app.domain.EntityType import EntityType


class Credential(ABC):

    def __init__(self, issuer_id: str, holder_id: str, valid_from: datetime, valid_until: datetime):
        self._issuer_id = issuer_id
        self._holder_id = holder_id

        if valid_from.tzinfo is None:
            raise ValueError("valid_from must be timezone-aware")
        if valid_until.tzinfo is None:
            raise ValueError("valid_until must be timezone-aware")

        self._valid_from = valid_from.astimezone(timezone.utc)
        self._valid_until = valid_until.astimezone(timezone.utc)
        self._status = CredentialStatus.ACTIVE
        self._suspension_reason: Optional[str] = None
        self._revocation_reason: Optional[str] = None

    @abstractmethod
    def _validate_holder_id(self, holder_id: str) -> None:
        """Validate the holder_id"""
        pass

    @abstractmethod
    def get_credential_type(self) -> CredentialType:
        pass

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def issuer_id(self) -> UUID:
        return self._issuer_id

    @property
    def holder_id(self) -> str:
        return self._holder_id

    @property
    def status(self) -> CredentialStatus:
        return self._status

    @property
    @abstractmethod
    def authorized_issuers(self) -> List[EntityType]:
        """List of entity types authorized to issue this credential"""
        pass

    def suspend(self, reason: str) -> None:
        # TODO: Add validation
        self._status = CredentialStatus.SUSPENDED
        self._suspension_reason = reason

    def reinstate(self) -> None:
        # TODO: Add validation
        self._status = CredentialStatus.ACTIVE
        self._suspension_reason = None

    def revoke(self, reason: str) -> None :
        # TODO: Add validation
        self._status = CredentialStatus.REVOKED
        self._revocation_reason = reason

    def is_valid(self) -> bool:
        return ((self._status == CredentialStatus.ACTIVE)
                and (datetime.now() >= self._valid_from)
                and (datetime.now() <= self._valid_until))

    @property
    def valid_from(self):
        return self._valid_from

    @property
    def valid_until(self):
        return self._valid_until

    @property
    def suspension_reason(self):
        return self._suspension_reason

    @property
    def revocation_reason(self):
        return self._revocation_reason