from abc import abstractmethod, ABC
from datetime import datetime, timezone, UTC
from typing import Optional, List
from uuid import UUID

from app.domain.credential_status import CredentialStatus
from app.domain.credential_type import CredentialType
from app.domain.entity_type import EntityType
from app.domain.exceptions.credential.expired_credential_exception import ExpiredCredentialException
from app.domain.exceptions.credential.invalid_credential_state_exception import InvalidCredentialStateException


class Credential(ABC):

    def __init__(self, issuer_id: str, holder_id: str, valid_from: datetime, valid_until: datetime):
        self._issuer_id = issuer_id
        self._holder_id = holder_id

        if valid_from.tzinfo is None:
            raise ValueError("valid_from must be timezone-aware")
        if valid_until.tzinfo is None:
            raise ValueError("valid_until must be timezone-aware")

        if valid_until < valid_from:
            raise InvalidCredentialStateException("valid_until must be after valid_from")

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
        if not reason:
            raise InvalidCredentialStateException("Suspension reason cannot be empty")

        if self._status == CredentialStatus.REVOKED:
            raise InvalidCredentialStateException("Cannot suspend a revoked credential")
        self._status = CredentialStatus.SUSPENDED
        self.set_suspension_reason(reason)

    def reinstate(self) -> None:
        if self._status == CredentialStatus.REVOKED:
            raise InvalidCredentialStateException("Cannot reinstate a revoked credential")

        self._status = CredentialStatus.ACTIVE
        self.set_suspension_reason(None)
        self.set_suspension_reason(None)

    def revoke(self, reason: str) -> None :
        if not reason:
            raise InvalidCredentialStateException("Revocation reason cannot be empty")
        self._status = CredentialStatus.REVOKED
        self.set_revocation_reason(reason)

    def is_valid(self) -> bool:
        now = datetime.now(UTC)

        if now > self._valid_until:
            raise ExpiredCredentialException(self._valid_until)

        return ((self._status == CredentialStatus.ACTIVE)
                and (now >= self._valid_from)
                and (now <= self._valid_until))

    def set_suspension_reason(self, reason: str | None):
        self._suspension_reason = reason

    def set_revocation_reason(self, reason: str | None):
        self._revocation_reason = reason

    def set_status(self, value):
        self._status = value

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

    def update_status(self, status: CredentialStatus, reason: str | None) -> None:
        match status:
            case CredentialStatus.SUSPENDED:
                self.suspend(reason)
            case CredentialStatus.REVOKED:
                self.revoke(reason)
            case CredentialStatus.ACTIVE:
                self.reinstate()