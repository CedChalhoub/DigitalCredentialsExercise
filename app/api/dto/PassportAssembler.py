from datetime import datetime
from uuid import UUID

from app.api.dto.AssemblerRegistry import AssemblerRegistry
from app.api.dto.CredentialAssembler import CredentialAssembler
from app.domain.Passport import Passport
from app.api.dto.PassportDTO import PassportDTO

@AssemblerRegistry.register("passport")
class PassportAssembler(CredentialAssembler):
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
    def to_domain(self, credential_dto: dict) -> Passport:
        return Passport(
            holder_id=credential_dto['holder_id'],
            issuer_id=credential_dto['issuer_id'],
            valid_from=datetime.fromisoformat(credential_dto['valid_from']),
            valid_until=datetime.fromisoformat(credential_dto['valid_until']),
            nationality=credential_dto['nationality'],
            issuing_country=credential_dto['issuing_country']
        )