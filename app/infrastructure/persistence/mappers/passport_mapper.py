from datetime import datetime, UTC

from app.domain.enums.credential_status import CredentialStatus
from app.domain.enums.credential_type import CredentialType
from app.domain.models.passport import Passport
from app.infrastructure.persistence.mappers.credential_mapper import CredentialMapper


class PassportMapper(CredentialMapper):
    def to_dynamo(self, credential: Passport) -> dict:
        return {
            'PK': f'CRED#{credential.issuing_country}#{str(credential.credential_id)}',
            'SK': f'METADATA#passport',
            'credential_type': CredentialType.PASSPORT.value,
            'credential_id': str(credential.credential_id),
            'valid_from': credential.valid_from.isoformat(),
            'valid_until': credential.valid_until.isoformat(),
            'status': credential.status.value,
            'nationality': credential.nationality,
            'issuing_country': credential.issuing_country,
            'suspension_reason': credential.suspension_reason,
            'revocation_reason': credential.revocation_reason,
            'created_at': datetime.now(UTC).isoformat(),
            'updated_at': datetime.now(UTC).isoformat(),
            'version': 1
        }

    def to_domain(self, item: dict) -> Passport:
        passport: Passport = Passport(
            credential_id=item['credential_id'],
            valid_from=datetime.fromisoformat(item['valid_from']),
            valid_until=datetime.fromisoformat(item['valid_until']),
            nationality=item['nationality'],
            issuing_country=item['issuing_country']
        )
        passport.set_suspension_reason(item['suspension_reason'])
        passport.set_revocation_reason(item['revocation_reason'])
        passport.set_status(CredentialStatus(item['status']))

        return passport
