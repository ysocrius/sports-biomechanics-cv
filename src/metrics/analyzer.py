"""Biomechanical metrics calculation for cricket analysis."""
import numpy as np
from typing import Dict, List
from src.utils.geometry import calculate_angle, get_keypoint, center_of_mass

# COCO Pose keypoint indices (YOLOv8)
NOSE = 0
LEFT_SHOULDER, RIGHT_SHOULDER = 5, 6
LEFT_ELBOW, RIGHT_ELBOW = 7, 8
LEFT_WRIST, RIGHT_WRIST = 9, 10
LEFT_HIP, RIGHT_HIP = 11, 12
LEFT_KNEE, RIGHT_KNEE = 13, 14
LEFT_ANKLE, RIGHT_ANKLE = 15, 16

class MetricsEngine:
    def __init__(self, sport_type: str = 'cricket'):
        self.sport_type = sport_type
        self.frame_metrics = []
    
    def calculate_frame_metrics(self, landmarks: List[Dict]) -> Dict:
        """Calculate all metrics for a single frame."""
        if not landmarks:
            return {}
        
        metrics = {
            'knee_angle_left': self._knee_angle(landmarks, 'left'),
            'knee_angle_right': self._knee_angle(landmarks, 'right'),
            'elbow_angle_left': self._elbow_angle(landmarks, 'left'),
            'elbow_angle_right': self._elbow_angle(landmarks, 'right'),
            'com_x': self._center_of_mass(landmarks)[0],
            'com_y': self._center_of_mass(landmarks)[1]
        }
        
        # Add interpretations
        metrics['knee_status'] = self._interpret_knee(metrics['knee_angle_right'])
        
        self.frame_metrics.append(metrics)
        return metrics
    
    def _knee_angle(self, landmarks: List[Dict], side: str) -> float:
        """Calculate knee flexion angle."""
        if side == 'left':
            hip, knee, ankle = LEFT_HIP, LEFT_KNEE, LEFT_ANKLE
        else:
            hip, knee, ankle = RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE
        
        p_hip = get_keypoint(landmarks, hip)
        p_knee = get_keypoint(landmarks, knee)
        p_ankle = get_keypoint(landmarks, ankle)
        
        return calculate_angle(p_hip, p_knee, p_ankle)
    
    def _elbow_angle(self, landmarks: List[Dict], side: str) -> float:
        """Calculate elbow flexion angle."""
        if side == 'left':
            shoulder, elbow, wrist = LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST
        else:
            shoulder, elbow, wrist = RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST
        
        p_shoulder = get_keypoint(landmarks, shoulder)
        p_elbow = get_keypoint(landmarks, elbow)
        p_wrist = get_keypoint(landmarks, wrist)
        
        return calculate_angle(p_shoulder, p_elbow, p_wrist)
    
    def _center_of_mass(self, landmarks: List[Dict]) -> tuple:
        """Estimate center of mass from torso keypoints."""
        torso_indices = [LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_HIP, RIGHT_HIP]
        return center_of_mass(landmarks, torso_indices)
    
    def _interpret_knee(self, angle: float) -> str:
        """Interpret knee angle based on sport."""
        if self.sport_type == 'tennis':
            if angle < 120:
                return "Good Loading (Serve)"
            elif angle > 160:
                return "Extension"
            else:
                return "Transition"
        
        # Default: Cricket logic
        if angle > 160:
            return "Straight (High)"
        elif angle > 140:
            return "Good Balance"
        else:
            return "Deep Bend"
    
    def get_summary_stats(self) -> Dict:
        """Calculate summary statistics across all frames."""
        if not self.frame_metrics:
            return {}
        
        knee_angles = [m['knee_angle_right'] for m in self.frame_metrics if m.get('knee_angle_right')]
        
        return {
            'avg_knee_angle': np.mean(knee_angles) if knee_angles else 0,
            'min_knee_angle': np.min(knee_angles) if knee_angles else 0,
            'max_knee_angle': np.max(knee_angles) if knee_angles else 0
        }
