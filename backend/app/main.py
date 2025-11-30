"""
FastAPI Main Application
Multi-Modal AI Inspector Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.database import init_db
from app.api import upload, ask, media, export, websocket, batch
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="Multi-Modal AI Inspector",
    description="Hybrid conversational AI analyst for images, audio, and video",
    version="2.0.0"
)

# CORS middleware
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, tags=["Upload"])
app.include_router(ask.router, tags=["Chat"])
app.include_router(media.router, tags=["Media"])
app.include_router(export.router, tags=["Export"])
app.include_router(websocket.router, tags=["WebSocket"])
app.include_router(batch.router, tags=["Batch"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Multi-Modal AI Inspector",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "storage": os.path.exists(os.getenv("STORAGE_PATH", "./storage"))
    }

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug
    )
