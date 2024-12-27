from datetime import datetime

from app.api.dto.AssemblerRegistry import AssemblerRegistry
from app.api.dto.CredentialAssembler import CredentialAssembler
from app.api.dto.CredentialDTO import CredentialDTO
from app.domain.Passport import Passport
from app.api.dto.PassportDTO import PassportDTO

@AssemblerRegistry.register("passport")
class PassportAssembler(CredentialAssembler):
    def _to_specific_dto(self, credential_dict: dict) -> PassportDTO:
        return PassportDTO(**credential_dict)

    def to_dto(self, passport: Passport) -> PassportDTO:
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
    def to_domain(self, credential_dto: CredentialDTO) -> Passport:
        passport_dto = self._to_specific_dto(credential_dto)
        return Passport(
            holder_id=passport_dto.holder_id,
            issuer_id=passport_dto.issuer_id,
            valid_from=datetime.fromisoformat(passport_dto.valid_from),
            valid_until=datetime.fromisoformat(passport_dto.valid_until),
            nationality=passport_dto.nationality,
            issuing_country=passport_dto.issuing_country
        )