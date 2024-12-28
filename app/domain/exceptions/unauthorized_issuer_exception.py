from app.domain.exceptions.domain_exception import DomainException


class UnauthorizedIssuerException(DomainException):
    def __init__(self, issuer: str, credential_type: str):
        self._issuer = issuer
        self._credential_type = credential_type
        super().__init__(f"Issuer '{self._issuer}' is not authorized to issue credential of type '{self._credential_type}'.")