"""
Upload API endpoint
"""
from fastapi import APIRouter, File, UploadFile, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.utils.file_validation import validate_file
from app.models.db import Media
from app.services.orchestrator import start_processing
import os
import shutil
from uuid import uuid4
from PIL import Image
from app.utils.ffmpeg import get_audio_duration, extract_video_metadata

router = APIRouter()

STORAGE_PATH = os.getenv("STORAGE_PATH", "./storage")
os.makedirs(STORAGE_PATH, exist_ok=True)

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Upload media file (image, audio, or video)
    Validates file, saves to storage, creates DB record, starts processing
    """
    # Generate unique ID
    media_id = str(uuid4())
    
    # Create temp file
    temp_path = os.path.join(STORAGE_PATH, f"temp_{media_id}")
    
    try:
        # Save uploaded file
        print(f"DEBUG: Saving file {file.filename} to {temp_path}")
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        file_size_bytes = os.path.getsize(temp_path)
        print(f"DEBUG: File saved. Size: {file_size_bytes} bytes")

        # Validate file
        print("DEBUG: Starting validation...")
        media_type, file_size = validate_file(temp_path)
        print(f"DEBUG: Validation successful. Type: {media_type}")
        
        # Move to permanent location
        file_extension = os.path.splitext(file.filename)[1]
        final_path = os.path.join(STORAGE_PATH, f"{media_id}{file_extension}")
        shutil.move(temp_path, final_path)
        
        # Extract metadata based on media type
        duration = None
        width = None
        height = None
        
        if media_type == "image":
            img = Image.open(final_path)
            width, height = img.size
            img.close()
        elif media_type == "audio":
            duration = get_audio_duration(final_path)
        elif media_type == "video":
            duration, width, height = extract_video_metadata(final_path)
        elif media_type == "text":
            # Text files don't have duration/dimensions
            pass
        
        # Create media record
        media = Media(
            id=media_id,
            filename=file.filename,
            media_type=media_type,
            size_bytes=file_size,
            duration=duration,
            width=width,
            height=height
        )
        
        db.add(media)
        db.commit()
        
        # Start background processing
        if background_tasks:
            background_tasks.add_task(
                run_async_processing,
                media_id=media_id,
                file_path=final_path,
                storage_dir=STORAGE_PATH
            )
        
        
        return {
            "media_id": media_id,
            "filename": file.filename,
            "media_type": media_type,
            "status": "processing"
        }
        
    except ValueError as e:
        # Validation error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        # Other errors
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# Helper function for async processing
import asyncio
from app.utils.database import SessionLocal

def run_async_processing(media_id, file_path, storage_dir):
    """Wrapper to run async processing in background task"""
    # Create new session for background task
    db = SessionLocal()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(
            start_processing(db, media_id, file_path, storage_dir)
        )
    except Exception as e:
        print(f"Background processing failed: {e}")
    finally:
        db.close()
        loop.close()
