"""Vector geometry utilities for biomechanical analysis."""
import numpy as np
from typing import Tuple

def calculate_angle(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> float:
    """
    Calculate angle at p2 formed by p1-p2-p3.
    
    Args:
        p1, p2, p3: (x, y) coordinates
        
    Returns:
        Angle in degrees (0-180)
    """
    v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
    v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
    
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    return np.degrees(angle)

def get_keypoint(landmarks: list, idx: int) -> Tuple[float, float]:
    """Extract (x, y) pixel coordinates from landmark list."""
    if idx < len(landmarks):
        return (landmarks[idx]['px'], landmarks[idx]['py'])
    return (0, 0)

def center_of_mass(landmarks: list, indices: list) -> Tuple[float, float]:
    """Calculate center of mass for given keypoint indices."""
    points = [get_keypoint(landmarks, i) for i in indices]
    x = np.mean([p[0] for p in points])
    y = np.mean([p[1] for p in points])
    return (x, y)
