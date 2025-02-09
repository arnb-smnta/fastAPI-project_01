import os
import shutil
from datetime import datetime
from fastapi import UploadFile, File, HTTPException
from pathlib import Path
import random

# Define the upload directory
UPLOAD_DIR = Path("./public/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

def save_uploaded_file(uploaded_file: UploadFile) -> str:
    """
    Handles file upload and saves it to the specified directory with a unique filename.

    Args:
        uploaded_file (UploadFile): The file uploaded via FastAPI.

    Returns:
        str: The saved file path.
    """
    file_extension = Path(uploaded_file.filename).suffix  # Extract file extension
    filename_without_ext = Path(uploaded_file.filename).stem.lower().replace(" ", "-")
    
    # Generate a unique filename to avoid conflicts
    unique_filename = f"{filename_without_ext}-{int(datetime.utcnow().timestamp())}-{random.randint(10000, 99999)}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    # Save the file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    return str(file_path)

__all__ = ["save_uploaded_file"]
