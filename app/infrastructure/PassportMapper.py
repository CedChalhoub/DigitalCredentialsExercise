from datetime import datetime, UTC
from uuid import UUID

from app.domain.Passport import Passport
from app.infrastructure.AbstractCredentialMapper import AbstractCredentialMapper


class PassportMapper(AbstractCredentialMapper):
    def to_dynamo(self, credential: Passport) -> dict:
        return {
            'PK': f'CRED#{str(credential.id)}',
            'SK': f'METADATA#passport',
            'credential_id': str(credential.id),
            'credential_type': 'passport',
            'issuer_id': str(credential.issuer_id),
            'holder_id': credential.holder_id,
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
        return Passport(
            issuer_id=UUID(item['issuer_id']),
            holder_id=item['holder_id'],
            valid_from=datetime.fromisoformat(item['valid_from']),
            valid_until=datetime.fromisoformat(item['valid_until']),
            nationality=item['nationality'],
            issuing_country=item['issuing_country']
        )

    def get_type(self) -> str:
        return 'passport'