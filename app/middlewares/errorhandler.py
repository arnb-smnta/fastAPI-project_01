import traceback
import logging
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError
from utils.apierror import ApiError  # Assuming ApiError is already defined
from utils.helpers import remove_unused_uploaded_files_on_error  # Custom helper
from dotenv import load_dotenv
import os
#Loading dot env
load_dotenv()

logger = logging.getLogger("uvicorn.error")

async def error_handler(request: Request, exc: Exception) -> Response:
    """Global error handler for FastAPI"""
    
    if not isinstance(exc, ApiError):
        # Assign appropriate status code
        status_code = getattr(exc, "status_code", 400 if isinstance(exc, PyMongoError) else 500)
        
        # Set a meaningful message
        message = str(exc) or "Something went wrong"
        
        # Convert it into ApiError for consistency
        exc = ApiError(status_code, message, stack=traceback.format_exc())

    # Create response payload
    response = {
        "status_code": exc.status_code,
        "message": exc.message,
        "errors": exc.errors,
        "success": False,
    }

    # Include stack trace in development mode
    if os.getenv("environment")== "development":  # Assuming settings.py manages ENV variables
        response["stack"] = exc.stack

    logger.error(f"Error: {exc.message}")

    await remove_unused_uploaded_files_on_error(request)

    return JSONResponse(status_code=exc.status_code, content=response)

__all__ = ["error_handler"]
