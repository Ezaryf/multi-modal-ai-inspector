"""
Text analysis service
"""
import os

def analyze_text(file_path: str) -> dict:
    """
    Analyze text file
    Returns dict with content and metadata
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return {
            "transcript": content,  # Use 'transcript' key so LLM service picks it up automatically
            "language": "en",      # Assumption for now
            "word_count": len(content.split()),
            "char_count": len(content)
        }
    except UnicodeDecodeError:
        # Fallback for non-UTF-8
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
            
        return {
            "transcript": content,
            "language": "unknown",
            "word_count": len(content.split()),
            "char_count": len(content)
        }
