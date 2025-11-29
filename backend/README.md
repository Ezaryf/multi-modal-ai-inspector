# Multi-Modal AI Inspector - Backend

FastAPI backend for analyzing images, audio, and video with AI models.

## Features

- 🖼️ **Image Analysis**: BLIP captioning, color extraction, tag generation
- 🎵 **Audio Analysis**: Whisper transcription, sentiment analysis, keyword extraction
- 🎬 **Video Analysis**: Frame extraction, audio extraction, combined analysis
- 💬 **LLM Chat**: Conversational assistant for exploring media content
- 📊 **Structured Analytics**: Database-backed analysis storage and retrieval

## Setup

### Prerequisites

- Python 3.9+
- FFmpeg installed and in PATH
- 8GB+ RAM (for running models locally)

### Installation

1. Create virtual environment:
```bash
python -m venv .venv
```

2. Activate environment:
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
copy .env.example .env
# Edit .env with your settings
```

5. Create storage directory:
```bash
mkdir storage
```

## Running the Server

Start the development server:

```bash
# From backend directory
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: http://localhost:8000

API documentation: http://localhost:8000/docs

## API Endpoints

### Upload
- `POST /upload` - Upload media file

### Media
- `GET /media/{id}` - Get media metadata and analysis
- `GET /media/{id}/analysis` - Get all analyses
- `GET /download/{id}` - Download original file
- `GET /media` - List all media

### Chat
- `POST /ask` - Ask question about media
- `GET /chat/{media_id}` - Get chat history

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/                 # API endpoints
│   │   ├── upload.py
│   │   ├── ask.py
│   │   └── media.py
│   ├── services/            # Analysis services
│   │   ├── image_service.py
│   │   ├── audio_service.py
│   │   ├── video_service.py
│   │   ├── llm_service.py
│   │   └── orchestrator.py
│   ├── models/              # Database models
│   │   └── db.py
│   └── utils/               # Utilities
│       ├── database.py
│       ├── file_validation.py
│       └── ffmpeg.py
├── requirements.txt
└── .env.example
```

## Models Used

- **BLIP** (Salesforce/blip-image-captioning-base) - Image captioning
- **Whisper** (small) - Audio transcription
- **DistilBERT** - Sentiment analysis
- **OPT-1.3B** (Facebook) - LLM for chat (lightweight, CPU-friendly)

## Development

Run tests (when implemented):
```bash
pytest
```

Format code:
```bash
black app/
```

## Notes

- First run will download AI models (~2-5GB total)
- Models are cached in `~/.cache/huggingface`
- For production, consider using GPU inference
- SQLite database created as `inspector.db` in backend directory
