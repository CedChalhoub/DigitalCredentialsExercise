from app.domain.Credential import Credential


class DriversLicense(Credential):
    def __init__(self):
        super().__init__(credential_id=self.credential_id)
