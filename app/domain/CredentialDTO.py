from pydantic import BaseModel


class CredentialDTO(BaseModel):
    credential_type: str
    credential_entity: str
    issuee_first_name: str
    issuee_last_name: str
    issuee_address: str | None # Optional depending on if required by credential
    drivers_license_type: str | None # Optional depending on if required by credential

    # @validator("fieldname")
    # def validate()