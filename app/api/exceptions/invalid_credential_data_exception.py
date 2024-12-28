from app.api.exceptions.assembler_exception import AssemblerException


class InvalidCredentialDataException(AssemblerException):
    def __init__(self, field: str, detail: str):
        super().__init__(f"Invalid credential data for field '{field}': {detail}")