from datetime import datetime

from app.domain.exceptions.domain_exception import DomainException


class ExpiredCredentialException(DomainException):
    def __init__(self, expiry_date: datetime):
        super().__init__(f"Credential has expired on {expiry_date}.")