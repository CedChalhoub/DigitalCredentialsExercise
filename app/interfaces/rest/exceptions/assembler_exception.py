from app.interfaces.rest.exceptions.api_exception import APIException


class AssemblerException(APIException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail = detail)