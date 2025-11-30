"""
Export API endpoints for generating reports
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.db import Media, Chat
from app.services.orchestrator import get_media_context
from app.services.report_service import (
    generate_pdf_report,
    generate_json_report,
    generate_markdown_report
)
import os
from datetime import datetime

router = APIRouter()

STORAGE_PATH = os.getenv("STORAGE_PATH", "./storage")

@router.get("/export/{media_id}/pdf")
async def export_pdf(
    media_id: str,
    db: Session = Depends(get_db)
):
    """Export analysis as PDF report"""
    # Get media
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    # Get analysis context
    analysis = get_media_context(db, media_id)
    if not analysis:
        raise HTTPException(status_code=400, detail="No analysis available")
    
    # Get chat history
    chat_history = db.query(Chat).filter(
        Chat.media_id == media_id
    ).order_by(Chat.created_at).all()
    
    chat_dicts = [
        {"role": msg.role, "message": msg.message}
        for msg in chat_history
    ]
    
    # Prepare media data
    media_data = {
        "id": media.id,
        "filename": media.filename,
        "media_type": media.media_type,
        "size_bytes": media.size_bytes,
        "uploaded_at": media.uploaded_at.isoformat(),
        "duration": media.duration,
        "width": media.width,
        "height": media.height
    }
    
    # Generate PDF
    pdf_filename = f"report_{media_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_path = os.path.join(STORAGE_PATH, pdf_filename)
    
    try:
        generate_pdf_report(media_data, analysis, chat_dicts, pdf_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{media.filename}_analysis.pdf"
    )

@router.get("/export/{media_id}/json")
async def export_json(
    media_id: str,
    db: Session = Depends(get_db)
):
    """Export analysis as JSON"""
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    analysis = get_media_context(db, media_id)
    if not analysis:
        raise HTTPException(status_code=400, detail="No analysis available")
    
    chat_history = db.query(Chat).filter(
        Chat.media_id == media_id
    ).order_by(Chat.created_at).all()
    
    chat_dicts = [
        {"role": msg.role, "message": msg.message, "created_at": msg.created_at.isoformat()}
        for msg in chat_history
    ]
    
    media_data = {
        "id": media.id,
        "filename": media.filename,
        "media_type": media.media_type,
        "size_bytes": media.size_bytes,
        "uploaded_at": media.uploaded_at.isoformat(),
        "duration": media.duration,
        "width": media.width,
        "height": media.height
    }
    
    json_content = generate_json_report(media_data, analysis, chat_dicts)
    
    return Response(
        content=json_content,
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename={media.filename}_analysis.json"
        }
    )

@router.get("/export/{media_id}/markdown")
async def export_markdown(
    media_id: str,
    db: Session = Depends(get_db)
):
    """Export analysis as Markdown"""
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    analysis = get_media_context(db, media_id)
    if not analysis:
        raise HTTPException(status_code=400, detail="No analysis available")
    
    chat_history = db.query(Chat).filter(
        Chat.media_id == media_id
    ).order_by(Chat.created_at).all()
    
    chat_dicts = [
        {"role": msg.role, "message": msg.message}
        for msg in chat_history
    ]
    
    media_data = {
        "id": media.id,
        "filename": media.filename,
        "media_type": media.media_type,
        "size_bytes": media.size_bytes,
        "uploaded_at": media.uploaded_at.isoformat(),
        "duration": media.duration,
        "width": media.width,
        "height": media.height
    }
    
    md_content = generate_markdown_report(media_data, analysis, chat_dicts)
    
    return Response(
        content=md_content,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f"attachment; filename={media.filename}_analysis.md"
        }
    )
