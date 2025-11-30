"""
WebSocket manager for real-time updates
Replaces polling with push notifications
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import asyncio

class ConnectionManager:
    """Manages WebSocket connections and broadcasts"""
    
    def __init__(self):
        # Map of media_id to set of connected websockets
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, media_id: str):
        """Accept new WebSocket connection"""
        await websocket.accept()
        
        if media_id not in self.active_connections:
            self.active_connections[media_id] = set()
        
        self.active_connections[media_id].add(websocket)
        print(f"✅ WebSocket connected for media {media_id}")
    
    def disconnect(self, websocket: WebSocket, media_id: str):
        """Remove WebSocket connection"""
        if media_id in self.active_connections:
            self.active_connections[media_id].discard(websocket)
            
            # Clean up empty sets
            if len(self.active_connections[media_id]) == 0:
                del self.active_connections[media_id]
        
        print(f"❌ WebSocket disconnected for media {media_id}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific websocket"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")
    
    async def broadcast_to_media(self, media_id: str, message: dict):
        """Broadcast message to all connections watching a specific media"""
        if media_id not in self.active_connections:
            return
        
        disconnected = []
        
        for connection in self.active_connections[media_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to connection: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for conn in disconnected:
            self.disconnect(conn, media_id)
    
    async def send_progress_update(self, media_id: str, stage: str, progress: int, message: str = ""):
        """Send analysis progress update"""
        await self.broadcast_to_media(media_id, {
            "type": "progress",
            "stage": stage,
            "progress": progress,
            "message": message
        })
    
    async def send_analysis_complete(self, media_id: str, analysis: dict):
        """Send analysis completion notification"""
        await self.broadcast_to_media(media_id, {
            "type": "analysis_complete",
            "media_id": media_id,
            "analysis": analysis
        })
    
    async def send_error(self, media_id: str, error: str):
        """Send error notification"""
        await self.broadcast_to_media(media_id, {
            "type": "error",
            "error": error
        })

# Global connection manager instance
manager = ConnectionManager()
