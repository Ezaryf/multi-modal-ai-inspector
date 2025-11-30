"""
Batch processing API endpoints
Upload and process multiple files at once
"""
from fastapi import APIRouter, File, UploadFile, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.db import Media
from typing import List
import os
from uuid import uuid4
from datetime import datetime

router = APIRouter()

STORAGE_PATH = os.getenv("STORAGE_PATH", "./storage")

# Simple in-memory batch job tracking (use Redis/Celery for production)
batch_jobs = {}

@router.post("/batch/upload")
async def batch_upload(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Upload multiple files in batch
    Returns batch job ID for tracking
    """
    if len(files) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 files per batch")
    
    batch_id = str(uuid4())
    uploaded_media = []
    
    for file in files:
        try:
            # Generate unique ID
            media_id = str(uuid4())
            
            # Save file
            file_extension = os.path.splitext(file.filename)[1]
            file_path = os.path.join(STORAGE_PATH, f"{media_id}{file_extension}")
            
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Get file size
            file_size = len(content)
            
            # Create media record (minimal metadata for now)
            media = Media(
                id=media_id,
                filename=file.filename,
                media_type="unknown",  # Will be detected during processing
                size_bytes=file_size
            )
            
            db.add(media)
            uploaded_media.append({
                "media_id": media_id,
                "filename": file.filename,
                "status": "pending"
            })
            
        except Exception as e:
            uploaded_media.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })
    
    db.commit()
    
    # Store batch job
    batch_jobs[batch_id] = {
        "id": batch_id,
        "created_at": datetime.now().isoformat(),
        "total_files": len(files),
        "files": uploaded_media,
        "status": "processing"
    }
    
    # TODO: Add background processing task
    # background_tasks.add_task(process_batch, batch_id, uploaded_media, db)
    
    return {
        "batch_id": batch_id,
        "total_files": len(files),
        "uploaded": len([f for f in uploaded_media if f.get("status") == "pending"]),
        "failed": len([f for f in uploaded_media if f.get("status") == "failed"]),
        "files": uploaded_media
    }

@router.get("/batch/{batch_id}")
async def get_batch_status(batch_id: str):
    """Get status of batch upload job"""
    if batch_id not in batch_jobs:
        raise HTTPException(status_code=404, detail="Batch job not found")
    
    return batch_jobs[batch_id]

@router.get("/batch")
async def list_batches():
    """List all batch jobs"""
    return list(batch_jobs.values())

@router.delete("/batch/{batch_id}")
async def delete_batch(
    batch_id: str,
    db: Session = Depends(get_db)
):
    """Delete a batch job and all associated media"""
    if batch_id not in batch_jobs:
        raise HTTPException(status_code=404, detail="Batch job not found")
    
    batch = batch_jobs[batch_id]
    
    # Delete all media files
    for file_info in batch["files"]:
        if "media_id" in file_info:
            media_id = file_info["media_id"]
            
            # Delete from database
            media = db.query(Media).filter(Media.id == media_id).first()
            if media:
                db.delete(media)
            
            # Delete file (if exists)
            for ext in ['.jpg', '.png', '.mp4', '.mp3', '.wav']:
                file_path = os.path.join(STORAGE_PATH, f"{media_id}{ext}")
                if os.path.exists(file_path):
                    os.remove(file_path)
    
    db.commit()
    
    # Remove batch job
    del batch_jobs[batch_id]
    
    return {"message": "Batch deleted successfully"}
