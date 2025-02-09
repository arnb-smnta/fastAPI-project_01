from typing import Any
from pydantic import BaseModel

class ApiResponse(BaseModel):
    status_code: int
    data: Any
    message: str = "Success"
    success: bool

    def __init__(self, status_code: int, data: Any, message: str = "Success"):
        super().__init__(
            status_code=status_code,
            data=data,
            message=message,
            success=status_code < 400
        )

__all__ = ["ApiResponse"]  # Explicit export
