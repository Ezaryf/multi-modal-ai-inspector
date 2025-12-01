"""
File validation utilities
"""
import os
import magic
from typing import Tuple

# Allowed MIME types
ALLOWED_MIME_TYPES = {
    "image": ["image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp", "image/tiff"],
    "audio": ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/ogg", "audio/mp4", "audio/x-m4a", "audio/aac"],
    "video": ["video/mp4", "video/mpeg", "video/quicktime", "video/x-msvideo", "video/webm", "video/x-matroska", "video/avi"],
    "text": ["text/plain", "text/csv", "text/markdown"]
}

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE_MB", "100")) * 1024 * 1024  # Default 100MB

def detect_media_type(file_path: str) -> str:
    """Detect media type from file"""
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)
    print(f"DEBUG: Detected MIME type: {mime_type} for {file_path}")
    
    for media_type, allowed_mimes in ALLOWED_MIME_TYPES.items():
        if mime_type in allowed_mimes:
            return media_type
            
    # Fallback: Check extension if magic fails or returns generic
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.jpg', '.jpeg']: return 'image'
    if ext in ['.png']: return 'image'
    if ext in ['.mp3']: return 'audio'
    if ext in ['.mp4']: return 'video'
    if ext in ['.wav']: return 'audio'
    if ext in ['.txt', '.md', '.csv']: return 'text'
    
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
    print(f"DEBUG: File size: {file_size} bytes. Max: {MAX_FILE_SIZE}")
    if file_size > MAX_FILE_SIZE:
        print(f"DEBUG: File too large!")
        raise ValueError(f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB")
    
    if file_size == 0:
        raise ValueError("File is empty")
    
    # Detect and validate media type
    media_type = detect_media_type(file_path)
    
    return media_type, file_size
