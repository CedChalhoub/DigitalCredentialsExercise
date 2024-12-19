from datetime import datetime
from uuid import UUID

from app.api.dto.AssemblerRegistry import AssemblerRegistry
from app.api.dto.CredentialAssembler import CredentialAssembler
from app.api.dto.DriversLicenseDTO import DriversLicenseDTO
from app.domain.DriversLicense import DriversLicense

@AssemblerRegistry.register("drivers_license")
class DriversLicenseAssembler(CredentialAssembler):
    def to_dto(self, drivers_license: DriversLicense) -> DriversLicenseDTO:
        return DriversLicenseDTO(
            issuer_id=str(drivers_license.issuer_id),
            holder_id=drivers_license.holder_id,
            valid_from=drivers_license.valid_from.isoformat(),
            valid_until=drivers_license.valid_until.isoformat(),
            status=drivers_license.status.value,
            suspension_reason=drivers_license.suspension_reason,
            revocation_reason=drivers_license.revocation_reason,
            vehicle_classes=drivers_license.vehicle_classes,
            issuing_province=drivers_license.issuing_province
        )

    def to_domain(self, license_dto: DriversLicenseDTO) -> DriversLicense:
        return DriversLicense(
            issuer_id=UUID(license_dto.issuer_id),
            holder_id=license_dto.holder_id,
            valid_from=datetime.fromisoformat(license_dto.valid_from),
            valid_until=datetime.fromisoformat(license_dto.valid_until),
            vehicle_classes=license_dto.vehicle_classes,
            issuing_province=license_dto.issuing_province
        )