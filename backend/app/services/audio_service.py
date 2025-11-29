"""
Audio analysis service using Whisper
"""
import whisper
import os
from typing import Dict, List
from transformers import pipeline

# Global model instance (lazy loaded)
_whisper_model = None
_sentiment_analyzer = None

def get_whisper_model():
    """Lazy load Whisper model"""
    global _whisper_model
    if _whisper_model is None:
        model_size = os.getenv("WHISPER_MODEL", "small")
        print(f"Loading Whisper model: {model_size}")
        _whisper_model = whisper.load_model(model_size)
    return _whisper_model

def get_sentiment_analyzer():
    """Lazy load sentiment analyzer"""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        print("Loading sentiment analyzer")
        _sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    return _sentiment_analyzer

def analyze_audio(audio_path: str) -> Dict:
    """
    Transcribe audio using Whisper and analyze sentiment
    Returns: dict with transcript, segments, language, sentiment
    """
    model = get_whisper_model()
    
    # Transcribe
    result = model.transcribe(audio_path, verbose=False)
    
    text = result["text"]
    segments = result.get("segments", [])
    language = result.get("language", "unknown")
    
    # Analyze sentiment on full text
    sentiment = analyze_sentiment(text)
    
    # Format segments
    formatted_segments = [
        {
            "text": seg["text"],
            "start": seg["start"],
            "end": seg["end"]
        }
        for seg in segments
    ]
    
    return {
        "transcript": text,
        "segments": formatted_segments,
        "language": language,
        "sentiment": sentiment,
        "word_count": len(text.split())
    }

def analyze_sentiment(text: str) -> Dict:
    """Analyze sentiment of text"""
    if not text.strip():
        return {"label": "neutral", "score": 0.0}
    
    analyzer = get_sentiment_analyzer()
    
    # Truncate if too long (512 tokens max for most models)
    words = text.split()[:100]
    truncated_text = " ".join(words)
    
    try:
        result = analyzer(truncated_text)[0]
        return {
            "label": result["label"].lower(),
            "score": round(result["score"], 3)
        }
    except Exception as e:
        print(f"Sentiment analysis failed: {e}")
        return {"label": "unknown", "score": 0.0}

def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """Simple keyword extraction from transcript"""
    # Remove common words
    stop_words = {'i', 'me', 'my', 'we', 'you', 'he', 'she', 'it', 'they', 
                  'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 
                  'were', 'to', 'of', 'in', 'on', 'at', 'for', 'with'}
    
    words = text.lower().split()
    keywords = [w.strip('.,!?;:') for w in words if w not in stop_words and len(w) > 3]
    
    # Count frequency
    from collections import Counter
    word_counts = Counter(keywords)
    
    return [word for word, _ in word_counts.most_common(top_n)]
