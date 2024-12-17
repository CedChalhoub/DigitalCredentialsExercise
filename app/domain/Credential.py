from app.domain.CredentialStatus import CredentialStatus


class Credential:
    def __init__(self, credential_id: str, credential_type: CredentialStatus):
        self.credential_id = credential_id
        self.credential_type = credential_type
