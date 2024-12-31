from datetime import datetime

from app.interfaces.rest.dto.assembler_registry import AssemblerRegistry
from app.interfaces.rest.dto.credential_assembler import CredentialAssembler
from app.interfaces.rest.dto.credential_dto import CredentialDTO
from app.interfaces.rest.dto.drivers_license_dto import DriversLicenseDTO
from app.interfaces.rest.exceptions.invalid_credential_data_exception import InvalidCredentialDataException
from app.domain.models.drivers_license import DriversLicense

@AssemblerRegistry.register("drivers_license")
class DriversLicenseAssembler(CredentialAssembler):
    def _to_specific_dto(self, credential_dict: dict) -> DriversLicenseDTO:
        try:
            return DriversLicenseDTO(**credential_dict)
        except ValueError as e:
            raise InvalidCredentialDataException("format", str(e))
    def to_dto(self, drivers_license: DriversLicense) -> DriversLicenseDTO:
        return DriversLicenseDTO(
            issuer_id=str(drivers_license.issuer_id),
            holder_id=drivers_license.holder_id,
            valid_from=drivers_license.valid_from.isoformat(),
            valid_until=drivers_license.valid_until.isoformat(),
            issuing_country=drivers_license.issuing_country,
            status=drivers_license.status.value,
            suspension_reason=drivers_license.suspension_reason,
            revocation_reason=drivers_license.revocation_reason,
            vehicle_classes=drivers_license.vehicle_classes,
            issuing_region=drivers_license.issuing_region
        )

    def to_domain(self, credential_dto: CredentialDTO) -> DriversLicense:
        license_dto = self._to_specific_dto(credential_dto)
        return DriversLicense(
            issuer_id=license_dto.issuer_id,
            holder_id=license_dto.holder_id,
            valid_from=datetime.fromisoformat(license_dto.valid_from),
            valid_until=datetime.fromisoformat(license_dto.valid_until),
            issuing_country=license_dto.issuing_country,
            vehicle_classes=license_dto.vehicle_classes,
            issuing_region=license_dto.issuing_region
        )