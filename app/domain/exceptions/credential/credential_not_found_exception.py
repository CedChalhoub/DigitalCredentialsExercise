from app.domain.exceptions.domain_exception import DomainException


class CredentialNotFoundException(DomainException):
    def __init__(self, credential_id: str, credential_type: str):
        self._credential_id = credential_id
        self._credential_type = credential_type

        super().__init__(f"Credential with id '{self._credential_id}' of type '{self._credential_type}' not found.")