from fastapi import HTTPException, status

class TaskTrackerHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class ConflictException(TaskTrackerHTTPException):
    def __init__(self, detail="Resourse Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class InvalidPasswordException(TaskTrackerHTTPException):
    def __init__(self, detail="Password mismatch error"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)