from datetime import datetime

from app.rest.assemblers.assembler_registry import AssemblerRegistry
from app.rest.assemblers.credential_assembler import CredentialAssembler
from app.rest.exceptions.invalid_credential_data_exception import InvalidCredentialDataException
from app.domain.models.passport import Passport
from app.rest.dto.passport_dto import PassportDTO

@AssemblerRegistry.register("passport")
class PassportAssembler(CredentialAssembler):
    def _to_specific_dto(self, credential_dict: dict) -> PassportDTO:
        try:
            return PassportDTO(**credential_dict)
        except ValueError as e:
            raise InvalidCredentialDataException("format", str(e))

    def to_dto(self, passport: Passport) -> PassportDTO:
        try:
            return PassportDTO(
                issuer_id=str(passport.issuer_id),
                holder_id=passport.holder_id,
                valid_from=passport.valid_from.isoformat(),
                valid_until=passport.valid_until.isoformat(),
                status=passport.status.value,
                suspension_reason=passport.suspension_reason,
                revocation_reason=passport.revocation_reason,
                nationality=passport.nationality,
                issuing_country=passport.issuing_country
            )
        except Exception as e:
            raise InvalidCredentialDataException("conversion", f"Failed to write the passport: {str(e)}"
                                                 )
    def to_domain(self, credential_dto: dict) -> Passport:
        passport_dto = self._to_specific_dto(credential_dto)
        return Passport(
            holder_id=passport_dto.holder_id,
            issuer_id=passport_dto.issuer_id,
            valid_from=datetime.fromisoformat(passport_dto.valid_from),
            valid_until=datetime.fromisoformat(passport_dto.valid_until),
            nationality=passport_dto.nationality,
            issuing_country=passport_dto.issuing_country
        )