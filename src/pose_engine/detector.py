"""Pose detection using YOLOv8-pose."""
import cv2
import numpy as np
from ultralytics import YOLO
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)

class PoseDetector:
    def __init__(self, model: str = 'yolov8n-pose.pt'):
        self.model = YOLO(model)
        logger.info(f"YOLOv8-pose loaded: {model}")

    def process_frame(self, frame: np.ndarray) -> Optional[object]:
        results = self.model(frame, verbose=False)
        return results[0] if results else None

    def draw_landmarks(self, frame: np.ndarray, results: object) -> np.ndarray:
        if results and results.keypoints is not None:
            return results.plot()
        return frame

    def extract_landmarks(self, results: object, shape: tuple) -> List[Dict]:
        if not results or results.keypoints is None:
            return []
        kpts = results.keypoints.xy.cpu().numpy()[0]  # First person
        conf = results.keypoints.conf.cpu().numpy()[0]
        return [{
            'id': i,
            'px': int(kpts[i][0]), 'py': int(kpts[i][1]),
            'x': kpts[i][0]/shape[1], 'y': kpts[i][1]/shape[0],
            'visibility': float(conf[i])
        } for i in range(len(kpts))]
