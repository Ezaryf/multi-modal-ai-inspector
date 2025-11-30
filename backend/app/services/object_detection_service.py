"""
Object Detection service using YOLOv8
Detects objects, people, animals, vehicles in images and video frames
"""
from ultralytics import YOLO
import os
from PIL import Image
from typing import List, Dict
import numpy as np

# Global model instance (lazy loaded)
_yolo_model = None

def get_yolo_model():
    """Lazy load YOLO model"""
    global _yolo_model
    if _yolo_model is None:
        model_name = os.getenv("YOLO_MODEL", "yolov8n.pt")  # nano model (smallest)
        print(f"Loading YOLO model: {model_name}")
        _yolo_model = YOLO(model_name)
    return _yolo_model

def detect_objects(image_path: str, confidence_threshold: float = 0.25) -> Dict:
    """
    Detect objects in an image using YOLOv8
    
    Args:
        image_path: Path to image file
        confidence_threshold: Minimum confidence for detections (0-1)
    
    Returns:
        Dict with detected objects, counts, and metadata
    """
    model = get_yolo_model()
    
    # Run inference
    results = model.predict(
        source=image_path,
        conf=confidence_threshold,
        verbose=False
    )
    
    # Extract results
    detections = []
    class_counts = {}
    
    for result in results:
        boxes = result.boxes
        
        for box in boxes:
            # Get box coordinates
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            
            # Get class and confidence
            cls_id = int(box.cls[0].cpu().numpy())
            confidence = float(box.conf[0].cpu().numpy())
            class_name = result.names[cls_id]
            
            detection = {
                "label": class_name,
                "confidence": round(confidence, 3),
                "bbox": {
                    "x": int(x1),
                    "y": int(y1),
                    "width": int(x2 - x1),
                    "height": int(y2 - y1)
                }
            }
            
            detections.append(detection)
            
            # Count occurrences
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
    
    # Get image dimensions
    img = Image.open(image_path)
    width, height = img.size
    img.close()
    
    return {
        "detections": detections,
        "total_objects": len(detections),
        "object_counts": class_counts,
        "unique_classes": len(class_counts),
        "image_dimensions": {"width": width, "height": height},
        "confidence_threshold": confidence_threshold
    }

def detect_objects_batch(image_paths: List[str], confidence_threshold: float = 0.25) -> List[Dict]:
    """
    Detect objects in multiple images (batch processing)
    More efficient than calling detect_objects individually
    
    Args:
        image_paths: List of image file paths
        confidence_threshold: Minimum confidence for detections
    
    Returns:
        List of detection results (one per image)
    """
    model = get_yolo_model()
    
    # Run batch inference
    results = model.predict(
        source=image_paths,
        conf=confidence_threshold,
        verbose=False
    )
    
    all_detections = []
    
    for idx, result in enumerate(results):
        detections = []
        class_counts = {}
        
        boxes = result.boxes
        
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            cls_id = int(box.cls[0].cpu().numpy())
            confidence = float(box.conf[0].cpu().numpy())
            class_name = result.names[cls_id]
            
            detection = {
                "label": class_name,
                "confidence": round(confidence, 3),
                "bbox": {
                    "x": int(x1),
                    "y": int(y1),
                    "width": int(x2 - x1),
                    "height": int(y2 - y1)
                }
            }
            
            detections.append(detection)
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        # Get image dimensions
        img = Image.open(image_paths[idx])
        width, height = img.size
        img.close()
        
        all_detections.append({
            "image_path": image_paths[idx],
            "detections": detections,
            "total_objects": len(detections),
            "object_counts": class_counts,
            "unique_classes": len(class_counts),
            "image_dimensions": {"width": width, "height": height}
        })
    
    return all_detections

def get_supported_classes() -> List[str]:
    """Get list of object classes that YOLO can detect"""
    model = get_yolo_model()
    return list(model.names.values())

def analyze_scene(detections: List[Dict]) -> str:
    """
    Generate natural language description of detected scene
    
    Args:
        detections: List of detection dicts
    
    Returns:
        Human-readable scene description
    """
    if not detections:
        return "No objects detected in the scene."
    
    # Count people
    people_count = sum(1 for d in detections if d["label"] == "person")
    
    # Get other objects
    other_objects = {}
    for d in detections:
        if d["label"] != "person":
            other_objects[d["label"]] = other_objects.get(d["label"], 0) + 1
    
    # Build description
    parts = []
    
    if people_count > 0:
        if people_count == 1:
            parts.append("1 person")
        else:
            parts.append(f"{people_count} people")
    
    if other_objects:
        object_strs = [
            f"{count} {label}{'s' if count > 1 else ''}"
            for label, count in sorted(other_objects.items(), key=lambda x: -x[1])[:5]
        ]
        parts.extend(object_strs)
    
    if len(parts) == 0:
        return "Scene detected but no specific objects identified."
    elif len(parts) == 1:
        return f"Scene contains {parts[0]}."
    elif len(parts) == 2:
        return f"Scene contains {parts[0]} and {parts[1]}."
    else:
        return f"Scene contains {', '.join(parts[:-1])}, and {parts[-1]}."
