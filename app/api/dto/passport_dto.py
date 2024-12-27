from app.api.dto.credential_dto import CredentialDTO


class PassportDTO(CredentialDTO):
    nationality: str
    issuing_country: str