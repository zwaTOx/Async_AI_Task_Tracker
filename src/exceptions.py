from fastapi import HTTPException, status

class TaskTrackerHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class ConflictException(TaskTrackerHTTPException):
    def __init__(self, detail="Resourse Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class InvalidPasswordException(TaskTrackerHTTPException):
    def __init__(self, detail="Пароли не совпадают"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class BadRequestException(TaskTrackerHTTPException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class AuthException(TaskTrackerHTTPException):
    def __init__(self, detail="Authentication failed"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class PermissionException(TaskTrackerHTTPException):
    def __init__(self, detail="Доступ запрещен"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class NotFoundException(TaskTrackerHTTPException):
    def __init__(self, detail="Не найдено"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class IternalServerException(TaskTrackerHTTPException):
    def __init__(self, detail="Ошибка отправки"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class TooLargeEntityException(TaskTrackerHTTPException):
    def __init__(self, detail):
        super().__init__(status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail=detail)