from fastapi import status
from typing import Callable, Dict

from app.rest.exceptions.api_exception import APIException
from app.rest.exceptions.assembler_exception import AssemblerException
from app.rest.exceptions.invalid_credential_data_exception import InvalidCredentialDataException
from app.application.exceptions.validation_exceptions import CredentialValidationException
from app.domain.exceptions.credential.credential_not_found_exception import CredentialNotFoundException
from app.domain.exceptions.credential.expired_credential_exception import ExpiredCredentialException
from app.domain.exceptions.credential.invalid_credential_state_exception import InvalidCredentialStateException
from app.domain.exceptions.unauthorized_issuer_exception import UnauthorizedIssuerException
from app.infrastructure.exceptions.database_connection_exception import DatabaseConnectionException
from app.infrastructure.exceptions.database_exception import DatabaseException
from app.infrastructure.exceptions.database_operation_exception import DatabaseOperationException

ExceptionHandler = Callable[[Exception], APIException]

class ExceptionHandlerRegistry:
    _handlers: Dict[Exception, ExceptionHandler] = {
        # Domain Exceptions
        CredentialNotFoundException: lambda e: APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ),
        InvalidCredentialStateException: lambda e: APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ),
        UnauthorizedIssuerException: lambda e: APIException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        ),
        ExpiredCredentialException: lambda e: APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ),

        # Application Exceptions
        CredentialValidationException: lambda e: APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ),

        # API/Assembler Exceptions
        AssemblerException: lambda e: APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ),
        InvalidCredentialDataException: lambda e: APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ),

        # Infrastructure Exceptions
        DatabaseException: lambda e: APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ),
        DatabaseConnectionException: lambda e: APIException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        ),
        DatabaseOperationException: lambda e: APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    }

    @classmethod
    def register(cls, exception_class: Exception, handler: ExceptionHandler):
        cls._handlers[exception_class] = handler

    @classmethod
    def get_handler(cls, exception: Exception) -> APIException:
        for exc_type, handler in cls._handlers.items():
            if isinstance(exception, exc_type):
                return handler(exception)

        return APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal server error'
        )