"""
File validation utilities
"""
import os
import magic
from typing import Tuple

# Allowed MIME types
ALLOWED_MIME_TYPES = {
    "image": ["image/jpeg", "image/png", "image/gif", "image/webp"],
    "audio": ["audio/mpeg", "audio/wav", "audio/ogg", "audio/mp4", "audio/x-m4a"],
    "video": ["video/mp4", "video/mpeg", "video/quicktime", "video/x-msvideo", "video/webm"]
}

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE_MB", "100")) * 1024 * 1024  # Default 100MB

def detect_media_type(file_path: str) -> str:
    """Detect media type from file"""
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)
    
    for media_type, allowed_mimes in ALLOWED_MIME_TYPES.items():
        if mime_type in allowed_mimes:
            return media_type
    
    raise ValueError(f"Unsupported file type: {mime_type}")

def validate_file(file_path: str) -> Tuple[str, int]:
    """
    Validate uploaded file
    Returns: (media_type, file_size)
    Raises: ValueError if invalid
    """
    # Check file exists
    if not os.path.exists(file_path):
        raise ValueError("File not found")
    
    # Check file size
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB")
    
    if file_size == 0:
        raise ValueError("File is empty")
    
    # Detect and validate media type
    media_type = detect_media_type(file_path)
    
    return media_type, file_size
