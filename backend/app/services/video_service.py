"""
Video analysis service - orchestrates audio + frame analysis
"""
import os
from typing import Dict, List
from app.utils.ffmpeg import extract_audio_from_video, extract_frames, extract_video_metadata
from app.services.audio_service import analyze_audio
from app.services.image_service import analyze_image

def analyze_video(video_path: str, storage_dir: str) -> Dict:
    """
    Analyze video by extracting audio and frames, then analyzing each
    Returns: combined analysis results
    """
    # Extract metadata
    duration, width, height = extract_video_metadata(video_path)
    
    # Create working directory for this video
    video_id = os.path.basename(video_path).split('.')[0]
    work_dir = os.path.join(storage_dir, f"temp_{video_id}")
    os.makedirs(work_dir, exist_ok=True)
    
    results = {
        "duration": duration,
        "width": width,
        "height": height,
        "aspect_ratio": round(width / height, 2)
    }
    
    # Extract and analyze audio
    audio_path = os.path.join(work_dir, "audio.wav")
    try:
        extract_audio_from_video(video_path, audio_path)
        audio_analysis = analyze_audio(audio_path)
        results["audio"] = audio_analysis
    except Exception as e:
        print(f"Audio extraction/analysis failed: {e}")
        results["audio"] = {"error": str(e)}
    
    # Extract and analyze frames (sample at 1 fps)
    frames_dir = os.path.join(work_dir, "frames")
    try:
        # Sample frames - limit to avoid overload
        sample_fps = 0.5 if duration > 30 else 1  # Every 2s for long videos, every 1s for short
        frame_paths = extract_frames(video_path, frames_dir, fps=sample_fps)
        
        # Analyze a subset of frames (max 10)
        max_frames = min(10, len(frame_paths))
        frame_analyses = []
        
        for i, frame_path in enumerate(frame_paths[:max_frames]):
            try:
                analysis = analyze_image(frame_path)
                analysis["timestamp"] = i / sample_fps
                frame_analyses.append(analysis)
            except Exception as e:
                print(f"Frame {i} analysis failed: {e}")
        
        results["frames"] = {
            "total_extracted": len(frame_paths),
            "analyzed": len(frame_analyses),
            "samples": frame_analyses
        }
        
        # Generate overall video description from frames
        if frame_analyses:
            results["visual_summary"] = generate_visual_summary(frame_analyses)
        
    except Exception as e:
        print(f"Frame extraction/analysis failed: {e}")
        results["frames"] = {"error": str(e)}
    
    # Clean up temp files (optional, comment out for debugging)
    # import shutil
    # if os.path.exists(work_dir):
    #     shutil.rmtree(work_dir)
    
    return results

def generate_visual_summary(frame_analyses: List[Dict]) -> str:
    """Generate summary from frame captions"""
    if not frame_analyses:
        return "No visual content analyzed"
    
    # Get unique scenes/captions
    captions = [fa["caption"] for fa in frame_analyses]
    
    # Simple approach: concatenate unique captions
    unique_captions = []
    seen = set()
    for cap in captions:
        if cap not in seen:
            unique_captions.append(cap)
            seen.add(cap)
    
    if len(unique_captions) == 1:
        return f"Video shows: {unique_captions[0]}"
    else:
        return f"Video contains {len(unique_captions)} distinct scenes: " + "; ".join(unique_captions[:5])
