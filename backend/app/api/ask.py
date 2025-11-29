"""
Ask/Chat API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.utils.database import get_db
from app.models.db import Media, Chat
from app.services.orchestrator import get_media_context
from app.services.llm_service import ask_llm

router = APIRouter()

class AskRequest(BaseModel):
    media_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list = []

@router.post("/ask", response_model=ChatResponse)
async def ask_question(
    request: AskRequest,
    db: Session = Depends(get_db)
):
    """
    Ask a question about analyzed media
    Returns LLM-generated answer with sources
    """
    # Verify media exists
    media = db.query(Media).filter(Media.id == request.media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    # Get media context (all analyses)
    context = get_media_context(db, request.media_id)
    
    if not context:
        raise HTTPException(status_code=400, detail="Media not yet analyzed")
    
    # Get chat history
    chat_history = db.query(Chat).filter(
        Chat.media_id == request.media_id
    ).order_by(Chat.created_at).all()
    
    history_dicts = [
        {"role": msg.role, "message": msg.message}
        for msg in chat_history
    ]
    
    # Generate answer
    try:
        answer = ask_llm(context, request.question, history_dicts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM failed: {str(e)}")
    
    # Save to chat history
    user_msg = Chat(
        media_id=request.media_id,
        role="user",
        message=request.question
    )
    assistant_msg = Chat(
        media_id=request.media_id,
        role="assistant",
        message=answer
    )
    
    db.add(user_msg)
    db.add(assistant_msg)
    db.commit()
    
    # Extract sources (simple approach)
    sources = extract_sources(context)
    
    return ChatResponse(answer=answer, sources=sources)

@router.get("/chat/{media_id}")
async def get_chat_history(
    media_id: str,
    db: Session = Depends(get_db)
):
    """Get chat history for a media item"""
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    chats = db.query(Chat).filter(
        Chat.media_id == media_id
    ).order_by(Chat.created_at).all()
    
    return [
        {
            "id": chat.id,
            "role": chat.role,
            "message": chat.message,
            "created_at": chat.created_at.isoformat()
        }
        for chat in chats
    ]

def extract_sources(context: dict) -> list:
    """Extract source pointers from context"""
    sources = []
    
    if "transcript" in context:
        sources.append("transcript")
    
    if "frames" in context:
        sources.append("frames")
    
    if "caption" in context:
        sources.append("image_caption")
    
    return sources
