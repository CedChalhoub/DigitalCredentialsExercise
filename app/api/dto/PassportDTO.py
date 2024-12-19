from app.api.dto.CredentialDTO import CredentialDTO


class PassportDTO(CredentialDTO):
    nationality: str
    issuing_country: str