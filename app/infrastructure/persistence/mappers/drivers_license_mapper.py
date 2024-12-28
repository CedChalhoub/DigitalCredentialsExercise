from abc import ABC
from datetime import datetime, UTC

from app.domain.enums.credential_status import CredentialStatus
from app.domain.enums.credential_type import CredentialType
from app.domain.models.drivers_license import DriversLicense
from app.application.interfaces.credential_mapper import AbstractCredentialMapper

class DriversLicenseMapper(AbstractCredentialMapper, ABC):
    def to_dynamo(self, credential: DriversLicense) -> dict:
        return {
            'PK': f'CRED#{str(credential.issuer_id)}',
            'SK': f'METADATA#drivers_license',
            'credential_type': CredentialType.DRIVERS_LICENSE.value,
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
        license: DriversLicense = DriversLicense(
            issuer_id=item['issuer_id'],
            holder_id=item['holder_id'],
            valid_from=datetime.fromisoformat(item['valid_from']),
            valid_until=datetime.fromisoformat(item['valid_until']),
            vehicle_classes=item['vehicle_classes'],
            issuing_province=item['issuing_province'])

        license.set_suspension_reason(item['suspension_reason'])
        license.set_revocation_reason(item['revocation_reason'])
        license.set_status(CredentialStatus(item['status']))
        return license