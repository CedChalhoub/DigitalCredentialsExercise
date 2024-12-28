from app.infrastructure.exceptions.database_exception import DatabaseException


class DatabaseConnectionException(DatabaseException):
    def __init__(self, message: str = 'Failed to connect to database'):
        super().__init__(message)