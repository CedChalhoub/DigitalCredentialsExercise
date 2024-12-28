from app.domain.exceptions.domain_exception import DomainException


class InvalidCredentialStateException(DomainException):
    def __init__(self, message: str):
        super().__init__(message)