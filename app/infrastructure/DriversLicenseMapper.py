from datetime import datetime, UTC
from uuid import UUID

from app.domain.DriversLicense import DriversLicense
from app.infrastructure.AbstractCredentialMapper import AbstractCredentialMapper


class DriversLicenseMapper(AbstractCredentialMapper):
    def to_dynamo(self, credential: DriversLicense) -> dict:
        return {
            'PK': f'CRED#{str(credential.id)}',
            'SK': f'METADATA#drivers_license',
            'credential_id': str(credential.id),
            'credential_type': 'drivers_license',
            'issuer_id': str(credential.issuer_id),
            'holder_id': credential.holder_id,
            'valid_from': credential.valid_from.isoformat(),
            'valid_until': credential.valid_until.isoformat(),
            'status': credential.status.value,
            'vehicle_classes': credential.vehicle_classes,
            'issuing_province': credential.issuing_province,
            'suspension_reason': credential.suspension_reason,
            'revocation_reason': credential.revocation_reason,
            'created_at': datetime.now(UTC).isoformat(),
            'updated_at': datetime.now(UTC).isoformat(),
            'version': 1
        }
    def to_domain(self, item: dict) -> DriversLicense:
        return DriversLicense(
            issuer_id=UUID(item['issuer_id']),
            holder_id=item['holder_id'],
            valid_from=datetime.fromisoformat(item['valid_from']),
            valid_until=datetime.fromisoformat(item['valid_until']),
            vehicle_classes=item['vehicle_classes'],
            issuing_province=item['issuing_province']
        )

    # TODO: This needs to be handled in a better way
    def get_type(self) -> str:
        return 'drivers_license'