"""
Image analysis service using BLIP and CLIP
"""
from transformers import BlipProcessor, BlipForConditionalGeneration, CLIPProcessor, CLIPModel
from PIL import Image
import torch
import os
from typing import Dict, List

# Global model instances (lazy loaded)
_blip_processor = None
_blip_model = None
_clip_processor = None
_clip_model = None

def get_blip_models():
    """Lazy load BLIP models"""
    global _blip_processor, _blip_model
    if _blip_processor is None:
        model_name = os.getenv("BLIP_MODEL", "Salesforce/blip-image-captioning-base")
        print(f"Loading BLIP model: {model_name}")
        _blip_processor = BlipProcessor.from_pretrained(model_name)
        _blip_model = BlipForConditionalGeneration.from_pretrained(model_name)
    return _blip_processor, _blip_model

def get_clip_models():
    """Lazy load CLIP models"""
    global _clip_processor, _clip_model
    if _clip_processor is None:
        model_name = "openai/clip-vit-base-patch32"
        print(f"Loading CLIP model: {model_name}")
        _clip_processor = CLIPProcessor.from_pretrained(model_name)
        _clip_model = CLIPModel.from_pretrained(model_name)
    return _clip_processor, _clip_model

def analyze_image(image_path: str, detect_objects: bool = True) -> Dict:
    """
    Analyze image using BLIP for captioning and optionally detect objects
    Returns: dict with caption, colors, dimensions, and objects
    """
    # Load image
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    
    # Generate caption using BLIP
    processor, model = get_blip_models()
    inputs = processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        out = model.generate(**inputs, max_length=50)
    
    caption = processor.decode(out[0], skip_special_tokens=True)
    
    # Extract dominant colors (simple version)
    colors = extract_dominant_colors(image)
    
    result = {
        "caption": caption,
        "width": width,
        "height": height,
        "colors": colors,
        "aspect_ratio": round(width / height, 2)
    }
    
    # Add object detection if enabled
    if detect_objects:
        try:
            from app.services.object_detection_service import detect_objects as yolo_detect
            detection_result = yolo_detect(image_path)
            result["object_detection"] = detection_result
        except Exception as e:
            print(f"Object detection failed: {e}")
            result["object_detection"] = {"error": str(e)}
    
    return result

def extract_dominant_colors(image: Image.Image, num_colors: int = 5) -> List[str]:
    """Extract dominant colors from image (simple palette extraction)"""
    # Resize for performance
    image = image.resize((100, 100))
    
    # Get color palette
    palette = image.quantize(colors=num_colors).getpalette()
    
    # Convert to hex colors
    colors = []
    for i in range(num_colors):
        r, g, b = palette[i*3:i*3+3]
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        colors.append(hex_color)
    
    return colors

def generate_tags_from_caption(caption: str) -> List[str]:
    """Generate tags from caption (simple keyword extraction)"""
    # Simple approach: split and filter common words
    stop_words = {'a', 'an', 'the', 'is', 'are', 'in', 'on', 'of', 'with', 'and', 'or'}
    words = caption.lower().split()
    tags = [w.strip('.,!?') for w in words if w not in stop_words and len(w) > 2]
    return list(set(tags))[:10]  # Return unique tags, max 10
