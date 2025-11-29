"""
FFmpeg utilities for video processing
"""
import ffmpeg
import os
from typing import Tuple, List

def extract_video_metadata(video_path: str) -> Tuple[float, int, int]:
    """
    Extract duration, width, height from video
    Returns: (duration_sec, width, height)
    """
    probe = ffmpeg.probe(video_path)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    
    duration = float(probe['format']['duration'])
    width = int(video_info['width'])
    height = int(video_info['height'])
    
    return duration, width, height

def extract_audio_from_video(video_path: str, output_path: str) -> str:
    """
    Extract audio track from video
    Returns: path to extracted audio file
    """
    try:
        (
            ffmpeg
            .input(video_path)
            .output(output_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True, quiet=True)
        )
        return output_path
    except ffmpeg.Error as e:
        raise RuntimeError(f"Audio extraction failed: {e.stderr.decode()}")

def extract_frames(video_path: str, output_dir: str, fps: int = 1) -> List[str]:
    """
    Extract frames from video at specified FPS
    Returns: list of frame paths
    """
    os.makedirs(output_dir, exist_ok=True)
    output_pattern = os.path.join(output_dir, "frame_%04d.jpg")
    
    try:
        (
            ffmpeg
            .input(video_path)
            .filter('fps', fps=fps)
            .output(output_pattern, **{'q:v': 2})
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True, quiet=True)
        )
        
        # Get list of created frames
        frames = sorted([
            os.path.join(output_dir, f) 
            for f in os.listdir(output_dir) 
            if f.startswith("frame_") and f.endswith(".jpg")
        ])
        
        return frames
    except ffmpeg.Error as e:
        raise RuntimeError(f"Frame extraction failed: {e.stderr.decode()}")

def get_audio_duration(audio_path: str) -> float:
    """Get duration of audio file in seconds"""
    probe = ffmpeg.probe(audio_path)
    return float(probe['format']['duration'])
