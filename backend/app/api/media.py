"""
Media API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.db import Media, Analysis, Report
import os

router = APIRouter()

STORAGE_PATH = os.getenv("STORAGE_PATH", "./storage")

@router.get("/media/{media_id}")
async def get_media(
    media_id: str,
    db: Session = Depends(get_db)
):
    """Get media metadata and latest analysis summary"""
    media = db.query(Media).filter(Media.id == media_id).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    # Get latest analysis
    latest_analysis = db.query(Analysis).filter(
        Analysis.media_id == media_id
    ).order_by(Analysis.created_at.desc()).first()
    
    # Get latest report
    latest_report = db.query(Report).filter(
        Report.media_id == media_id
    ).order_by(Report.created_at.desc()).first()
    
    return {
        "id": media.id,
        "filename": media.filename,
        "media_type": media.media_type,
        "uploaded_at": media.uploaded_at.isoformat(),
        "duration": media.duration,
        "width": media.width,
        "height": media.height,
        "size_bytes": media.size_bytes,
        "analysis": latest_analysis.payload if latest_analysis else None,
        "summary": latest_report.summary if latest_report else None,
        "status": "completed" if latest_analysis else "processing"
    }

@router.get("/media/{media_id}/analysis")
async def get_all_analyses(
    media_id: str,
    db: Session = Depends(get_db)
):
    """Get all analysis records for a media item"""
    media = db.query(Media).filter(Media.id == media_id).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    analyses = db.query(Analysis).filter(
        Analysis.media_id == media_id
    ).order_by(Analysis.created_at).all()
    
    return [
        {
            "id": analysis.id,
            "stage": analysis.stage,
            "payload": analysis.payload,
            "created_at": analysis.created_at.isoformat()
        }
        for analysis in analyses
    ]

@router.get("/download/{media_id}")
async def download_media(
    media_id: str,
    db: Session = Depends(get_db)
):
    """Download original media file"""
    media = db.query(Media).filter(Media.id == media_id).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    # Find file (try different extensions)
    file_path = None
    for ext in ['.jpg', '.png', '.gif', '.mp4', '.mp3', '.wav', '.mov', '.avi']:
        candidate = os.path.join(STORAGE_PATH, f"{media_id}{ext}")
        if os.path.exists(candidate):
            file_path = candidate
            break
    
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=media.filename
    )

@router.get("/media")
async def list_media(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all media items"""
    media_items = db.query(Media).order_by(
        Media.uploaded_at.desc()
    ).limit(limit).offset(offset).all()
    
    return [
        {
            "id": m.id,
            "filename": m.filename,
            "media_type": m.media_type,
            "uploaded_at": m.uploaded_at.isoformat(),
            "size_bytes": m.size_bytes
        }
        for m in media_items
    ]
