from app.domain import Credential
from app.domain.CredentialFactory import CredentialFactory
from app.domain.Entity import Entity


class FedGovEntity(Entity):
    def __init__(self, name: str):
        super().__init__(name)

    def issue_credential(self, credential_type: str) -> Credential:
        credentialFactory: CredentialFactory = CredentialFactory()
        return credentialFactory.create(credential_type)
