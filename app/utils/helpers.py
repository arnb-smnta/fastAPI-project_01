import os
import logging
from typing import Optional
from starlette.requests import Request

logger = logging.getLogger(__name__)

def remove_local_file(file_path: str):
    """Helper function to remove a local file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")

def remove_unused_uploaded_files_on_error(request: Request):
    """
    Removes uploaded files if an error occurs during request processing.
    """
    try:
        files = request.state.files  # Assuming files are stored in request.state.files
        
        if isinstance(files, list):  # Multiple files case
            for file in files:
                remove_local_file(file.filename)

        elif isinstance(files, dict):  # If files are stored as a dictionary by field
            for field_files in files.values():
                for file in field_files:
                    remove_local_file(file.filename)

    except Exception as error:
        logger.error(f"Error while removing uploaded files: {error}")
