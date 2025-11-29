# 🎯 Multi-Modal AI Inspector

> **Hybrid conversational AI analyst for images, audio, and video**

A production-ready full-stack application that analyzes multimedia content using state-of-the-art AI models and provides conversational insights through an intelligent chat interface.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)

## ✨ Features

### 🖼️ Image Analysis
- **BLIP Captioning** - Generate natural language descriptions
- **Color Extraction** - Identify dominant color palettes
- **Tag Generation** - Automatic keyword extraction

### 🎵 Audio Analysis
- **Whisper Transcription** - State-of-the-art speech-to-text
- **Sentiment Analysis** - Detect emotional tone
- **Keyword Extraction** - Identify key topics
- **Language Detection** - Automatic language identification

### 🎬 Video Analysis
- **Frame Extraction** - Sample key moments
- **Audio Track Analysis** - Extract and transcribe audio
- **Visual Timeline** - Frame-by-frame breakdown
- **Combined Insights** - Unified analysis

### 💬 Conversational Assistant
- **Context-Aware Chat** - Ask questions about your media
- **Structured Responses** - Facts + creative interpretation
- **Source Attribution** - Track where insights come from
- **Chat History** - Persistent conversation threads

### 🎨 Modern UI
- **Dark Theme** - Sleek, professional design
- **Glassmorphism** - Modern visual effects
- **Drag & Drop** - Intuitive file uploads
- **Real-time Updates** - Live analysis progress
- **Responsive Design** - Works on all devices

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   React     │ ◄────── │   FastAPI    │ ◄────── │  AI Models  │
│   Frontend  │  HTTP   │   Backend    │         │   (Local)   │
│             │         │              │         │             │
│  • Upload   │         │  • Routes    │         │  • BLIP     │
│  • Chat UI  │         │  • Services  │         │  • Whisper  │
│  • Analytics│         │  • DB (SQL)  │         │  • LLM      │
└─────────────┘         └──────────────┘         └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Node.js 16+**
- **FFmpeg** (for video processing)
- **8GB+ RAM** (for running models locally)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd multi-modal-ai-inspector
```

2. **Backend Setup**
```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

# Create environment file
copy .env.example .env
# Edit .env as needed

# Create storage directory
mkdir storage
```

3. **Frontend Setup**
```bash
cd ../frontend
npm install
```

### Running Locally

**Terminal 1 - Backend:**
```bash
cd backend
.venv\Scripts\activate  # or source .venv/bin/activate
python -m app.main
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Open in browser:** http://localhost:5173

## 📁 Project Structure

```
multi-modal-ai-inspector/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── api/                 # API endpoints
│   │   │   ├── upload.py
│   │   │   ├── ask.py
│   │   │   └── media.py
│   │   ├── services/            # Analysis services
│   │   │   ├── image_service.py
│   │   │   ├── audio_service.py
│   │   │   ├── video_service.py
│   │   │   ├── llm_service.py
│   │   │   └── orchestrator.py
│   │   ├── models/              # Database models
│   │   │   └── db.py
│   │   └── utils/               # Utilities
│   │       ├── database.py
│   │       ├── file_validation.py
│   │       └── ffmpeg.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadDropzone.jsx
│   │   │   ├── MediaPlayer.jsx
│   │   │   ├── AnalyticsPanel.jsx
│   │   │   └── ChatPanel.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🤖 AI Models Used

| Model | Purpose | Size |
|-------|---------|------|
| [Salesforce/BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base) | Image captioning | ~1GB |
| [OpenAI Whisper](https://github.com/openai/whisper) (small) | Audio transcription | ~500MB |
| [DistilBERT](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english) | Sentiment analysis | ~250MB |
| [Facebook OPT-1.3B](https://huggingface.co/facebook/opt-1.3b) | Conversational LLM | ~2.5GB |

**Total model size:** ~4-5GB (downloaded automatically on first run)

## 📊 Database Schema

SQLite database with the following tables:

- `media` - Uploaded files metadata
- `analysis` - Analysis results (JSON)
- `transcript_segments` - Transcript with timestamps
- `objects` - Detected objects (future)
- `reports` - Generated summaries
- `chats` - Conversation history

## 🔒 Security & Privacy

- ✅ File type and size validation
- ✅ MIME type verification
- ✅ Secure file storage
- ✅ CORS configuration
- ⚠️ **Note:** For production, add authentication and encryption

## 🌐 Deployment

### Zero-Cost Options

1. **Frontend (Vercel)**
   - Push to GitHub
   - Import in Vercel
   - Auto-deploy on push

2. **Backend (Hugging Face Spaces)**
   - Create Space with FastAPI
   - Deploy backend code
   - CPU inference (free tier)

3. **Alternative: Local Demo**
   - Run locally
   - Record screencast
   - Share video demo

### Production Deployment

- **Frontend:** Vercel, Netlify, CloudFlare Pages
- **Backend:** Railway, Render, DigitalOcean
- **Database:** PostgreSQL (upgrade from SQLite)
- **Models:** GPU inference for speed

## 🧪 Testing

```bash
# Backend (future)
cd backend
pytest

# Frontend (future)
cd frontend
npm test
```

## 📈 Roadmap

- [ ] Object detection (YOLO/DETR)
- [ ] Speaker diarization
- [ ] Multi-language support
- [ ] Batch processing
- [ ] Export reports (PDF)
- [ ] User authentication
- [ ] Cloud storage integration
- [ ] Real-time streaming analysis

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- **Salesforce** - BLIP image captioning
- **OpenAI** - Whisper speech recognition
- **Hugging Face** - Model hosting and transformers library
- **FFmpeg** - Media processing

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at `/docs` endpoint

---

**Built with ❤️ using FastAPI, React, and state-of-the-art AI models**
