from app.rest.dto.credential_dto import CredentialDTO


class PassportDTO(CredentialDTO):
    nationality: str
    issuing_country: str