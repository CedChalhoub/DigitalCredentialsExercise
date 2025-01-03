from datetime import datetime, UTC

from app.domain.enums.credential_status import CredentialStatus
from app.domain.enums.credential_type import CredentialType
from app.domain.models.drivers_license import DriversLicense
from app.infrastructure.persistence.mappers.credential_mapper import CredentialMapper


class DriversLicenseMapper(CredentialMapper):
    def to_dynamo(self, credential: DriversLicense) -> dict:
        return {
            'PK': f'CRED#{credential.issuing_country}#{str(credential.credential_id)}',
            'SK': f'METADATA#drivers_license',
            'credential_type': CredentialType.DRIVERS_LICENSE.value,
            'credential_id': str(credential.credential_id),
            'valid_from': credential.valid_from.isoformat(),
            'valid_until': credential.valid_until.isoformat(),
            'status': credential.status.value,
            'vehicle_classes': credential.vehicle_classes,
            'issuing_region': credential.issuing_region,
            'issuing_country': credential.issuing_country,
            'suspension_reason': credential.suspension_reason,
            'revocation_reason': credential.revocation_reason,
            'created_at': datetime.now(UTC).isoformat(),
            'updated_at': datetime.now(UTC).isoformat(),
            'version': 1
        }
    def to_domain(self, item: dict) -> DriversLicense:
        drivers_license: DriversLicense = DriversLicense(
            credential_id=item['credential_id'],
            valid_from=datetime.fromisoformat(item['valid_from']),
            valid_until=datetime.fromisoformat(item['valid_until']),
            vehicle_classes=item['vehicle_classes'],
            issuing_country=item['issuing_country'],
            issuing_region=item['issuing_region'])

        drivers_license.set_suspension_reason(item['suspension_reason'])
        drivers_license.set_revocation_reason(item['revocation_reason'])
        drivers_license.set_status(CredentialStatus(item['status']))
        return drivers_license