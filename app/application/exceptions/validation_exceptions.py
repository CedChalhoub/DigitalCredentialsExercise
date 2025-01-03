from app.application.exceptions.application_exception import ApplicationException


class CredentialValidationException(ApplicationException):
    def __init__(self, message):
        super().__init__(f'Validation failed: {message}')