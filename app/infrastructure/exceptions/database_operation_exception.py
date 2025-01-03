from app.infrastructure.exceptions.database_exception import DatabaseException


class DatabaseOperationException(DatabaseException):
    def __init__(self, operation: str, detail: str):
        super().__init__(f'Failed to {operation}: {detail}')