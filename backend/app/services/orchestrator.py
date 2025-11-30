"""
Orchestrator service - coordinates all analysis pipelines
"""
from app.services.image_service import analyze_image
from app.services.audio_service import analyze_audio
from app.services.video_service import analyze_video
from app.services.llm_service import summarize_analysis
from app.utils.file_validation import detect_media_type
from app.models.db import Media, Analysis, TranscriptSegment, Report
from app.utils.websocket_manager import manager
from sqlalchemy.orm import Session
import json
import os
import asyncio

async def start_processing(db: Session, media_id: str, file_path: str, storage_dir: str):
    """
    Main orchestrator: analyzes media and saves results to database
    Now with WebSocket progress updates
    
    Args:
        db: Database session
        media_id: Media record ID
        file_path: Path to uploaded file
        storage_dir: Storage directory for temp files
    """
    print(f"🚀 Starting processing for {media_id}")
    
    try:
        # Send initial progress
        await manager.send_progress_update(media_id, "starting", 0, "Initializing analysis...")
        
        # Get media record
        media = db.query(Media).filter(Media.id == media_id).first()
        if not media:
            raise ValueError(f"Media {media_id} not found")
        
        # Detect media type
        media_type = media.media_type
        
        # Run appropriate analysis
        if media_type == "image":
            await manager.send_progress_update(media_id, "image", 20, "Analyzing image...")
            result = analyze_image(file_path)
            stage = "image"
        elif media_type == "audio":
            await manager.send_progress_update(media_id, "audio", 20, "Transcribing audio...")
            result = analyze_audio(file_path)
            stage = "audio"
            # Save transcript segments
            save_transcript_segments(db, media_id, result.get("segments", []))
            await manager.send_progress_update(media_id, "audio", 60, "Analyzing sentiment...")
        elif media_type == "video":
            await manager.send_progress_update(media_id, "video", 20, "Extracting frames and audio...")
            result = analyze_video(file_path, storage_dir)
            stage = "video"
            # Save transcript segments if audio was analyzed
            if "audio" in result and "segments" in result["audio"]:
                save_transcript_segments(db, media_id, result["audio"]["segments"])
            await manager.send_progress_update(media_id, "video", 70, "Analyzing frames...")
        else:
            raise ValueError(f"Unknown media type: {media_type}")
        
        # Save analysis to database
        await manager.send_progress_update(media_id, "saving", 80, "Saving results...")
        
        analysis = Analysis(
            media_id=media_id,
            stage=stage,
            payload=result
        )
        db.add(analysis)
        
        # Generate summary report using LLM
        await manager.send_progress_update(media_id, "summarizing", 90, "Generating summary...")
        
        try:
            summary = summarize_analysis(result)
        except Exception as e:
            print(f"Summary generation failed: {e}")
            summary = f"Analysis completed for {media_type}"
        
        report = Report(
            media_id=media_id,
            summary=summary
        )
        db.add(report)
        
        db.commit()
        
        # Send completion via WebSocket
        await manager.send_progress_update(media_id, "complete", 100, "Analysis complete!")
        await manager.send_analysis_complete(media_id, result)
        
        print(f"✅ Processing completed for {media_id}")
        
    except Exception as e:
        print(f"❌ Processing failed for {media_id}: {e}")
        db.rollback()
        
        # Send error via WebSocket
        await manager.send_error(media_id, str(e))
        
        # Save error as analysis
        error_analysis = Analysis(
            media_id=media_id,
            stage="error",
            payload={"error": str(e)}
        )
        db.add(error_analysis)
        db.commit()
        raise

def save_transcript_segments(db: Session, media_id: str, segments: list):
    """Save transcript segments to database"""
    for seg in segments:
        transcript_seg = TranscriptSegment(
            media_id=media_id,
            text=seg.get("text", ""),
            start_sec=seg.get("start", 0),
            end_sec=seg.get("end", 0),
            speaker=seg.get("speaker")  # Will be None if not available
        )
        db.add(transcript_seg)

def get_media_context(db: Session, media_id: str) -> dict:
    """
    Build context dict from all analyses for a media item
    Used for LLM prompting
    """
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        return {}
    
    # Get latest analysis
    latest_analysis = db.query(Analysis).filter(
        Analysis.media_id == media_id
    ).order_by(Analysis.created_at.desc()).first()
    
    if not latest_analysis:
        return {}
    
    context = latest_analysis.payload.copy()
    
    # Add media metadata
    context["media_type"] = media.media_type
    context["filename"] = media.filename
    
    return context
