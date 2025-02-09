from typing import Any, List
import traceback

class ApiError(Exception):
    def __init__(
        self,
        status_code: int,
        message: str = "Something went wrong",
        errors: List[Any] = None,
        stack: str = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.data = None
        self.message = message
        self.success = False
        self.errors = errors or []

        # Capture stack trace if not provided
        self.stack = stack if stack else traceback.format_exc()

__all__ = ["ApiError"]  # Explicit export
