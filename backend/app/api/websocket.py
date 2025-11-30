"""
WebSocket API endpoints
Real-time updates for media analysis
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/{media_id}")
async def websocket_endpoint(websocket: WebSocket, media_id: str):
    """
    WebSocket endpoint for real-time updates on media analysis
    
    Usage:
        ws = new WebSocket('ws://localhost:8000/ws/{media_id}')
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data)
            // Handle: progress, analysis_complete, error
        }
    """
    await manager.connect(websocket, media_id)
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            
            # Echo back or handle commands (optional)
            await manager.send_personal_message({
                "type": "ack",
                "message": f"Received: {data}"
            }, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, media_id)
